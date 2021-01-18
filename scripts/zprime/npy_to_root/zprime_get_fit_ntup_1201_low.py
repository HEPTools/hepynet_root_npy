import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/fit_ntup_1201_low/run2")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/1201_stats/low_mass/run2")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

sample_keys = [
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
    "bkg_ggZZ",
    "bkg_qcd",
]

branch_list = ["mz1", "mz2", "dnn_out", "weight"]

# get ntuples
for sample_key in sample_keys:

    print("generating:", sample_key)

    dump_contents = []
    for branch in branch_list:
        array_path = input_array_dir.joinpath(f"{sample_key}_{branch}.npy")
        branch_content = np.load(array_path)
        dump_contents.append(branch_content)

    ntuple_path = ntup_save_dir.joinpath(f"{sample_key}.root")
    print("path:", ntuple_path)
    dump_ntup_from_npy(
        "ntup", branch_list, "f", dump_contents, ntuple_path,
    )
