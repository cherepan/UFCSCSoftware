# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: ProduceReco_v2.py --filein file:012344ab-9b99-48c9-966a-7a6653cc6b69.root --fileout test.root --step RAW2DIGI,L1Reco,RECO,RECOSIM --no_exec --conditions=124X_mcRun3_2022_realistic_v12 --mc --eventcontent FEVTDEBUGHLT --era Run3 --datatier GEN-SIM-DIGI-RAW -n 25
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('RECO',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.RecoSim_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring(#'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/521d9fbb-3406-4776-b7b2-73111ab5cc4d.root',
                                        #'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/2d110ec3-6485-408b-9e84-88da547c043c.root',
                                        #'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/4c01d2e8-4608-464f-a3a9-14d74ae22ca4.root',
                                        #'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/012344ab-9b99-48c9-966a-7a6653cc6b69.root',
                                        #'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/71810ecf-3ff3-4813-959f-c4a6b5793d5d.root',
                                        #'file:/eos/user/c/cherepan/CSC/ZMM_RAW_DIGI_ZMMRealVal/85afe352-54a2-4757-8d54-c57a89f37a9c.root'
#                                        '/store/relval/CMSSW_12_4_12/RelValZMM_PU_13p6/GEN-SIM-DIGI-RAW/PU_124X_mcRun3_2022_realistic_postEE_forPixelIneff_v5_PDMVRELVALS188_HS_2023PU-v1/00000/021f0888-0985-47ef-ae3a-891cbac30449.root'
                                        '/store/relval/CMSSW_12_4_14_patch2/RelValSingleMuPt10/GEN-SIM-DIGI-RAW/PU_124X_mcRun3_2022_realistic_v12_RV205-v1/2580000/0bb6ebca-c622-452f-a6ca-2d4838b1ee9e.root'
                                        #'/store/relval/CMSSW_12_4_0/RelValZMM_14/GEN-SIM-DIGI-RAW/124X_mcRun3_2022_realistic_v5-v1/2580000/050d4b88-616b-4e3d-a0e3-c5f3f28dd8c3.root'
                                    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(4),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('ProduceReco_v2.py nevts:25'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),

    fileName = cms.untracked.string('SingleMu10_AddRECOTier.root'),
                                              
#    fileName = cms.untracked.string('ZMM_RAW_DIGI_SIM_RECO_RU_CRAB.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_mcRun3_2022_realistic_v12', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.recosim_step = cms.Path(process.recosim)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.recosim_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)



# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
