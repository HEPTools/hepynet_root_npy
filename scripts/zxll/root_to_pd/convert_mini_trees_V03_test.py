import pathlib
import sys

import pandas as pd
import psutil
import ROOT
import uproot

MB = 1024 * 1024
GB = MB * 1024

ELECTRON_MASS = 0.00051099895  # GeV
MUON_MASS = 0.1056583755  # GeV

# setups
cut_level = "mva_2jet"
ntup_dir = pathlib.Path(f"/data/ZXll/ntuples/V03")
df_dir = pathlib.Path(f"/data/ZXll/data_frames/V03")
df_dir.mkdir(parents=True, exist_ok=True)

feature_list = [
    "is_ee",
    "is_mm",
    "lept_0_pt",
    "lept_0_eta",
    "lept_0_phi",
    "lept_1_pt",
    "lept_1_eta",
    "lept_1_phi",
    "ll_pt",
    "ll_m",
    "ll_dphi",
    "jet_0_pt",
    "jet_0_eta",
    "jet_0_phi",
    "jet_0_m",
    "jet_0_fjvt",
    "jet_0_time",
    "jet_1_pt",
    "jet_1_eta",
    "jet_1_phi",
    "jet_1_m",
    "jet_1_fjvt",
    "jet_1_time",
    "jj_m",
    "n_jet",
    "n_bjet",
    "met",
    "met_sumet",
    "met_phi",
    "met_sig",
    "met_ht",
    "weight",
]

bkg_ee_names = ["bkg_diboson"]
sig_ee_names = ["sig_HVTee_m0250"]
sig_masses = {"sig_HVTee_m0250": 250}

# convert to pandas DataFrame
def process_sample(sample_name, sample_path, is_sig, is_mc, channel, camp=None):
    print(f"Processing: {sample_name}")
    sample_dfs = list()
    for chunk_pd in uproot.iterate(
        f"{sample_path}:ntup",
        feature_list,
        cut=f"(ll_m >= 200) & ({channel} == 1)",
        library="pd",
        step_size="200 MB",
    ):
        mem_available = psutil.virtual_memory().available / GB
        mem_total = psutil.virtual_memory().total / GB
        print(
            f"RAM usage {mem_available:.02f} / {mem_total:.02f} GB",
            end="\r",
            flush=True,
        )
        # physic para for pNN
        if "bkg" in sample_name:
            chunk_pd = chunk_pd.assign(m_truth=chunk_pd["ll_m"])
        elif "sig" in sample_name:
            chunk_pd = chunk_pd.assign(m_truth=sig_masses[sample_name])

        # add extra variables
        ll_y_list = list()
        jet_0_ll_delta_phi_list = list()
        jet_1_ll_delta_phi_list = list()
        jj_pt_list = list()
        jj_y_list = list()
        jj_ll_delta_phi_list = list()
        for row in chunk_pd.itertuples():
            lep_0 = ROOT.TLorentzVector()
            lep_1 = ROOT.TLorentzVector()
            jet_0 = ROOT.TLorentzVector()
            jet_1 = ROOT.TLorentzVector()
            if channel == "is_ee":
                lep_0.SetPtEtaPhiM(
                    row.lept_0_pt, row.lept_0_eta, row.lept_0_phi, ELECTRON_MASS,
                )
                lep_1.SetPtEtaPhiM(
                    row.lept_1_pt, row.lept_1_eta, row.lept_1_phi, ELECTRON_MASS,
                )
            elif channel == "is_mm":
                lep_0.SetPtEtaPhiM(
                    row.lept_0_pt, row.lept_0_eta, row.lept_0_phi, MUON_MASS,
                )
                lep_1.SetPtEtaPhiM(
                    row.lept_1_pt, row.lept_1_eta, row.lept_1_phi, MUON_MASS,
                )
            else:
                print(f"## Unknown channel {channel}")
                exit()
            jet_0.SetPtEtaPhiM(
                row.jet_0_pt, row.jet_0_eta, row.jet_0_phi, row.jet_0_m,
            )
            jet_1.SetPtEtaPhiM(
                row.jet_1_pt, row.jet_1_eta, row.jet_1_phi, row.jet_1_m,
            )
            ll = lep_0 + lep_1
            jj = jet_0 + jet_1
            ll_y = ll.Rapidity()
            jet_0_ll_delta_phi = jet_0.DeltaPhi(ll)
            jet_1_ll_delta_phi = jet_0.DeltaPhi(ll)
            jj_pt = jj.Pt()
            jj_y = jj.Rapidity()
            jj_ll_delta_phi = jj.DeltaPhi(ll)
            # append to list
            ll_y_list.append(ll_y)
            jet_0_ll_delta_phi_list.append(jet_0_ll_delta_phi)
            jet_1_ll_delta_phi_list.append(jet_1_ll_delta_phi)
            jj_pt_list.append(jj_pt)
            jj_y_list.append(jj_y)
            jj_ll_delta_phi_list.append(jj_ll_delta_phi)
        chunk_pd = chunk_pd.assign(ll_y=ll_y_list)
        chunk_pd = chunk_pd.assign(jet_0_ll_delta_phi=jet_0_ll_delta_phi_list)
        chunk_pd = chunk_pd.assign(jet_1_ll_delta_phi=jet_1_ll_delta_phi_list)
        chunk_pd = chunk_pd.assign(jj_pt=jj_pt_list)
        chunk_pd = chunk_pd.assign(jj_y=jj_y_list)
        chunk_pd = chunk_pd.assign(jj_ll_delta_phi=jj_ll_delta_phi_list)

        # convert float64 to float32
        f64_cols = chunk_pd.select_dtypes(include="float64").columns
        chunk_pd[f64_cols] = chunk_pd[f64_cols].astype("float32")

        # add tags
        chunk_pd = chunk_pd.assign(sample_name=sample_name)
        chunk_pd = chunk_pd.assign(camp=camp)
        chunk_pd = chunk_pd.assign(is_sig=is_sig)
        chunk_pd = chunk_pd.assign(is_mc=is_mc)
        # update df list
        sample_dfs.append(chunk_pd)
    sys.stdout.write("\033[K")
    return sample_dfs


## ee channel
print("## Processing ee channel")
ee_df_list = list()
ee_dir = df_dir / "ee" / cut_level
ee_dir.mkdir(parents=True, exist_ok=True)
### bkg
for bkg_name in bkg_ee_names:
    root_path = ntup_dir / cut_level / f"{bkg_name}.root"
    ee_df_list += process_sample(bkg_name, root_path, False, True, "is_ee", camp="run2")
### sig
for sig_name in sig_ee_names:
    root_path = ntup_dir / cut_level / f"{sig_name}.root"
    ee_df_list += process_sample(sig_name, root_path, True, True, "is_ee", camp="run2")
### dump
ee_df = pd.concat(ee_df_list, ignore_index=True)
del ee_df_list
save_path = ee_dir / "test.feather"
print(f"## Saving to {save_path}")
ee_df.to_feather(save_path)
del ee_df
