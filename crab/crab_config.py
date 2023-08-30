from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'RAW2DIGI_L1Reco_RECO_RECOSIM_v3'
config.General.workArea =  'crab_area_v3'
config.General.transferLogs = True


config.section_("JobType")
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ProduceReco_v2_py_RAW2DIGI_L1Reco_RECO_RECOSIM.py'
config.JobType.maxMemoryMB      = 8000
config.JobType.maxJobRuntimeMin = 2750
config.JobType.numCores = 4

config.section_("Data")

config.Data.inputDataset = '/RelValZMM_PU_13p6/CMSSW_12_4_12-PU_124X_mcRun3_2022_realistic_postEE_forPixelIneff_v5_PDMVRELVALS188_HS_2023PU-v1/GEN-SIM-DIGI-RAW'
config.Data.inputDBS  = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits  = 60
#config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.publication = True
config.Data.outLFNDirBase = '/store/user/cherepan'
config.Data.outputDatasetTag = 'RelValZMM_14_CMSSW_12_4_0RAW2DIGI_L1Reco_RECO_RECOSIM_v3'


config.section_("Site")
##config.Site.whitelist = ['T2_US_Wisconsin','T2_US_Purdue','T1_US_FNAL']
##config.Data.ignoreLocality = True
#config.Site.storageSite = 'T2_US_Florida'
config.Site.whitelist = ['T2_US_Florida','T2_US_Wisconsin','T2_US_Purdue','T1_US_FNAL']
config.Data.ignoreLocality = True
config.Site.storageSite = 'T2_US_Florida'

