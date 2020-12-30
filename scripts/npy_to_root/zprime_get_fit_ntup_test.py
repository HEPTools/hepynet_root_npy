import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/all-mass-test/run2")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/all-mass-test/run2")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

sample_keys = [
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
    "bkg_ggZZ",
    "bkg_qcd",
]

branch_list = ["mz1", "dnn_out", "weight"]

# get ntuples
for sample_key in sample_keys:

    dump_contents = []
    for branch in branch_list:
        array_path = input_array_dir.joinpath(f"{sample_key}_{branch}.npy")
        branch_content = np.load(array_path)
        dump_contents.append(branch_content)

    ntuple_path = ntup_save_dir.joinpath(f"{sample_key}.root")
    dump_ntup_from_npy(
        "ntup", branch_list, "f", dump_contents, ntuple_path,
    )
