import FWCore.ParameterSet.Config as cms

cscRootMaker = cms.EDAnalyzer('UFCSCRootMaker',
  muonSrc = cms.untracked.InputTag('muons'),
  vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices'),
  standAloneMuonsSrc = cms.untracked.InputTag('standAloneMuons'),
  cscRecHitTagSrc = cms.untracked.InputTag('csc2DRecHits'),
  cscSegTagSrc = cms.untracked.InputTag('cscSegments','','reRECO'),   #  UF reco
#  cscSegTagSrc = cms.untracked.InputTag('cscSegments','','RECO'),    #  RU reco

  level1TagSrc = cms.untracked.InputTag('gtDigis'),
  hltTagSrc = cms.untracked.InputTag('TriggerResults', '', 'HLT'),
  stripDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCStripDigi'),
  wireDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCWireDigi'),
  compDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi'),
  alctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCALCTDigi'),
  clctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCCLCTDigi'),
  corrlctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCCorrelatedLCTDigi'),
  simHitTagSrc = cms.untracked.InputTag('g4SimHits', 'MuonCSCHits'),
  fedRawTagSrc = cms.untracked.InputTag('rawDataCollector'),
  isLocalRECO = cms.untracked.bool(False),
  isFullRECO = cms.untracked.bool(False),
  isGEN = cms.untracked.bool(False),
  isSIM = cms.untracked.bool(False),
  isRAW = cms.untracked.bool(False),
  isDIGI = cms.untracked.bool(False),
  isDATA = cms.untracked.bool(False),
  addMuons = cms.untracked.bool(False),
  addTracks = cms.untracked.bool(False),
  addRecHits = cms.untracked.bool(False),
  addSegments = cms.untracked.bool(False),
  addTrigger = cms.untracked.bool(False),
  addDigis = cms.untracked.bool(False),
  addTimeMonitoring = cms.untracked.bool(False),
  addCalibrations = cms.untracked.bool(False)
)
