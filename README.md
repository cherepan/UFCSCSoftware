# UFCSCSoftware
UF CSC ntuple

```
For Run II:
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv



For RunIII:
cmsrel CMSSW_12_4_4
cd CMSSW_12_4_4/src
cmsenv








cp the insides from https://github.com/cherepan/UFSegmentReco to the CMSSW core here


git cms-init
git cms-addpkg  DataFormats/CSCRecHit
git cms-addpkg  CalibMuon/CSCCalibration
git cms-addpkg  RecoLocalMuon/CSCRecHitD
git cms-addpkg  RecoLocalMuon/CSCSegment
git cms-addpkg RecoLocalMuon/CSCValidation
git clone git@github.com:cherepan/UFCSCSoftware.git
git clone git@github.com:cherepan/GifDisplay.git




git cms-addpkg L1Trigger/GlobalTrigger
git cms-addpkg SimMuon/CSCDigitizer
git cms-addpkg  RecoLocalMuon/Configuration
git cms-addpkg RecoMuon/StandAloneMuonProducer
```