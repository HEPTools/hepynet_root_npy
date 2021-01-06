import os
import logging
import numpy as np
from ntuple_to_array import dump_flat_ntuple_individual, save_array

logging.getLogger().setLevel(logging.INFO)

# Constants
release_name = "1220-sys"
ntuple_names = [
    "tree_NOMINAL",
    "tree_EG_RESOLUTION_ALL__1down",
    "tree_EG_RESOLUTION_ALL__1up",
    "tree_EG_SCALE_AF2__1down",
    "tree_EG_SCALE_AF2__1up",
    "tree_EG_SCALE_ALL__1down",
    "tree_EG_SCALE_ALL__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP0__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP0__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP1__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP1__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP10__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP10__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP11__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP11__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP12__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP12__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP13__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP13__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP14__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP14__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP15__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP15__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP2__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP2__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP3__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP3__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP4__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP4__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP5__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP5__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP6__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP6__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP7__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP7__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP8__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP8__1up",
    "tree_EL_EFF_ID_CorrUncertaintyNP9__1down",
    "tree_EL_EFF_ID_CorrUncertaintyNP9__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP0__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP0__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP1__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP1__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP10__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP10__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP11__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP11__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP12__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP12__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP13__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP13__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP14__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP14__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP15__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP15__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP16__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP16__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP17__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP17__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP2__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP2__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP3__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP3__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP4__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP4__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP5__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP5__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP6__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP6__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP7__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP7__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP8__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP8__1up",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP9__1down",
    "tree_EL_EFF_ID_SIMPLIFIED_UncorrUncertaintyNP9__1up",
    "tree_EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down",
    "tree_EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up",
    "tree_EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down",
    "tree_EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up",
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
    "tree_JET_BJES_Response__1up",
    "tree_JET_BJES_Response__1down",
    "tree_JET_EffectiveNP_Detector1__1up",
    "tree_JET_EffectiveNP_Detector1__1down",
    "tree_JET_EffectiveNP_Detector2__1up",
    "tree_JET_EffectiveNP_Detector2__1down",
    "tree_JET_EffectiveNP_Mixed1__1up",
    "tree_JET_EffectiveNP_Mixed1__1down",
    "tree_JET_EffectiveNP_Mixed2__1up",
    "tree_JET_EffectiveNP_Mixed2__1down",
    "tree_JET_EffectiveNP_Mixed3__1up",
    "tree_JET_EffectiveNP_Mixed3__1down",
    "tree_JET_EffectiveNP_Modelling1__1up",
    "tree_JET_EffectiveNP_Modelling1__1down",
    "tree_JET_EffectiveNP_Modelling2__1up",
    "tree_JET_EffectiveNP_Modelling2__1down",
    "tree_JET_EffectiveNP_Modelling3__1up",
    "tree_JET_EffectiveNP_Modelling3__1down",
    "tree_JET_EffectiveNP_Modelling4__1up",
    "tree_JET_EffectiveNP_Modelling4__1down",
    "tree_JET_EffectiveNP_Statistical1__1up",
    "tree_JET_EffectiveNP_Statistical1__1down",
    "tree_JET_EffectiveNP_Statistical2__1up",
    "tree_JET_EffectiveNP_Statistical2__1down",
    "tree_JET_EffectiveNP_Statistical3__1up",
    "tree_JET_EffectiveNP_Statistical3__1down",
    "tree_JET_EffectiveNP_Statistical4__1up",
    "tree_JET_EffectiveNP_Statistical4__1down",
    "tree_JET_EffectiveNP_Statistical5__1up",
    "tree_JET_EffectiveNP_Statistical5__1down",
    "tree_JET_EffectiveNP_Statistical6__1up",
    "tree_JET_EffectiveNP_Statistical6__1down",
    "tree_JET_EtaIntercalibration_Modelling__1up",
    "tree_JET_EtaIntercalibration_Modelling__1down",
    "tree_JET_EtaIntercalibration_NonClosure_2018data__1up",
    "tree_JET_EtaIntercalibration_NonClosure_2018data__1down",
    "tree_JET_EtaIntercalibration_NonClosure_highE__1up",
    "tree_JET_EtaIntercalibration_NonClosure_highE__1down",
    "tree_JET_EtaIntercalibration_NonClosure_negEta__1up",
    "tree_JET_EtaIntercalibration_NonClosure_negEta__1down",
    "tree_JET_EtaIntercalibration_NonClosure_posEta__1up",
    "tree_JET_EtaIntercalibration_NonClosure_posEta__1down",
    "tree_JET_EtaIntercalibration_TotalStat__1up",
    "tree_JET_EtaIntercalibration_TotalStat__1down",
    "tree_JET_Flavor_Composition__1up",
    "tree_JET_Flavor_Composition__1down",
    "tree_JET_Flavor_Response__1up",
    "tree_JET_Flavor_Response__1down",
    "tree_JET_JER_DataVsMC_MC16__1up",
    "tree_JET_JER_DataVsMC_MC16__1down",
    "tree_JET_JER_EffectiveNP_1__1up",
    "tree_JET_JER_EffectiveNP_1__1down",
    "tree_JET_JER_EffectiveNP_2__1up",
    "tree_JET_JER_EffectiveNP_2__1down",
    "tree_JET_JER_EffectiveNP_3__1up",
    "tree_JET_JER_EffectiveNP_3__1down",
    "tree_JET_JER_EffectiveNP_4__1up",
    "tree_JET_JER_EffectiveNP_4__1down",
    "tree_JET_JER_EffectiveNP_5__1up",
    "tree_JET_JER_EffectiveNP_5__1down",
    "tree_JET_JER_EffectiveNP_6__1up",
    "tree_JET_JER_EffectiveNP_6__1down",
    "tree_JET_JER_EffectiveNP_7restTerm__1up",
    "tree_JET_JER_EffectiveNP_7restTerm__1down",
    "tree_JET_JvtEfficiency__1down",
    "tree_JET_JvtEfficiency__1up",
    "tree_JET_Pileup_OffsetMu__1up",
    "tree_JET_Pileup_OffsetMu__1down",
    "tree_JET_Pileup_OffsetNPV__1up",
    "tree_JET_Pileup_OffsetNPV__1down",
    "tree_JET_Pileup_PtTerm__1up",
    "tree_JET_Pileup_PtTerm__1down",
    "tree_JET_Pileup_RhoTopology__1up",
    "tree_JET_Pileup_RhoTopology__1down",
    "tree_JET_PunchThrough_MC16__1up",
    "tree_JET_PunchThrough_MC16__1down",
    "tree_JET_SingleParticle_HighPt__1up",
    "tree_JET_SingleParticle_HighPt__1down",
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
    # "ggZZ": "ggZZ",
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
ntup_dir = f"/data/zprime/ntuples/{release_name}"
arrays_dir = f"/data/zprime/arrays/{release_name}"
if not os.path.exists(arrays_dir):
    os.makedirs(arrays_dir)

# for camp in ["mc16a", "mc16d", "mc16e"]:
for camp in ["mc16d"]:
    for ntuple_name in ntuple_names:
        # Dump bkg
        for index, bkg_key in enumerate(bkg_names):
            root_path = f"{ntup_dir}/{camp}/tree_{bkg_names[bkg_key]}.root"
            save_dir_sub = f"{arrays_dir}/{ntuple_name}/{camp}"
            dump_flat_ntuple_individual(
                root_path,
                ntuple_name,
                feature_list,
                save_dir_sub,
                f"bkg_{bkg_key}",
                use_lower_var_name=True,
            )
            mz1 = np.load(f"{save_dir_sub}/bkg_{bkg_key}_mz1.npy")
            mz2 = np.load(f"{save_dir_sub}/bkg_{bkg_key}_mz2.npy")
            mz1_mz2 = mz1 - mz2
            save_array(mz1_mz2, save_dir_sub, f"bkg_{bkg_key}_mz1_mz2")
            # parameterized feature
            save_array(mz1, save_dir_sub, f"bkg_{bkg_key}_mz1_p")
            # parameterized feature
            save_array(mz2, save_dir_sub, f"bkg_{bkg_key}_mz2_p")
            dummy_channel = np.ones(len(mz1))
            save_array(dummy_channel, save_dir_sub, f"bkg_{bkg_key}_dummy_channel")
            normed_weight = np.load(f"{save_dir_sub}/bkg_{bkg_key}_weightr.npy")
            save_array(normed_weight, save_dir_sub, f"bkg_{bkg_key}_weight")

        # Dump sig
        """
        for index, sig_key in enumerate(sig_names):
            root_path = ntup_dir + "/" + camp + \
                "/tree_{}.root".format(sig_names[sig_key])

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
                mz1 = np.load(arrays_dir + "/" + camp +
                            "/sig_{}_mz1.npy".format(sig_key))
                arr_len = len(mz1)
                # deal with missing etazz
                etal1 = np.load(arrays_dir + "/" + camp +
                                "/sig_{}_etal1.npy".format(sig_key))
                etal2 = np.load(arrays_dir + "/" + camp +
                                "/sig_{}_etal2.npy".format(sig_key))
                etal3 = np.load(arrays_dir + "/" + camp +
                                "/sig_{}_etal3.npy".format(sig_key))
                etal4 = np.load(arrays_dir + "/" + camp +
                                "/sig_{}_etal4.npy".format(sig_key))
                etazz = etal1 + etal2 + etal3 + etal4
                save_array(etazz, arrays_dir + "/" + camp,
                        "sig_{}_etazz".format(sig_key))
            else:
                dump_flat_ntuple_individual(
                    root_path,
                    ntuple_name,
                    feature_list,
                    arrays_dir + "/" + camp,
                    "sig_{}".format(sig_key),
                    use_lower_var_name=True,
                )
            mz1 = np.load(arrays_dir + "/" + camp +
                        "/sig_{}_mz1.npy".format(sig_key))
            mz2 = np.load(arrays_dir + "/" + camp +
                        "/sig_{}_mz2.npy".format(sig_key))
            mz1_mz2 = mz1 - mz2
            save_array(mz1_mz2, arrays_dir + "/" + camp,
                    "sig_{}_mz1_mz2".format(sig_key))

            # prepare parameterized feature
            truth_mass = sig_masses[sig_key]
            if truth_mass < 42:
                mz2_p = np.repeat(truth_mass, len(mz2))
                save_array(mz2_p, arrays_dir + "/" + camp +
                        "/", "sig_{}_mz2_p".format(sig_key))
            else:
                mz1_p = np.repeat(truth_mass, len(mz1))
                save_array(mz1_p, arrays_dir + "/" + camp +
                        "/", "sig_{}_mz1_p".format(sig_key))

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
                normed_weight, arrays_dir + "/" +
                camp, "sig_{}_weight".format(sig_key)
            )
        """

