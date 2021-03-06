import pathlib

import numpy as np

from array_to_ntuple import dump_ntup_from_npy

input_array_dir = pathlib.Path("/data/zprime/arrays_fit/21-0115-sys")
ntup_save_dir = pathlib.Path("/data/zprime/ntuples_fit/21-0115-sys")

ntup_save_dir.mkdir(parents=True, exist_ok=True)

bkg_keys = [
    # "bkg_ggZZ",
    "bkg_qcd",
]

branch_list = ["mz1", "mz2", "dnn_out", "weight"]
branch_list_wt = [
    "mz1",
    "mz2",
    "dnn_out",
    "weight",
    "weight_QCD_SCALE_UP_MZ1".lower(),
    "weight_QCD_SCALE_DOWN_MZ1".lower(),
    "weight_QCD_SCALE_UP_MZ2".lower(),
    "weight_QCD_SCALE_DOWN_MZ2".lower(),
    "weight_PDF_UP_MZ1".lower(),
    "weight_PDF_UP_MZ2".lower(),
    "weight_ALPHA_S_UP_MZ1".lower(),
    "weight_ALPHA_S_UP_MZ2".lower(),
]

bkg_ntuple_names = [
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

camp = "mc16d"

def generate_one_region(region):
    for variation in bkg_ntuple_names:
        print(f"Generating fit ntuples for {variation}")
        for sample_key in bkg_keys:
            dump_contents = []
            ntuple_path = ntup_save_dir.joinpath(
                f"{region}/{variation}/{camp}/{sample_key}.root"
            )
            ntuple_path.parent.mkdir(parents=True, exist_ok=True)
            if variation == "tree_NOMINAL":
                for branch in branch_list_wt:
                    array_path = input_array_dir.joinpath(
                        f"{region}/{variation}/{camp}/{sample_key}_{branch}.npy"
                    )
                    branch_content = np.load(array_path)
                    dump_contents.append(branch_content)
                dump_ntup_from_npy(
                    "ntup", branch_list_wt, "f", dump_contents, ntuple_path,
                )
            else:
                for branch in branch_list:
                    array_path = input_array_dir.joinpath(
                        f"{region}/{variation}/{camp}/{sample_key}_{branch}.npy"
                    )
                    branch_content = np.load(array_path)
                    dump_contents.append(branch_content)
                dump_ntup_from_npy(
                    "ntup", branch_list, "f", dump_contents, ntuple_path,
                )


for region in ["low_mass", "high_mass"]:
    generate_one_region(region)
