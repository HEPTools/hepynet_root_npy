import io
import logging
import os
import pathlib

import numpy as np
import uproot


def dump_flat_ntuple_individual(
    root_path: str,
    ntuple_name: str,
    variable_list: list,
    save_dir: str,
    save_pre_fix: str,
    use_lower_var_name: bool = False,
    channel_feature: str = None,
) -> None:
    """Reads numpy array from ROOT ntuple and convert to numpy array.

    Note:
        Each branch will be saved as an individual file.

    """
    try:
        events = uproot.open(f"{root_path}:{ntuple_name}")
    except:
        raise IOError("Can not get ntuple")
    logging.info(f"Read arrays from: {root_path}")
    if channel_feature is not None:
        cut_index = np.argwhere(events[channel_feature].array(library="np") == 1)
    else:
        cut_index = None
    for var in variable_list:
        if use_lower_var_name:
            file_name = save_pre_fix + "_" + var.lower()
        else:
            file_name = save_pre_fix + "_" + var
        logging.info(f"Generating: {file_name}")
        temp_arr = events[var].array(library="np")
        if cut_index is not None:
            temp_arr = temp_arr[cut_index]
        save_array(temp_arr, save_dir, file_name)


def save_array(npy_array, directory_path, file_name, dump_empty=False):
    """Saves numpy data as .npy file

    Args:
        array: numpy array, array to be saved
        directory_path: str, directory path to save the file
        file_name: str, file name used by .npy file

    """
    save_dir = pathlib.Path(directory_path)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir.joinpath(f"{file_name}.npy")
    if npy_array.size == 0:
        if dump_empty:
            logging.warn("Empty array detected! Will save empty array as specified.")
        else:
            logging.warn("Empty array detected!")
    with io.open(save_path, "wb") as f:
        np.save(f, npy_array)
