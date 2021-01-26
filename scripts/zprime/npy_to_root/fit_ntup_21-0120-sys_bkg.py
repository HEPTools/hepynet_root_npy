import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/21-0120-sys")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/21-0120-sys")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

camp = "run2"
bkg_keys = [
    # "bkg_ggZZ",
    "bkg_qcd",
]

branch_list = ["mz1", "mz2", "dnn_out", "weight"]
branch_list_wt = [
    "mz1",
    "mz2",
    "dnn_out",
    "weight",
    "weight_QCD_SCALE_UP_MZ1".lower(),
    "weight_QCD_SCALE_DOWN_MZ1".lower(),
    "weight_QCD_SCALE_UP_MZ2".lower(),
    "weight_QCD_SCALE_DOWN_MZ2".lower(),
    "weight_PDF_UP_MZ1".lower(),
    "weight_PDF_UP_MZ2".lower(),
    "weight_ALPHA_S_UP_MZ1".lower(),
    "weight_ALPHA_S_UP_MZ2".lower(),
]

bkg_ntuple_names = [
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


def generate_one_region(region):
    for variation in bkg_ntuple_names:
        print(f"Generating fit ntuples for {variation}")
        for sample_key in bkg_keys:
            dump_contents = []
            ntuple_path = ntup_save_dir.joinpath(
                f"{region}/{variation}/{camp}/{sample_key}.root"
            )
            ntuple_path.parent.mkdir(parents=True, exist_ok=True)
            if variation == "tree_NOMINAL":
                for branch in branch_list_wt:
                    array_path = input_array_dir.joinpath(
                        f"{region}/{variation}/{camp}/{sample_key}_{branch}.npy"
                    )
                    branch_content = np.load(array_path)
                    dump_contents.append(branch_content)
                dump_ntup_from_npy(
                    "ntup",
                    branch_list_wt,
                    "f",
                    dump_contents,
                    ntuple_path,
                )
            else:
                for branch in branch_list:
                    array_path = input_array_dir.joinpath(
                        f"{region}/{variation}/{camp}/{sample_key}_{branch}.npy"
                    )
                    branch_content = np.load(array_path)
                    dump_contents.append(branch_content)
                dump_ntup_from_npy(
                    "ntup",
                    branch_list,
                    "f",
                    dump_contents,
                    ntuple_path,
                )


for region in ["low_mass", "high_mass"]:
    generate_one_region(region)
