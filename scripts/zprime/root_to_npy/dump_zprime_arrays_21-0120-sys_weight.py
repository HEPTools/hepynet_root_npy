import os
import logging
import numpy as np
from ntuple_to_array import dump_flat_ntuple_individual, save_array

logging.getLogger().setLevel(logging.INFO)

# Constants
release_name = "21-0120-sys"

sig_feature_list_low = {}

sig_feature_list_high = {}

bkg_feature_list = {
    "weight_QCD_SCALE_UP_MZ1",
    "weight_QCD_SCALE_DOWN_MZ1",
    "weight_QCD_SCALE_UP_MZ2",
    "weight_QCD_SCALE_DOWN_MZ2",
    "weight_PDF_UP_MZ1",
    "weight_PDF_UP_MZ2",
    "weight_ALPHA_S_UP_MZ1",
    "weight_ALPHA_S_UP_MZ2",
}

bkg_names = {
    "qcd": "364250_QCD",
    # "ggZZ": "ggZZ",
}
sig_names_low = {
    "Zp005": "502547_2muZp005",
    "Zp007": "502548_2muZp007",
    "Zp009": "502549_2muZp009",
    "Zp011": "502550_2muZp011",
    "Zp013": "502551_2muZp013",
    "Zp015": "502552_2muZp015",
    "Zp017": "502553_2muZp017",
    "Zp019": "502554_2muZp019",
    "Zp023": "502555_2muZp023",
    "Zp027": "502556_2muZp027",
    "Zp031": "502557_2muZp031",
    "Zp035": "502558_2muZp035",
    "Zp039": "502559_2muZp039",
}
sig_names_high = {
    "Zp042": "502560_2muZp042",
    "Zp045": "502561_2muZp045",
    "Zp048": "502562_2muZp048",
    "Zp051": "502563_2muZp051",
    "Zp054": "502564_2muZp054",
    "Zp057": "502565_2muZp057",
    "Zp060": "502566_2muZp060",
    "Zp063": "502567_2muZp063",
    "Zp066": "502568_2muZp066",
    "Zp069": "502569_2muZp069",
    "Zp072": "502570_2muZp072",
    "Zp075": "502571_2muZp075",
}


# Set path in docker
ntup_dir = f"/data/zprime/ntuples/{release_name}"
arrays_fit_dir = f"/data/zprime/arrays_fit/{release_name}"
if not os.path.exists(arrays_fit_dir):
    os.makedirs(arrays_fit_dir)

# Dump bkg
for camp in ["run2"]:
    ntuple_name = "tree_NOMINAL"
    for index, bkg_key in enumerate(bkg_names):
        root_path = f"{ntup_dir}/{camp}/tree_{bkg_names[bkg_key]}.root"
        save_dir_sub = f"{arrays_fit_dir}/low_mass/{ntuple_name}/{camp}"
        dump_flat_ntuple_individual(
            root_path,
            ntuple_name,
            bkg_feature_list,
            save_dir_sub,
            f"bkg_{bkg_key}",
            use_lower_var_name=True,
        )
        save_dir_sub = f"{arrays_fit_dir}/high_mass/{ntuple_name}/{camp}"
        dump_flat_ntuple_individual(
            root_path,
            ntuple_name,
            bkg_feature_list,
            save_dir_sub,
            f"bkg_{bkg_key}",
            use_lower_var_name=True,
        )

# Dump sig
# for camp in ["run2"]:
#     ntuple_name = "tree_NOMINAL"
#     # low mass
#     for index, sig_key in enumerate(sig_names_low):
#         root_path = f"{ntup_dir}/{camp}/tree_{sig_names_low[sig_key]}.root"
#         save_dir_sub = f"{arrays_fit_dir}/low_mass/{ntuple_name}/{camp}"
#         dump_flat_ntuple_individual(
#             root_path,
#             ntuple_name,
#             sig_feature_list_low,
#             save_dir_sub,
#             f"sig_{sig_key}",
#             use_lower_var_name=True,
#         )
#     # high mass
#     for index, sig_key in enumerate(sig_names_high):
#         root_path = f"{ntup_dir}/{camp}/tree_{sig_names_high[sig_key]}.root"
#         save_dir_sub = f"{arrays_fit_dir}/high_mass/{ntuple_name}/{camp}"
#         dump_flat_ntuple_individual(
#             root_path,
#             ntuple_name,
#             sig_feature_list_high,
#             save_dir_sub,
#             f"sig_{sig_key}",
#             use_lower_var_name=True,
#         )
