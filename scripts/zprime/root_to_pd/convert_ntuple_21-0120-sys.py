from logging import root
import pathlib
import sys

import pandas as pd
import psutil
import uproot

MB = 1024 * 1024
GB = MB * 1024

# setups
cut_level = "mva_2jet"
ntup_dir = pathlib.Path(f"/data/zprime/ntuples/21-0120-sys")
df_dir = pathlib.Path(f"/data/zprime/data_frames/21-0120-sys")
df_dir.mkdir(parents=True, exist_ok=True)


feature_list = [
    "PtL1",
    "PtL2",
    "PtL3",
    "PtL4",
    "EtaL1",
    "EtaL2",
    "EtaL3",
    "EtaL4",
    "MZ1",
    "MZ2",
    "PtZ1",
    "PtZ2",
    "MZZ",
    "PtZZ",
    "EtaZZ",
    "DeltaRl12",
    "DeltaRl34",
    "dEtal12",
    "dEtal34",
    "nJet",
    "EtaZ1",
    "EtaZ2",
    "run",
    "event",
    "quadtype",
    "weightr",
]

feature_list_final = [f.lower() for f in feature_list]
feature_list_final[-1] = "weight"

bkg_names = {
    "bkg_qcd": "364250_QCD",
    "bkg_ggZZ": "ggZZ",
}

sig_names_low = {
    "sig_Zp005": "502547_2muZp005",
    "sig_Zp007": "502548_2muZp007",
    "sig_Zp009": "502549_2muZp009",
    "sig_Zp011": "502550_2muZp011",
    "sig_Zp013": "502551_2muZp013",
    "sig_Zp015": "502552_2muZp015",
    "sig_Zp017": "502553_2muZp017",
    "sig_Zp019": "502554_2muZp019",
    "sig_Zp023": "502555_2muZp023",
    "sig_Zp027": "502556_2muZp027",
    "sig_Zp031": "502557_2muZp031",
    "sig_Zp035": "502558_2muZp035",
    "sig_Zp039": "502559_2muZp039",
}

sig_names_high = {
    "sig_Zp042": "502560_2muZp042",
    "sig_Zp045": "502561_2muZp045",
    "sig_Zp048": "502562_2muZp048",
    "sig_Zp051": "502563_2muZp051",
    "sig_Zp054": "502564_2muZp054",
    "sig_Zp057": "502565_2muZp057",
    "sig_Zp060": "502566_2muZp060",
    "sig_Zp063": "502567_2muZp063",
    "sig_Zp066": "502568_2muZp066",
    "sig_Zp069": "502569_2muZp069",
    "sig_Zp072": "502570_2muZp072",
    "sig_Zp075": "502571_2muZp075",
}

sig_masses = {
    "sig_Zp005": 5,
    "sig_Zp007": 7,
    "sig_Zp009": 9,
    "sig_Zp011": 11,
    "sig_Zp013": 13,
    "sig_Zp015": 15,
    "sig_Zp017": 17,
    "sig_Zp019": 19,
    "sig_Zp023": 23,
    "sig_Zp027": 27,
    "sig_Zp031": 31,
    "sig_Zp035": 35,
    "sig_Zp039": 39,
    "sig_Zp042": 42,
    "sig_Zp045": 45,
    "sig_Zp048": 48,
    "sig_Zp051": 51,
    "sig_Zp054": 54,
    "sig_Zp057": 57,
    "sig_Zp060": 60,
    "sig_Zp063": 63,
    "sig_Zp066": 66,
    "sig_Zp069": 69,
    "sig_Zp072": 72,
    "sig_Zp075": 75,
}

# convert to pandas DataFrame
def process_sample(sample_name, sample_path, is_sig, is_mc, m_truth_name):
    print(f"Processing: {sample_name}")
    sample_dfs = list()
    for chunk_pd in uproot.iterate(
        f"{sample_path}:tree_NOMINAL",
        feature_list,
        cut=f"quadtype == 2",
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
        # use lower case for features' names
        chunk_pd.columns = feature_list_final
        # physic para for pNN
        if "bkg" in sample_name:
            chunk_pd = chunk_pd.assign(m_truth=chunk_pd[m_truth_name])
        elif "sig" in sample_name:
            chunk_pd = chunk_pd.assign(m_truth=sig_masses[sample_name])
        # additional_parameters
        mz1_mz2 = chunk_pd["mz1"].values - chunk_pd["mz2"].values
        chunk_pd["mz1_mz2"] = mz1_mz2
        # convert float64 to float32
        f64_cols = chunk_pd.select_dtypes(include="float64").columns
        chunk_pd[f64_cols] = chunk_pd[f64_cols].astype("float32")
        # add tags
        chunk_pd = chunk_pd.assign(sample_name=sample_name)
        chunk_pd = chunk_pd.assign(camp=None)
        chunk_pd = chunk_pd.assign(is_sig=is_sig)
        chunk_pd = chunk_pd.assign(is_mc=is_mc)
        # update df list
        sample_dfs.append(chunk_pd)
    sys.stdout.write("\033[K")
    return sample_dfs


# low mass region
print("## Processing low mass region")
low_df_list = list()
low_dir = df_dir / "low_mass"
low_dir.mkdir(parents=True, exist_ok=True)
## bkg
for bkg_name, bkg_file in bkg_names.items():
    root_path = ntup_dir / f"tree_{bkg_file}.root"
    low_df_list += process_sample(bkg_name, root_path, False, True, "mz2")
## sig
for sig_name, sig_file in sig_names_low.items():
    root_path = ntup_dir / f"tree_{sig_file}.root"
    low_df_list += process_sample(sig_name, root_path, True, True, "mz2")
## dump
low_df: pd.DataFrame = pd.concat(low_df_list, ignore_index=True)
del low_df_list
save_path = low_dir / "zprime_low_m_quadtype_2.feather"
print(f"## Saving to {save_path}")
low_df.to_feather(save_path)
del low_df

# high mass region
print("## Processing high mass region")
high_df_list = list()
high_dir = df_dir / "high_mass"
high_dir.mkdir(parents=True, exist_ok=True)
## bkg
for bkg_name, bkg_file in bkg_names.items():
    root_path = ntup_dir / f"tree_{bkg_file}.root"
    high_df_list += process_sample(bkg_name, root_path, False, True, "mz1")
## sig
for sig_name, sig_file in sig_names_high.items():
    root_path = ntup_dir / f"tree_{sig_file}.root"
    high_df_list += process_sample(sig_name, root_path, True, True, "mz1")
## dump
high_df: pd.DataFrame = pd.concat(high_df_list, ignore_index=True)
del high_df_list
save_path = high_dir / "zprime_high_m_quadtype_2.feather"
print(f"## Saving to {save_path}")
high_df.to_feather(save_path)
del high_df

