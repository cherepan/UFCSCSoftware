import FWCore.ParameterSet.Config as cms

cscRootMaker = cms.EDAnalyzer('UFCSCRootMaker',
  muonSrc = cms.untracked.InputTag('muons'),
  vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices'),
  genParticles = cms.untracked.InputTag('genParticles'),
  standAloneMuonsSrc = cms.untracked.InputTag('standAloneMuons'),
  generalTracksSrc   = cms.untracked.InputTag('generalTracks','','RECO'),

#  cscRecHitTagSrc = cms.untracked.InputTag('csc2DRecHits'), # it was default
#  cscSegTagSrc = cms.untracked.InputTag('cscSegments','','RECO'),    #  RU recocscSegTagSrc



#  cscRecHitTagSrc = cms.untracked.InputTag('csc2DRecHits','','localRecoUF'), # UF RECO
 cscRecHitTagSrc = cms.untracked.InputTag('csc2DRecHits','','RECO'), # RU reco # always use the rechots if STD aldo


#  cscSegTagSrc = cms.untracked.InputTag('cscSegments','','localRecoUF'),   #  UF reco
  cscSegTagSrc = cms.untracked.InputTag('cscSegments','','RECO'),    #  RU reco



  cscRecHitTagSrcRULR = cms.untracked.InputTag('csc2DRecHits','','RECO'),        # RU reco
  cscRecHitTagSrcUFLR = cms.untracked.InputTag('csc2DRecHits','','localRecoUF'), # UF RECO

  cscSegmentsRULR = cms.untracked.InputTag('cscSegments','','RECO'),           #  RU reco
  cscSegmentsUFLR = cms.untracked.InputTag('cscSegments','','localRecoUF'),    #  UF reco



  level1TagSrc = cms.untracked.InputTag('gtDigis'),
  hltTagSrc = cms.untracked.InputTag('TriggerResults', '', 'HLT'),
  stripDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCStripDigi'),
  wireDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCWireDigi'),
  compDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi'),
  alctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCALCTDigi'),
  clctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCCLCTDigi'),
  corrlctDigiTagSrc = cms.untracked.InputTag('muonCSCDigis', 'MuonCSCCorrelatedLCTDigi'),
  simHitTagSrc = cms.untracked.InputTag('g4SimHits', 'MuonCSCHits'),
  simTracksTagSrc = cms.untracked.InputTag('g4SimHits','', 'SIM'),
  fedRawTagSrc = cms.untracked.InputTag('rawDataCollector'),
  isLocalRECO = cms.untracked.bool(False),
  isFullRECO = cms.untracked.bool(True),
  isGEN = cms.untracked.bool(False),
  isSIM = cms.untracked.bool(False),
  isRAW = cms.untracked.bool(False),
  isDIGI = cms.untracked.bool(False),
  isDATA = cms.untracked.bool(False),
  addMuons = cms.untracked.bool(False),
  addTracks = cms.untracked.bool(False),
  addRecoTracks = cms.untracked.bool(False),
  addRecHits = cms.untracked.bool(False),
  addSegments = cms.untracked.bool(False),
  addTrigger = cms.untracked.bool(False),
  addDigis = cms.untracked.bool(False),
  addTimeMonitoring = cms.untracked.bool(False),
  addCalibrations = cms.untracked.bool(False)

)
