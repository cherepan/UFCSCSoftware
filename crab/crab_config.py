from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'CSCLocalReco_26_05_2023'
config.General.workArea =  'crab_area'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'makeLocalReco.py'

config.section_("Data")

config.Data.inputDataset = '/SingleMuon/Run2018B-ZMu-12Nov2019_UL2018-v2/RAW-RECO'
config.Data.inputDBS  = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.totalUnits  = 20
config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.publication = True
config.Data.outLFNDirBase = '/store/user/cherepan'
config.Data.outputDatasetTag = 'CSC_LocalReco_reProcess_UF_algo_Run2018B_ZMu_12Nov2019'

config.section_("Site")
#config.Site.whitelist = ['T2_US_Wisconsin','T2_US_Purdue','T1_US_FNAL']
#config.Data.ignoreLocality = True
config.Site.storageSite = 'T2_US_Florida'
