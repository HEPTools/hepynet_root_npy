# hepynet_root_npy

Handle transformation between Root and Numpy format for hepynet framework

## Environment

- use **Docker**:

  - just run the "**start_root**" script in the docker folder, it will pull image from docker hub if image doesn't exist locally

  - the data path should be specified in the start_root script according to user's platform

- manually setup:
  - **python3**: python3 is required, python 3.8+ is recommended
  - **ROOT**: see CERN ROOT website for installation instructions
  - **uproot**: pip install uproot=4.0.0 (uproot<4.0.0 will not work)

## Prepare the input arrays

Input ntuple must be flat, each input feature should have same quantities.
Besides, "weight" and "channel" array is needed.
If no "channel" branch is in the ntuple or there is only one channel, one should create the "dummy channel"
branch.

### Example code

```python
import logging
import numpy as np
from make_array import dump_flat_ntuple_individual, save_array
import pathlib

logging.getLogger().setLevel(logging.INFO)

# Constants
ntuple_name = "Emutau"
feature_list = ["M_ll", "ele_pt", "mu_pt", "emu", "weight"]
bkg_names = ["diboson", "zll", "top", "wjets"]
sig_names = ["rpv_500", "rpv_700", "rpv_1000", "rpv_1500", "rpv_2000"]

# Set path in docker
ntup_dir = "/data/lfv/ntuples/rel_103_v4/merged"
arrays_dir = "/data/lfv/arrays/rel_103_v4"
arrays_dir_path = pathlib.Path(arrays_dir)
if not arrays_dir_path.exists():
    arrays_dir_path.mkdir(parents=True, exist_ok=True)

for camp in ["mc16a", "mc16d", "mc16e"]:
    # Dump bkg
    for bkg_name in bkg_names:
        root_path = f"{ntup_dir}/{camp}/bkg_{bkg_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            ntuple_name,
            feature_list,
            f"{arrays_dir}/{camp}",
            f"bkg_{bkg_name}",
            use_lower_var_name=True,
        )
    # Dump sig
    for sig_name in sig_names:
        root_path = f"{ntup_dir}/{camp}/sig_{sig_name}.root"
        dump_flat_ntuple_individual(
            root_path,
            ntuple_name,
            feature_list,
            f"{arrays_dir}/{camp}",
            f"sig_{sig_name}",
            use_lower_var_name=True,
        )
    # Dump data
    root_path = f"{ntup_dir}/{camp}/data_all.root"
    dump_flat_ntuple_individual(
        root_path,
        ntuple_name,
        feature_list,
        f"arrays_dir/camp",
        "data_all",
        use_lower_var_name=True,
    )

```

### Example notes

- First import "**dump_flat_ntuple_individual**" and specify the **ntuple name** in
  root file, name **list of input features** and input **samples names** to be used
  later in arrays production.
- Specify the **input directory** where the ntuples root file were stores.
  If Docker is used, please change the path defined in docker image.
- Call "dump_flat_ntuple_individual" to dump arrays from ntuples. Note the
  arrays saving directory should be: **/array_save_dir/campaign/**

## Convert fit numpy arrays to ntuple

Need to generate numpy arrays for fitting in hepynet first

### Example code

```python
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

```
