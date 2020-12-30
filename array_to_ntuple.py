import array
import logging
import pathlib

import ROOT
import uproot


def dump_ntup_from_npy(ntup_name, branch_list, branch_type, contents, out_path):
    """Generates ntuples from numpy arrays."""
    out_path = pathlib.Path(out_path)
    out_dir = pathlib.Path(out_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = ROOT.TFile(out_path.as_posix(), "RECREATE")
    out_file.cd()
    out_ntuple = ROOT.TNtuple(ntup_name, ntup_name, ":".join(branch_list))
    n_branch = len(branch_list)
    n_entries = len(contents[0])
    for i in range(n_entries):
        fill_values = []
        for j in range(n_branch):
            fill_values.append(contents[j][i])
        out_ntuple.Fill(array.array(branch_type, fill_values))
    out_file.cd()
    out_ntuple.Write()
