import logging
import pathlib

import numpy as np
from ntuple_to_array import dump_flat_ntuple_individual, save_array

logging.getLogger().setLevel(logging.INFO)

version_name = "V03"
tree_name = "ntup"
ntup_dir = pathlib.Path(f"/data/ZXll/ntuples/{version_name}")
arrays_dir = pathlib.Path(f"/data/ZXll/arrays/{version_name}")
arrays_dir.mkdir(parents=True, exist_ok=True)

feature_list = [
    # "is_ee",
    # "is_mm",
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

bkg_names = {
    "diboson": "bkg_diboson",
    "top": "bkg_top",
    "W": "bkg_W",
    "Zee": "bkg_Zee",
    "Zmumu": "bkg_Zmumu",
    "Ztautau": "bkg_Ztautau",
}

sig_ee_names = {
    "HVTee_m0250": "sig_HVTee_m0250",
    "HVTee_m0300": "sig_HVTee_m0300",
    "HVTee_m0350": "sig_HVTee_m0350",
    "HVTee_m0500": "sig_HVTee_m0500",
    "HVTee_m0700": "sig_HVTee_m0700",
    "HVTee_m1000": "sig_HVTee_m1000",
    "HVTee_m1500": "sig_HVTee_m1500",
    "HVTee_m2000": "sig_HVTee_m2000",
    "HVTee_m2500": "sig_HVTee_m2500",
    "HVTee_m3000": "sig_HVTee_m3000",
    "HVTee_m3500": "sig_HVTee_m3500",
    "HVTee_m4000": "sig_HVTee_m4000",
    "HVTee_m4500": "sig_HVTee_m4500",
    "HVTee_m5000": "sig_HVTee_m5000",
    "HVTee_m6000": "sig_HVTee_m6000",
}

sig_mm_names = {
    "HVTmumu_m0250": "sig_HVTmumu_m0250",
    "HVTmumu_m0300": "sig_HVTmumu_m0300",
    "HVTmumu_m0350": "sig_HVTmumu_m0350",
    "HVTmumu_m0500": "sig_HVTmumu_m0500",
    "HVTmumu_m0700": "sig_HVTmumu_m0700",
    "HVTmumu_m1000": "sig_HVTmumu_m1000",
    "HVTmumu_m1500": "sig_HVTmumu_m1500",
    "HVTmumu_m2000": "sig_HVTmumu_m2000",
    "HVTmumu_m2500": "sig_HVTmumu_m2500",
    "HVTmumu_m3000": "sig_HVTmumu_m3000",
    "HVTmumu_m3500": "sig_HVTmumu_m3500",
    "HVTmumu_m4000": "sig_HVTmumu_m4000",
    "HVTmumu_m4500": "sig_HVTmumu_m4500",
    "HVTmumu_m5000": "sig_HVTmumu_m5000",
    "HVTmumu_m6000": "sig_HVTmumu_m6000",
}

sig_masses = {
    "HVTee_m0250": 250,
    "HVTee_m0300": 300,
    "HVTee_m0350": 350,
    "HVTee_m0500": 500,
    "HVTee_m0700": 700,
    "HVTee_m1000": 1000,
    "HVTee_m1500": 1500,
    "HVTee_m2000": 2000,
    "HVTee_m2500": 2500,
    "HVTee_m3000": 3000,
    "HVTee_m3500": 3500,
    "HVTee_m4000": 4000,
    "HVTee_m4500": 4500,
    "HVTee_m5000": 5000,
    "HVTee_m6000": 6000,
    "HVTmumu_m0250": 250,
    "HVTmumu_m0300": 300,
    "HVTmumu_m0350": 350,
    "HVTmumu_m0500": 500,
    "HVTmumu_m0700": 700,
    "HVTmumu_m1000": 1000,
    "HVTmumu_m1500": 1500,
    "HVTmumu_m2000": 2000,
    "HVTmumu_m2500": 2500,
    "HVTmumu_m3000": 3000,
    "HVTmumu_m3500": 3500,
    "HVTmumu_m4000": 4000,
    "HVTmumu_m4500": 4500,
    "HVTmumu_m5000": 5000,
    "HVTmumu_m6000": 6000,
}

#for cut_level in ["mva_2jet", "mva_2jet_timing"]:
for cut_level in ["mva_2jet"]:
    # dump bkg

    # ee channel
    ee_dir = arrays_dir / "ee" / cut_level
    ee_dir.mkdir(parents=True, exist_ok=True)
    for bkg_key, bkg_name in bkg_names.items():
        root_path = ntup_dir / cut_level / f"{bkg_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            tree_name,
            feature_list,
            ee_dir,
            bkg_name,
            use_lower_var_name=True,
            channel_feature="is_ee",
        )
        m_ll = np.load(ee_dir / f"{bkg_name}_ll_m.npy")
        # save m_truth
        save_array(m_ll, ee_dir, f"{bkg_name}_m_truth")
    # mm channel
    mm_dir = arrays_dir / "mm" / cut_level
    mm_dir.mkdir(parents=True, exist_ok=True)
    for bkg_key, bkg_name in bkg_names.items():
        root_path = ntup_dir / cut_level / f"{bkg_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            tree_name,
            feature_list,
            mm_dir,
            bkg_name,
            use_lower_var_name=True,
            channel_feature="is_mm",
        )
        m_ll = np.load(mm_dir / f"{bkg_name}_ll_m.npy")
        # save m_truth
        save_array(m_ll, mm_dir, f"{bkg_name}_m_truth")

    # dump sig

    # ee channel
    ee_dir = arrays_dir / "ee" / cut_level
    ee_dir.mkdir(parents=True, exist_ok=True)
    for sig_key, sig_name in sig_ee_names.items():
        root_path = ntup_dir / cut_level / f"{sig_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            tree_name,
            feature_list,
            ee_dir,
            sig_name,
            use_lower_var_name=True,
            channel_feature="is_ee",
        )
        m_ll = np.load(ee_dir / f"{sig_name}_ll_m.npy")
        truth_mass = sig_masses[sig_key]
        m_p = np.repeat(truth_mass, len(m_ll))
        save_array(m_p, ee_dir, f"{sig_name}_m_truth")

    # mm channel
    mm_dir = arrays_dir / "mm" / cut_level
    mm_dir.mkdir(parents=True, exist_ok=True)
    for sig_key, sig_name in sig_mm_names.items():
        root_path = ntup_dir / cut_level / f"{sig_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            tree_name,
            feature_list,
            mm_dir,
            sig_name,
            use_lower_var_name=True,
            channel_feature="is_mm",
        )
        m_ll = np.load(mm_dir / f"{sig_name}_ll_m.npy")
        truth_mass = sig_masses[sig_key]
        m_p = np.repeat(truth_mass, len(m_ll))
        save_array(m_p, mm_dir, f"{sig_name}_m_truth")
