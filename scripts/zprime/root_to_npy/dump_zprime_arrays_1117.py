import os
import  logging
import numpy as np
from ntuple_to_array import dump_flat_ntuple_individual, save_array

logging.getLogger().setLevel(logging.INFO)

# Constants
release_name = "1117"
ntuple_name = "tree_NOMINAL"
feature_list = [
    "PtL1",
    "PtL2",
    "PtL3",
    "PtL4",
    "EtaL1",
    "EtaL2",
    "EtaL3",
    "EtaL4",
    "MZ1",
    "MZ2",
    "PtZ1",
    "PtZ2",
    "MZZ",
    "PtZZ",
    "EtaZZ",
    "DeltaRl12",
    "DeltaRl34",
    "dEtal12",
    "dEtal34",
    "nJet",
    "EtaZ1",
    "EtaZ2",
    "run",
    "event",
    "quadtype",
    "weight",
    "weightr",
]

bkg_names = {
    "qcd": "364250_QCD",
    "ggZZ": "ggZZ",
}
sig_names = {
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
sig_masses = {
    "Zp005": 5,
    "Zp007": 7,
    "Zp009": 9,
    "Zp011": 11,
    "Zp013": 13,
    "Zp015": 15,
    "Zp017": 17,
    "Zp019": 19,
    "Zp023": 23,
    "Zp027": 27,
    "Zp031": 31,
    "Zp035": 35,
    "Zp039": 39,
    "Zp042": 42,
    "Zp045": 45,
    "Zp048": 48,
    "Zp051": 51,
    "Zp054": 54,
    "Zp057": 57,
    "Zp060": 60,
    "Zp063": 63,
    "Zp066": 66,
    "Zp069": 69,
    "Zp072": 72,
    "Zp075": 75,
}

# Set path in docker
ntup_dir = "/data/zprime/ntuples/{}".format(release_name)
arrays_dir = "/data/zprime/arrays/{}".format(release_name)
if not os.path.exists(arrays_dir):
    os.makedirs(arrays_dir)

for camp in ["mc16a", "mc16d", "mc16e"]:
    # Dump bkg
    for index, bkg_key in enumerate(bkg_names):
        root_path = ntup_dir + "/" + camp + "/tree_{}.root".format(bkg_names[bkg_key])
        dump_flat_ntuple_individual(
            root_path,
            ntuple_name,
            feature_list,
            arrays_dir + "/" + camp,
            "bkg_{}".format(bkg_key),
            use_lower_var_name=True,
        )
        mz1 = np.load(arrays_dir + "/" + camp + "/bkg_{}_mz1.npy".format(bkg_key))
        mz2 = np.load(arrays_dir + "/" + camp + "/bkg_{}_mz2.npy".format(bkg_key))
        mz1_mz2 = mz1 - mz2
        save_array(mz1_mz2, arrays_dir + "/" + camp + "/", "bkg_{}_mz1_mz2".format(bkg_key))
        save_array(
            mz1, arrays_dir + "/" + camp + "/", "bkg_{}_mz1_p".format(bkg_key)
        )  # parameterized feature
        save_array(
            mz2, arrays_dir + "/" + camp + "/", "bkg_{}_mz2_p".format(bkg_key)
        )  # parameterized feature
        dummy_channel = np.ones(len(mz1))
        save_array(dummy_channel, arrays_dir + "/" + camp, "bkg_{}_dummy_channel".format(bkg_key))
        normed_weight = np.load(arrays_dir + "/" + camp + "/bkg_{}_weightr.npy".format(bkg_key))
        save_array(normed_weight, arrays_dir + "/" + camp, "/bkg_{}_weight".format(bkg_key))

    # Dump sig
    for index, sig_key in enumerate(sig_names):
        root_path = ntup_dir + "/" + camp + "/tree_{}.root".format(sig_names[sig_key])

        if sig_key == "Zp063" and camp == "mc16a":
            feature_list_tmp = feature_list[:]
            feature_list_tmp.remove("EtaZZ")
            print(f"m16a Zp063 feature_list: {feature_list}")
            print(f"m16a Zp063 feature_list: {feature_list_tmp}")
            dump_flat_ntuple_individual(
                root_path,
                ntuple_name,
                feature_list_tmp,
                arrays_dir + "/" + camp,
                "sig_{}".format(sig_key),
                use_lower_var_name=True,
            )
            mz1 = np.load(arrays_dir + "/" + camp + "/sig_{}_mz1.npy".format(sig_key))
            arr_len = len(mz1)
            # deal with missing etazz
            etal1 = np.load(arrays_dir + "/" + camp + "/sig_{}_etal1.npy".format(sig_key))
            etal2 = np.load(arrays_dir + "/" + camp + "/sig_{}_etal2.npy".format(sig_key))
            etal3 = np.load(arrays_dir + "/" + camp + "/sig_{}_etal3.npy".format(sig_key))
            etal4 = np.load(arrays_dir + "/" + camp + "/sig_{}_etal4.npy".format(sig_key))
            etazz = etal1 + etal2 + etal3 + etal4
            save_array(etazz, arrays_dir + "/" + camp, "sig_{}_etazz".format(sig_key))
        else:
            dump_flat_ntuple_individual(
                root_path,
                ntuple_name,
                feature_list,
                arrays_dir + "/" + camp,
                "sig_{}".format(sig_key),
                use_lower_var_name=True,
            )
        mz1 = np.load(arrays_dir + "/" + camp + "/sig_{}_mz1.npy".format(sig_key))
        mz2 = np.load(arrays_dir + "/" + camp + "/sig_{}_mz2.npy".format(sig_key))
        mz1_mz2 = mz1 - mz2
        save_array(mz1_mz2, arrays_dir + "/" + camp, "sig_{}_mz1_mz2".format(sig_key))

        # prepare parameterized feature
        truth_mass = sig_masses[sig_key]
        if truth_mass < 42:
            mz2_p = np.repeat(truth_mass, len(mz2))
            save_array(mz2_p, arrays_dir + "/" + camp + "/", "sig_{}_mz2_p".format(sig_key))
        else:
            mz1_p = np.repeat(truth_mass, len(mz1))
            save_array(mz1_p, arrays_dir + "/" + camp + "/", "sig_{}_mz1_p".format(sig_key))

        dummy_channel = np.ones(len(mz1))
        save_array(
            dummy_channel,
            arrays_dir + "/" + camp,
            "sig_{}_dummy_channel".format(sig_key),
        )
        normed_weight = np.load(
            arrays_dir + "/" + camp + "/sig_{}_weightr.npy".format(sig_key)
        )
        save_array(
            normed_weight, arrays_dir + "/" + camp, "/sig_{}_weight".format(sig_key)
        )
