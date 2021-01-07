import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/1220-sys")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/1220-sys")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

bkg_keys = [
    # "bkg_ggZZ",
    "bkg_qcd",
]

branch_list = [
    "mz1",
    "mz2",
    "dnn_out",
    "weight_QCD_SCALE_UP_MZ1".lower(),
    "weight_QCD_SCALE_DOWN_MZ1".lower(),
    "weight_QCD_SCALE_UP_MZ2".lower(),
    "weight_QCD_SCALE_DOWN_MZ2".lower(),
]


# get bkg ntuples
variation = "tree_NOMINAL"
print(f"Generating fit ntuples for {variation}")
for sample_key in bkg_keys:
    dump_contents = []
    for branch in branch_list:
        array_path = input_array_dir.joinpath(f"{variation}/mc16d/{sample_key}_{branch}.npy")
        branch_content = np.load(array_path)
        dump_contents.append(branch_content)

    ntuple_path = ntup_save_dir.joinpath(f"{variation}/mc16d/{sample_key}.root")
    ntuple_path.parent.mkdir(parents=True, exist_ok=True)
    dump_ntup_from_npy(
        "ntup", branch_list, "f", dump_contents, ntuple_path,
    )
