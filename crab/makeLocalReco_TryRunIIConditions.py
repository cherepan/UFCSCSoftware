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


#process.GlobalTag.globaltag = "124X_dataRun3_PromptAnalysis_v1"
process.GlobalTag.globaltag = "124X_mcRun3_2022_realistic_v12"


#process.GlobalTag.globaltag = "106X_upgrade2018_realistic_v15_L1v1"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
isSIMDIGI = bool(False)
isRAW = bool(True)
###################################################


process.options   = cms.untracked.PSet( SkipEvent = cms.untracked.vstring("ProductNotFound") )
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.source    = cms.Source("PoolSource",
                               noEventSort = cms.untracked.bool(True),
                               duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                               fileNames = cms.untracked.vstring(
#                                   'file:6513929e-95f2-4528-9b6b-6b0a15a768d4.root'
                                   #'/store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-RECO/PUForTRK_106X_upgrade2018_realistic_v11_L1v1-v2/50000/01A742E9-38B3-6448-8003-36BBB8F1E936.root'
#                                   '/store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-RECO/PUForTRK_106X_upgrade2018_realistic_v11_L1v1-v2/50000/01A742E9-38B3-6448-8003-36BBB8F1E936.root'
#                                   'file:/afs/cern.ch/work/c/cherepan/CSC/Synchronise_10_05/CSC_RU_Seg_Alog/CMSSW_10_6_20/src/UFCSCSoftware/crab/cms/store/mc/RunIISummer20UL18HLT/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/GEN-SIM-DIGI-RAW/PUForTRKv2_TRKv2_102X_upgrade2018_realistic_v15-v2/2530000/94390A02-4C99-A143-B721-BDB0A1C04C03.root'


#                                   '/store/data/Run2022C/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/356/381/00000/6513929e-95f2-4528-9b6b-6b0a15a768d4.root',
#                                   '/store/data/Run2022C/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/356/378/00000/c6e5cdb2-8369-46e9-8870-08bce43b26a7.root'

########################################## MC

#                                   'file:DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root'
                                   'file:ZMM_RAW_DIGI_SIM_RECO.root'
#                                   'file:012344ab-9b99-48c9-966a-7a6653cc6b69.root'

#                                   '/store/relval/CMSSW_12_4_13/RelValZMM_14/GEN-SIM-DIGI-RECO/124X_mcRun3_2022_realistic_v12_2021_FastSim-v1/2590000/8a48a70c-ddaf-4aa3-91b5-23dcac5a80a2.root'


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

process.csc2DRecHits.wireDigiTag  = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
process.csc2DRecHits.stripDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCStripDigi")



process.out = cms.OutputModule("PoolOutputModule",
                               fastCloning = cms.untracked.bool(False),
#                               fileName = cms.untracked.string('/eos/user/c/cherepan/CSC/UF_tuples/SingleMuon_RAW-RECO_ZMu-12Nov2019_UL2018_CSCSegmentBuilder_UF_testRun.root'),
#                               fileName = cms.untracked.string('RelValZMM_14_RU_CSCSegmentBuilder.root'),
                               fileName = cms.untracked.string('DY_MUMURelVal_UF_CSCSegmentBuilder.root'),
#                               fileName = cms.untracked.string('DYJetsToLL_M-50_RU_CSCSegmentBuilder.root'),
                               outputCommands = cms.untracked.vstring('keep *')
                               )


# --- TO ACTIVATE LogTrace IN CSCRecHitD NEED TO COMPILE IT WITH scram b -j8 USER_CXXFLAGS="-DEDM_ML_DEBUG"
# LogTrace output goes to cout; all other output to "junk.log"
 
from Configuration.DataProcessing.RecoTLR import customiseDataRun2Common

#call to customisation function customiseDataRun2Common imported from Configuration.DataProcessing.RecoTLR
process = customiseDataRun2Common(process)


process.load("FWCore.MessageLogger.MessageLogger_cfi")
# module label is something like "muonCSCDigis"...

process.MessageLogger.debugModules = cms.untracked.vstring("*")

#process.MessageLogger.debugModules = ["CSCRecHit", "CSCRecHitDBuilder","CSCMake2DRecHit","CSCHitFromStripOnly"]
process.MessageLogger.debugModules = [ "CSCRecHitDBuilder"]
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(5)
#process.MessageLogger.destinations = cms.untracked.vstring("cout","junk")
process.MessageLogger.cerr.threshold = "DEBUG"
process.MessageLogger.cerr.enable = True

process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string("DEBUG"),
    default   = cms.untracked.PSet( limit = cms.untracked.int32(1)  ),
    FwkReport = cms.untracked.PSet( limit = cms.untracked.int32(5) )
##    , CSCGeometry = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
#    , CSCRecHit = cms.untracked.PSet( limit = cms.untracked.int32(20) )
    , CSCRecHitDBuilder = cms.untracked.PSet( limit = cms.untracked.int32(20) )
#    , CSCMake2DRecHit = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
#    , CSCHitFromStripOnly = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
##    , CSCRecoConditions = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)




process.MessageLogger = cms.Service("MessageLogger",
     destinations  = cms.untracked.vstring(
                                             'detailedInfo'
                                               ,'critical'
                                               ,'cerr'
                    )
)


process.load("SimMuon.CSCDigitizer.muonCSCDigis_cfi")
# Path and EndPath def
process.unpack = cms.Path(process.muonCSCDigis * process.gtDigis)
process.reco = cms.Path(process.csc2DRecHits * process.cscSegments )




#process.reco = cms.Path(process.cscSegments )
#process.reco = cms.Path(process.reconstruction)
process.out_step = cms.EndPath(process.out)

# Schedule definition
process.schedule = cms.Schedule(process.reco, process.out_step)


if isSIMDIGI:
    process.reco.replace(process.csc2DRecHits, process.simMuonCSCDigis* process.gtDigis * process.csc2DRecHits * process.cscSegments )

if isRAW:
#    process.reco.replace(process.csc2DRecHits, process.muonCSCDigis * process.gtDigis * process.csc2DRecHits * process.cscSegments)
    process.reco.replace(process.csc2DRecHits, process.muonCSCDigis * process.gtDigis * process.csc2DRecHits * process.cscSegments)
