import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/21-0120-sys")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/21-0120-sys")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

camp = "run2"
sig_keys_low = [
    "sig_Zp005",
    "sig_Zp007",
    "sig_Zp009",
    "sig_Zp011",
    "sig_Zp013",
    "sig_Zp015",
    "sig_Zp017",
    "sig_Zp019",
    "sig_Zp023",
    "sig_Zp027",
    "sig_Zp031",
    "sig_Zp035",
    "sig_Zp039",
]

sig_keys_high = [
    "sig_Zp042",
    "sig_Zp045",
    "sig_Zp048",
    "sig_Zp051",
    "sig_Zp054",
    "sig_Zp057",
    "sig_Zp060",
    "sig_Zp063",
    "sig_Zp066",
    "sig_Zp069",
    "sig_Zp072",
    "sig_Zp075",
]

branch_list = ["mz1", "mz2", "dnn_out", "weight"]
branch_list_wt_low = ["mz1", "mz2", "dnn_out", "weight"]
branch_list_wt_high = ["mz1", "mz2", "dnn_out", "weight"]


sig_ntuple_names = [
    "tree_NOMINAL",
    "tree_FT_EFF_B_systematics__1down",
    "tree_FT_EFF_B_systematics__1up",
    "tree_FT_EFF_C_systematics__1down",
    "tree_FT_EFF_C_systematics__1up",
    "tree_FT_EFF_Light_systematics__1down",
    "tree_FT_EFF_Light_systematics__1up",
    "tree_FT_EFF_extrapolation__1down",
    "tree_FT_EFF_extrapolation__1up",
    "tree_FT_EFF_extrapolation_from_charm__1down",
    "tree_FT_EFF_extrapolation_from_charm__1up",
    "tree_MUON_EFF_ISO_STAT__1down",
    "tree_MUON_EFF_ISO_STAT__1up",
    "tree_MUON_EFF_ISO_SYS__1down",
    "tree_MUON_EFF_ISO_SYS__1up",
    "tree_MUON_EFF_RECO_STAT__1down",
    "tree_MUON_EFF_RECO_STAT__1up",
    "tree_MUON_EFF_RECO_STAT_LOWPT__1down",
    "tree_MUON_EFF_RECO_STAT_LOWPT__1up",
    "tree_MUON_EFF_RECO_SYS__1down",
    "tree_MUON_EFF_RECO_SYS__1up",
    "tree_MUON_EFF_RECO_SYS_LOWPT__1down",
    "tree_MUON_EFF_RECO_SYS_LOWPT__1up",
    "tree_MUON_EFF_TTVA_STAT__1down",
    "tree_MUON_EFF_TTVA_STAT__1up",
    "tree_MUON_EFF_TTVA_SYS__1down",
    "tree_MUON_EFF_TTVA_SYS__1up",
    "tree_MUON_ID__1down",
    "tree_MUON_ID__1up",
    "tree_MUON_MS__1down",
    "tree_MUON_MS__1up",
    "tree_MUON_SAGITTA_RESBIAS__1down",
    "tree_MUON_SAGITTA_RESBIAS__1up",
    "tree_MUON_SAGITTA_RHO__1down",
    "tree_MUON_SAGITTA_RHO__1up",
    "tree_MUON_SCALE__1down",
    "tree_MUON_SCALE__1up",
    "tree_PRW_DATASF__1down",
    "tree_PRW_DATASF__1up",
]

# get bkg ntuples
for variation in sig_ntuple_names:
    # for variation in ["tree_NOMINAL"]:
    # low mass
    print(f"Generating fit ntuples for {variation}")
    for sample_key in sig_keys_low:
        dump_contents = []
        ntuple_path = ntup_save_dir.joinpath(
            f"low_mass/{variation}/{camp}/{sample_key}.root"
        )
        ntuple_path.parent.mkdir(parents=True, exist_ok=True)
        if variation == "tree_NOMINAL":
            for branch in branch_list_wt_low:
                array_path = input_array_dir.joinpath(
                    f"low_mass/{variation}/{camp}/{sample_key}_{branch}.npy"
                )
                branch_content = np.load(array_path)
                dump_contents.append(branch_content)
            dump_ntup_from_npy(
                "ntup", branch_list_wt_low, "f", dump_contents, ntuple_path
            )
        else:
            for branch in branch_list:
                array_path = input_array_dir.joinpath(
                    f"low_mass/{variation}/{camp}/{sample_key}_{branch}.npy"
                )
                branch_content = np.load(array_path)
                dump_contents.append(branch_content)
            dump_ntup_from_npy("ntup", branch_list, "f", dump_contents, ntuple_path)

    # high_mass
    print(f"Generating fit ntuples for {variation}")
    for sample_key in sig_keys_high:
        dump_contents = []
        ntuple_path = ntup_save_dir.joinpath(
            f"high_mass/{variation}/{camp}/{sample_key}.root"
        )
        ntuple_path.parent.mkdir(parents=True, exist_ok=True)
        if variation == "tree_NOMINAL":
            for branch in branch_list_wt_high:
                array_path = input_array_dir.joinpath(
                    f"high_mass/{variation}/{camp}/{sample_key}_{branch}.npy"
                )
                branch_content = np.load(array_path)
                dump_contents.append(branch_content)
            dump_ntup_from_npy(
                "ntup", branch_list_wt_high, "f", dump_contents, ntuple_path
            )
        else:
            for branch in branch_list:
                array_path = input_array_dir.joinpath(
                    f"high_mass/{variation}/{camp}/{sample_key}_{branch}.npy"
                )
                branch_content = np.load(array_path)
                dump_contents.append(branch_content)
            dump_ntup_from_npy("ntup", branch_list, "f", dump_contents, ntuple_path)
