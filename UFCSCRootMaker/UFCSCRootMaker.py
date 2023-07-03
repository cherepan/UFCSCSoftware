######################################################################
#                                                                    #
# This version works with CMSSW_6_2_X                                #
#                                                                    #
######################################################################
import FWCore.ParameterSet.Config as cms
doUnpacking = bool(True)

########## Options ############
isDATA = bool(False)
isRAW = bool(True)
isDIGI = bool(True)

isSIM = bool(True)
isGEN = bool(True)

isLocalRECO = bool(True)
isFullRECO = bool(True)

addMuonInfo = bool(True)
addTrackInfo = bool(False)
addRecHitInfo = bool(True)
addSegmentInfo = bool(True)
addTriggerInfo = bool(True)

addDigiInfo = bool(True)

addTimeMonitoringInfo = bool(True)
addCalibrationInfo = bool(False)

maxEvents = -1

MCGlobalTag='124X_mcRun3_2022_realistic_v12' #for DYmumu_PU140
#DataGlobalTag='76X_dataRun2_v19'
#DataGlobalTag='76X_dataRun2_v15'
#DataGlobalTag='92X_dataRun2_Prompt_v11'
#DataGlobalTag='106X_dataRun2_v32'
DataGlobalTag='124X_dataRun3_PromptAnalysis_v1'




doDebug = bool(False)
###############################

### Debug Printing ###

#if not isDATA:
#    print 'Sample Type: MC'
#else:
#    print "Sample Type: Data"
                



#####################
process = cms.Process("UFCSCRootMaker")

process.Timing = cms.Service("Timing",
                             summaryOnly = cms.untracked.bool(True)
                             )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxEvents))

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.MessageLogger.cerr.threshold = 'ERROR' # Options: INFO, WARNING, ERROR
process.MessageLogger.cerr.FwkReport.reportEvery = -1
#process.MessageLogger.destinations = ['cout', 'cerr']
#process.MessageLogger.suppressWarning.append('classByHitsGlb') # kill stupid RPC hit associator warning

#process.MessageLogger.cerr.FwkJob.limit=1
#process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(1))
                                                       
######################### Frontier Conditions #########################
# Conditions data for calibration and alignment                       #
# are defined in the Offline Conditions Database (ORCOF),             #
# which is read in CMSSW applications via Frontier caching servers.   #
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions  #
#######################################################################
#process.load('Configuration.StandardSequences.Services_cff')
#process.load('Configuration.StandardSequences.Geometry_cff')
#process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.EventContent.EventContent_cff')
###

process.load("CondCore.CondDB.CondDB_cfi")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
###
if not isDATA:
    process.GlobalTag.globaltag=MCGlobalTag 
    
else:
    process.GlobalTag.globaltag=DataGlobalTag


process.out = cms.OutputModule("PoolOutputModule",
                               #fileName = cms.untracked.string('test.root'),
                               # save only events passing the full path
                               outputCommands = cms.untracked.vstring('drop *')
                               )


process.TFileService = cms.Service("TFileService",
#                                   fileName = cms.string("DUMMYFILENAME.root")
#                                   fileName = cms.string("CSC_UF_ntuple_UF_SegmentBuilder.root")
#                                   fileName = cms.string("run3_MC_test_UF.root")
                                   fileName = cms.string("run3_MC_RU.root")

#                                   fileName = cms.string("test/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF_testRun.root")
                                   )

# Primary Vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter("VertexSelector",
                                                  src = cms.InputTag('offlinePrimaryVertices'),
                                                  cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'),
                                                  filter = cms.bool(True)
                                                  )


process.source = cms.Source ("PoolSource",
                             # Disable duplicate event check mode because the run and event -numbers
                             # are incorrect in current Madgraph samples (Dec 16, 2008)
                             # processingMode = cms.untracked.string('RunsAndLumis'),
                             duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                             fileNames = cms.untracked.vstring(),      
                             )

if isDATA:
    process.source.fileNames = cms.untracked.vstring(
#        'file:/eos/user/c/cherepan/HeavyFiles/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF.root'
#        'file:test/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF_testRun.root'
#         'file:/eos/user/c/cherepan/CSC/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF_testRun.root'
#        'file:/afs/cern.ch/work/c/cherepan/CSC/Run3/UFSegementBuilder/CMSSW_12_4_4/src/UFCSCSoftware/crab/DY_MUMURelVal_RU_CSCSegmentBuilder.root'
        'file:../crab/DY_MUMURelVal_RU_CSCSegmentBuilder.root'

#        '/store/data/Run2022C/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/356/381/00000/6513929e-95f2-4528-9b6b-6b0a15a768d4.root'


#        'file:test/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF.root'
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/5FE6A215-7096-6B41-B499-D12FE193A89B.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/A0AE2F0B-740C-B646-BF3B-58EE0943A261.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/7E66C6C3-7AEB-C048-8450-58BBD7E70343.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/2ACDF7AC-B65B-BB4C-915F-A0AF22098386.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/4C8FFD75-6243-8A4E-848E-ED14C0F8B9B2.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/F427E364-B84C-FA4D-9C5F-B1DF11176D71.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/7FD2532C-A050-DE47-B3CC-5D9FECA2312D.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/CC95D6CA-A6FE-D14B-98BF-77307ACFBCEE.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/A46A6EAF-311C-E248-8B44-FB8F13FDB3D5.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/D5A55C35-CF1A-664C-855C-0317C6F518A8.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/CA91E075-380C-2142-B047-0D214F6822B6.root',
#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/5DC4A3AC-206C-CC4A-9FBB-7080182ECDDD.root'

#        'file:001D83E9-4350-6648-89D2-155101834DEF.root'


#        '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/100000/001D83E9-4350-6648-89D2-155101834DEF.root'
#        'file:../../../../../UFCSCSoftware/UFCSCRootMaker/Zmu_rawreco_2016H.root'
# 'root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-16Dec2015-v1/10000/005D37B2-3CA9-E511-B9AF-001E67398223.root',
# 'root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-16Dec2015-v1/10000/005D37B2-3CA9-E511-B9AF-001E67398223.root',
# 'root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-16Dec2015-v1/10000/005D37B2-3CA9-E511-B9AF-001E67398223.root',
# 'root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-16Dec2015-v1/10000/005D37B2-3CA9-E511-B9AF-001E67398223.root',
# 'root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-16Dec2015-v1/10000/005D37B2-3CA9-E511-B9AF-001E67398223.root',
#'root://cmsxrootd.fnal.gov//store/data/Run2016F/SingleMuon/RECO/PromptReco-v1/000/277/981/00000/0075B7D0-6659-E611-8EB7-02163E012008.root'
#'root://cmsxrootd.fnal.gov//store/data/Run2016B/SingleMuon/RECO/PromptReco-v2/000/273/150/00000/1C609FC2-D919-E611-ACFB-02163E011C02.root'
#'file:/raid/raid8/mhl/CSC_Run2/CMSSW_dev/outputRoot/test2.root'
#'file://00E68DCF-E3B2-E711-910F-48FD8EE73A03.root'
#'file:/raid/raid8/mhl/CSC_Run2/CMSSW_dev/inputRoot/0014C2C5-92BA-E711-ADD1-008CFAFBE8F2.root'

)
else:
    process.source.fileNames = cms.untracked.vstring(
#        '/store/relval/CMSSW_12_4_13/RelValZMM_14/GEN-SIM-DIGI-RECO/124X_mcRun3_2022_realistic_v12_2021_FastSim-v1/2590000/8a48a70c-ddaf-4aa3-91b5-23dcac5a80a2.root'
        'file:../crab/DY_MUMURelVal_UF_CSCSegmentBuilder.root'
#        'file:../8a48a70c-ddaf-4aa3-91b5-23dcac5a80a2.root'
#        '/store/relval/CMSSW_7_0_0/RelValTTbar/GEN-SIM-DIGI-RECO/START70_V6_FastSim-v2/00000/00743452-B498-E311-AD84-02163E00EAC9.root',
#        'file:/raid/raid8/mhl/CSC_Run2/CMSSW_dev/outputRoot/test2.root'
#        'root://cmsxrootd.fnal.gov//store/group/upgrade/muon/ME0GlobalReco/ME0MuonReRun_DY_SLHC23patch1_SegmentReRunFullRun_ForPublish/M-20_TuneZ2star_14TeV_6_2_0_SLHC23patch1_2023/DYToMuMu_M-20_TuneZ2star_14TeV-pythia6-tauola/DYToMuMu_M-20_TuneZ2star_14TeV-pythia6-tauola_2023SHCalNoTaper_PU140_Selectors_RECO/b52ce42d5986c94dc336f39e015d825e/output_100_2_p9i.root'
    )
    
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True)
                                     #,SkipEvent = cms.untracked.vstring('ProductNotFound')
                                     )

### Physics Declared Filter (for data)
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

### No scraping
process.noscraping = cms.EDFilter("FilterOutScraping",
                                  applyfilter = cms.untracked.bool(True),
                                  debugOn = cms.untracked.bool(doDebug),
                                  numtrack = cms.untracked.uint32(10),
                                  thresh = cms.untracked.double(0.2)
                                  )


#process.LumiCorrectionSource = cms.ESSource("LumiCorrectionSource",
                                            #authpath=cms.untracked.string('/afs/cern.ch'file:/cms/lumi/DB'),
                                            #connect=cms.string('oracle:/'file:/cms_orcon_adg'file:/cms_lumi_prod')
#                                            connect=cms.string('frontier://LumiCalc_LUMI_PROD')
                                            #normtag=cms.untracked.string('HFV2a')
                                            #datatag=cms.untracked.string('v3')
#                                            )


# HB + HE noise filtering
#process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')
#process.HBHENoiseFilter.minIsolatedNoiseSumE        = 999999.
#process.HBHENoiseFilter.minNumIsolatedNoiseChannels = 999999
#process.HBHENoiseFilter.minIsolatedNoiseSumEt       = 999999.

#EventCount                                                                                                                             
process.nEventsTotal = cms.EDProducer("EventCountProducer")

#RM
process.load("UFCSCSoftware.UFCSCRootMaker.cscRootMaker_cfi")
process.cscRootMaker.isFullRECO = cms.untracked.bool(isFullRECO)
process.cscRootMaker.isLocalRECO = cms.untracked.bool(isLocalRECO)
process.cscRootMaker.isGEN = cms.untracked.bool(isGEN)
process.cscRootMaker.isSIM = cms.untracked.bool(isSIM)
process.cscRootMaker.isRAW = cms.untracked.bool(isRAW)
process.cscRootMaker.isDIGI = cms.untracked.bool(isDIGI)
process.cscRootMaker.isDATA = cms.untracked.bool(isDATA)
process.cscRootMaker.addMuons = cms.untracked.bool(addMuonInfo)
process.cscRootMaker.addTracks = cms.untracked.bool(addTrackInfo)
process.cscRootMaker.addRecHits = cms.untracked.bool(addRecHitInfo)
process.cscRootMaker.addSegments = cms.untracked.bool(addSegmentInfo)
process.cscRootMaker.addTrigger = cms.untracked.bool(addTriggerInfo)
process.cscRootMaker.addDigis = cms.untracked.bool(addDigiInfo)
process.cscRootMaker.addTimeMonitoring = cms.untracked.bool(addTimeMonitoringInfo)
process.cscRootMaker.addCalibrations = cms.untracked.bool(addCalibrationInfo)

process.unpack = cms.Sequence(process.muonCSCDigis*process.gtDigis)

process.p = cms.Path(
    process.nEventsTotal
#    *process.goodOfflinePrimaryVertices
#    *process.noscraping
    *process.cscRootMaker
    )

if not isDATA:
#    process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")
 #   process.totalKinematicsFilter.tolerance=5.0
    process.p.replace(process.nEventsTotal,process.nEventsTotal)
#    process.p.replace(process.nEventsTotal,process.nEventsTotal*process.totalKinematicsFilter)

if isDATA:
#    process.load("CondCore.CondDB.CondDB_cfi")
#    process.p.replace(process.nEventsTotal,process.hltPhysicsDeclared*process.nEventsTotal)
    process.p.replace(process.nEventsTotal,process.nEventsTotal)

if doUnpacking:
    process.p.replace(process.nEventsTotal,process.unpack*process.nEventsTotal)

