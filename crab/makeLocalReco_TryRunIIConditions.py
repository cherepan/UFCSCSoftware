## Dump  10  events in CSC rechit builder - Tim Cox - 07.11.2012
## This version runs in 6_0_1_PostLS1 on a simulated data DIGI sample.

import FWCore.ParameterSet.Config as cms

process = cms.Process("reRECO")

process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.EndOfProcess_cff")
process.load('Configuration.StandardSequences.Services_cff')

##################################################
# --- MATCH GT TO RELEASE AND DATA SAMPLE
#process.GlobalTag.globaltag = "POSTLS161_V11::All"
#process.GlobalTag.globaltag = "106X_dataRun2_v32"
process.GlobalTag.globaltag = "124X_dataRun3_PromptAnalysis_v1"
#process.GlobalTag.globaltag = "106X_upgrade2018_realistic_v15_L1v1"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )
isSIMDIGI = bool(True)
isRAW = bool(True)
###################################################


process.options   = cms.untracked.PSet( SkipEvent = cms.untracked.vstring("ProductNotFound") )
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.source    = cms.Source("PoolSource",
                               noEventSort = cms.untracked.bool(True),
                               duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                               fileNames = cms.untracked.vstring(
                                   #'/store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-RECO/PUForTRK_106X_upgrade2018_realistic_v11_L1v1-v2/50000/01A742E9-38B3-6448-8003-36BBB8F1E936.root'
#                                   '/store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-RECO/PUForTRK_106X_upgrade2018_realistic_v11_L1v1-v2/50000/01A742E9-38B3-6448-8003-36BBB8F1E936.root'
#                                   'file:/afs/cern.ch/work/c/cherepan/CSC/Synchronise_10_05/CSC_RU_Seg_Alog/CMSSW_10_6_20/src/UFCSCSoftware/crab/cms/store/mc/RunIISummer20UL18HLT/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-DIGI-RAW/PUForTRKv2_TRKv2_102X_upgrade2018_realistic_v15-v2/2530000/94390A02-4C99-A143-B721-BDB0A1C04C03.root'
                                   '/store/data/Run2022C/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/356/381/00000/6513929e-95f2-4528-9b6b-6b0a15a768d4.root',
                                   '/store/data/Run2022C/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/356/378/00000/c6e5cdb2-8369-46e9-8870-08bce43b26a7.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/240000/128783F5-CD11-AB49-9CAA-222EC8F82BA9.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/240000/49A33288-9925-FF43-AED3-C1F3BD2FD640.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/5FE6A215-7096-6B41-B499-D12FE193A89B.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/A0AE2F0B-740C-B646-BF3B-58EE0943A261.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/7E66C6C3-7AEB-C048-8450-58BBD7E70343.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/2ACDF7AC-B65B-BB4C-915F-A0AF22098386.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/4C8FFD75-6243-8A4E-848E-ED14C0F8B9B2.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/F427E364-B84C-FA4D-9C5F-B1DF11176D71.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/7FD2532C-A050-DE47-B3CC-5D9FECA2312D.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/CC95D6CA-A6FE-D14B-98BF-77307ACFBCEE.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/A46A6EAF-311C-E248-8B44-FB8F13FDB3D5.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/D5A55C35-CF1A-664C-855C-0317C6F518A8.root',
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/CA91E075-380C-2142-B047-0D214F6822B6.root'
#                                   '/store/data/Run2018B/SingleMuon/RAW-RECO/ZMu-12Nov2019_UL2018-v2/270003/5DC4A3AC-206C-CC4A-9FBB-7080182ECDDD.root'

#'file:./RelValJpsiMM_GEN-SIM-DIGI-RAW-HLTDEBUG_PRE_ST62_V8-v1/7412617A-E2E0-E211-8DB9-003048FEADCC.root',
#'file:./RelValJpsiMM_GEN-SIM-DIGI-RAW-HLTDEBUG_PRE_ST62_V8-v1/F0558878-E4E0-E211-8D59-02163E007A13.root'
#'file:/cms/data/store/mc/Summer13dr53X/DYToMuMu_M_20_TuneZ2star_13TeV-pythia6/GEN-SIM-RAW/PU25bx25_START53_V19D-v1/20000/BAB7C472-6ADF-E211-8702-20CF3027A5E9.root'




    )
)

# ME1/1A is  u n g a n g e d  Post-LS1
process.CSCGeometryESModule.useGangedStripsInME1a = True
##process.CSCGeometryESModule.debugV = True
##process.idealForDigiCSCGeometry.useGangedStripsInME1a = False

# Turn off some flags for CSCRecHitD that are turned ON in default config
process.csc2DRecHits.readBadChannels = cms.bool(False)
process.csc2DRecHits.readBadChannels = cms.bool(False)
process.csc2DRecHits.CSCUseTimingCorrections = cms.bool(False)
process.cscSegments.CSCUseTimingCorrections = cms.bool(False)
#process.csc2DRecHits.CSCUseTimingCorrections = cms.bool(False)
#process.csc2DRecHits.CSCUseGasGainCorrection = cms.bool(False)



# Switch input for CSCRecHitD to  s i m u l a t e d  digis  # i assume it is for MC only
#process.csc2DRecHits.wireDigiTag  = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
#process.csc2DRecHits.stripDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCStripDigi")


process.out = cms.OutputModule("PoolOutputModule",
                               fastCloning = cms.untracked.bool(False),
#                               fileName = cms.untracked.string('/eos/user/c/cherepan/CSC/UF_tuples/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF_testRun.root'),
                               fileName = cms.untracked.string('SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_RU_CSCSegmentBuilder.root'),
#                               fileName = cms.untracked.string('DYJetsToLL_M-50_RU_CSCSegmentBuilder.root'),
                               outputCommands = cms.untracked.vstring('keep *')
                               )


# --- TO ACTIVATE LogTrace IN CSCRecHitD NEED TO COMPILE IT WITH scram b -j8 USER_CXXFLAGS="-DEDM_ML_DEBUG"
# LogTrace output goes to cout; all other output to "junk.log"
 
from Configuration.DataProcessing.RecoTLR import customiseDataRun2Common

#call to customisation function customiseDataRun2Common imported from Configuration.DataProcessing.RecoTLR
process = customiseDataRun2Common(process)


process.load("FWCore.MessageLogger.MessageLogger_cfi")
##process.MessageLogger.categories.append("CSCGeometry")
#process.MessageLogger.categories.append("CSCRecHit")
#process.MessageLogger.categories.append("CSCRecHitDBuilder")
#process.MessageLogger.categories.append("CSCMake2DRecHit")
#process.MessageLogger.categories.append("CSCHitFromStripOnly")
## process.MessageLogger.categories.append("CSCRecoConditions")

# module label is something like "muonCSCDigis"...

#process.MessageLogger.debugModules = cms.untracked.vstring("*")

process.MessageLogger.debugModules = ["CSCRecHit", "CSCRecHitDBuilder","CSCMake2DRecHit","CSCHitFromStripOnly"]
#process.MessageLogger.destinations = cms.untracked.vstring("cout","junk")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)




process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string("DEBUG"),
    default   = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    FwkReport = cms.untracked.PSet( limit = cms.untracked.int32(3) )
##    , CSCGeometry = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
    , CSCRecHit = cms.untracked.PSet( limit = cms.untracked.int32(1) )
    , CSCRecHitDBuilder = cms.untracked.PSet( limit = cms.untracked.int32(1) )
    , CSCMake2DRecHit = cms.untracked.PSet( limit = cms.untracked.int32(1) )
    , CSCHitFromStripOnly = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
##    , CSCRecoConditions = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)



# Path and EndPath def
process.unpack = cms.Path(process.muonCSCDigis * process.gtDigis)
process.reco = cms.Path(process.csc2DRecHits * process.cscSegments )
#process.reco = cms.Path(process.cscSegments )
#process.reco = cms.Path(process.reconstruction)
process.out_step = cms.EndPath(process.out)

# Schedule definition
process.schedule = cms.Schedule(process.reco, process.out_step)

if isRAW:
    process.reco.replace(process.csc2DRecHits,process.muonCSCDigis * process.gtDigis * process.csc2DRecHits * process.cscSegments)
