import pathlib
import sys
from typing import Iterable

import numpy as np
import pandas as pd
import psutil
import uproot

MB = 1024 * 1024
GB = MB * 1024

test_file = pathlib.Path("/data/lfv/test/test.root")

for i, chunk_pd in enumerate(
    uproot.iterate(
        f"{test_file}:nominal",
        ["emuSelection", "mu_pt", "mu_eta", "el_pt", "tau_pt"],
        library="ak",
        step_size=10,
    )
):
    # for index, row in chunk_pd.iterrows():
    #    print(row)
    # exit()
    for line in chunk_pd:
        print(line)
    exit()
