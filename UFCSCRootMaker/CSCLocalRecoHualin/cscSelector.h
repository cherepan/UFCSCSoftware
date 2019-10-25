//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Oct 17 05:55:44 2017 by ROOT version 6.06/01
// from TTree Events/Events
// found on file: DUMMYFILENAME_UF.root
//////////////////////////////////////////////////////////

#ifndef cscSelector_h
#define cscSelector_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
// Headers needed by this particular selector
#include <vector>

#include "clib/CSC1DSegment.h"
typedef pair<int, vector<int> > SegsInChamber;
/*
   struct CSC1DSeg{

    int keyPos;
    int hitsPos[6];
    int hitsTime[6];
    int nHits;

   };
*/
class cscSelector : public TSelector {
public :
   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain

   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<ULong64_t> Run = {fReader, "Run"};
   TTreeReaderValue<ULong64_t> Event = {fReader, "Event"};
   TTreeReaderValue<ULong64_t> LumiSect = {fReader, "LumiSect"};
   TTreeReaderValue<Int_t> BunchCrossing = {fReader, "BunchCrossing"};
   TTreeReaderValue<UInt_t> timeSecond = {fReader, "timeSecond"};
//   TTreeReaderValue<Double_t> instLumi = {fReader, "instLumi"};
//   TTreeReaderValue<Double_t> avgInstantLumi = {fReader, "avgInstantLumi"};
//   TTreeReaderValue<Double_t> correctedAvgInstantLumi = {fReader, "correctedAvgInstantLumi"};
//   TTreeReaderValue<Double_t> rawbxlumi = {fReader, "rawbxlumi"};
/*
   TTreeReaderArray<Double_t> bx_B1 = {fReader, "bx_B1"};
   TTreeReaderArray<Double_t> bx_B2 = {fReader, "bx_B2"};
   TTreeReaderArray<Double_t> bx_LUMI = {fReader, "bx_LUMI"};
   TTreeReaderValue<Int_t> tracks_nTracks = {fReader, "tracks_nTracks"};
   TTreeReaderArray<Int_t> tracks_charge = {fReader, "tracks_charge"};
   TTreeReaderArray<Double_t> tracks_px = {fReader, "tracks_px"};
   TTreeReaderArray<Double_t> tracks_py = {fReader, "tracks_py"};
   TTreeReaderArray<Double_t> tracks_pz = {fReader, "tracks_pz"};
   TTreeReaderArray<Double_t> tracks_pt = {fReader, "tracks_pt"};
   TTreeReaderArray<Double_t> tracks_p = {fReader, "tracks_p"};
   TTreeReaderArray<Double_t> tracks_eta = {fReader, "tracks_eta"};
   TTreeReaderArray<Double_t> tracks_phi = {fReader, "tracks_phi"};
   TTreeReaderValue<Int_t> simHits_nSimHits = {fReader, "simHits_nSimHits"};
   TTreeReaderArray<Int_t> simHits_particleType = {fReader, "simHits_particleType"};
   TTreeReaderArray<Double_t> simHits_localX = {fReader, "simHits_localX"};
   TTreeReaderArray<Double_t> simHits_localY = {fReader, "simHits_localY"};
   TTreeReaderArray<Double_t> simHits_globalX = {fReader, "simHits_globalX"};
   TTreeReaderArray<Double_t> simHits_globalY = {fReader, "simHits_globalY"};
   TTreeReaderArray<Int_t> simHits_ID_endcap = {fReader, "simHits_ID_endcap"};
   TTreeReaderArray<Int_t> simHits_ID_ring = {fReader, "simHits_ID_ring"};
   TTreeReaderArray<Int_t> simHits_ID_station = {fReader, "simHits_ID_station"};
   TTreeReaderArray<Int_t> simHits_ID_chamber = {fReader, "simHits_ID_chamber"};
   TTreeReaderArray<Int_t> simHits_ID_layer = {fReader, "simHits_ID_layer"};
   TTreeReaderArray<Int_t> simHits_ID_chamberSerial = {fReader, "simHits_ID_chamberSerial"};
   TTreeReaderArray<Int_t> simHits_ID_ringSerial = {fReader, "simHits_ID_ringSerial"};
   TTreeReaderArray<Int_t> simHits_ID_processType = {fReader, "simHits_ID_processType"};
   TTreeReaderArray<Double_t> simHits_momentum = {fReader, "simHits_momentum"};
   TTreeReaderArray<Double_t> simHits_phi = {fReader, "simHits_phi"};
   TTreeReaderArray<Double_t> simHits_theta = {fReader, "simHits_theta"};
*/
   TTreeReaderValue<Int_t> recHits2D_nRecHits2D = {fReader, "recHits2D_nRecHits2D"};
   TTreeReaderArray<Int_t> recHits2D_ID_endcap = {fReader, "recHits2D_ID_endcap"};
   TTreeReaderArray<Int_t> recHits2D_ID_ring = {fReader, "recHits2D_ID_ring"};
   TTreeReaderArray<Int_t> recHits2D_ID_station = {fReader, "recHits2D_ID_station"};
   TTreeReaderArray<Int_t> recHits2D_ID_chamber = {fReader, "recHits2D_ID_chamber"};
   TTreeReaderArray<Int_t> recHits2D_ID_layer = {fReader, "recHits2D_ID_layer"};
   TTreeReaderArray<Double_t> recHits2D_localX = {fReader, "recHits2D_localX"};
   TTreeReaderArray<Double_t> recHits2D_localY = {fReader, "recHits2D_localY"};
   TTreeReaderArray<Double_t> recHits2D_localXXerr = {fReader, "recHits2D_localXXerr"};
//   TTreeReaderArray<Double_t> recHits2D_localYYer = {fReader, "recHits2D_localYYerr"};
   TTreeReaderArray<Double_t> recHits2D_localXYerr = {fReader, "recHits2D_localXYerr"};
   TTreeReaderArray<Double_t> recHits2D_stripPosition = {fReader, "recHits2D_stripPosition"};
   TTreeReaderArray<Double_t> recHits2D_stripError = {fReader, "recHits2D_stripError"};
   TTreeReaderArray<Double_t> recHits2D_SumQ = {fReader, "recHits2D_SumQ"};
   TTreeReaderArray<Double_t> recHits2D_SumQSides = {fReader, "recHits2D_SumQSides"};
   TTreeReaderArray<Double_t> recHits2D_Time = {fReader, "recHits2D_Time"};
   TTreeReaderArray<Double_t> recHits2D_globalX = {fReader, "recHits2D_globalX"};
   TTreeReaderArray<Double_t> recHits2D_globalY = {fReader, "recHits2D_globalY"};
   TTreeReaderArray<Int_t> recHits2D_belongsToSaMuon = {fReader, "recHits2D_belongsToSaMuon"};
   TTreeReaderArray<Int_t> recHits2D_belongsToMuon = {fReader, "recHits2D_belongsToMuon"};
   TTreeReaderArray<Int_t> recHits2D_ID_chamberSerial = {fReader, "recHits2D_ID_chamberSerial"};
   TTreeReaderArray<Int_t> recHits2D_ID_ringSerial = {fReader, "recHits2D_ID_ringSerial"};
   TTreeReaderArray<Int_t> recHits2D_simHit_particleTypeID = {fReader, "recHits2D_simHit_particleTypeID"};
   TTreeReaderArray<Double_t> recHits2D_simHit_localX = {fReader, "recHits2D_simHit_localX"};
   TTreeReaderArray<Double_t> recHits2D_simHit_localY = {fReader, "recHits2D_simHit_localY"};
   TTreeReaderArray<Double_t> recHits2D_ADCSignal = {fReader, "recHits2D_ADCSignal"};
   TTreeReaderArray<Int_t> recHits2D_nearestStrip = {fReader, "recHits2D_nearestStrip"};
   TTreeReaderArray<Int_t> recHits2D_nearestWire = {fReader, "recHits2D_nearestWire"};
   TTreeReaderArray<Int_t> recHits2D_nearestWireGroup = {fReader, "recHits2D_nearestWireGroup"};
   TTreeReaderArray<Double_t> recHits2D_localStripWireIntersectionX = {fReader, "recHits2D_localStripWireIntersectionX"};
   TTreeReaderArray<Double_t> recHits2D_localStripWireIntersectionY = {fReader, "recHits2D_localStripWireIntersectionY"};
   TTreeReaderArray<Double_t> recHits2D_localStripWireGroupIntersectionX = {fReader, "recHits2D_localStripWireGroupIntersectionX"};
   TTreeReaderArray<Double_t> recHits2D_localStripWireGroupIntersectionY = {fReader, "recHits2D_localStripWireGroupIntersectionY"};
   TTreeReaderArray<Double_t> recHits2D_stripWidthAtHit = {fReader, "recHits2D_stripWidthAtHit"};
   TTreeReaderArray<Double_t> recHits2D_positionWithinStrip = {fReader, "recHits2D_positionWithinStrip"};
   TTreeReaderArray<Double_t> recHits2D_wireTime = {fReader, "recHits2D_wireTime"};
   TTreeReaderArray<Int_t> recHits2D_hitWire = {fReader, "recHits2D_hitWire"};
   TTreeReaderArray<Int_t> recHits2D_wgroupsBX = {fReader, "recHits2D_wgroupsBX"};
   TTreeReaderArray<Int_t> recHits2D_nWireGroups = {fReader, "recHits2D_nWireGroups"};
   TTreeReaderValue<Int_t> cscSegments_nSegments = {fReader, "cscSegments_nSegments"};
   TTreeReaderArray<Double_t> cscSegments_localX = {fReader, "cscSegments_localX"};
   TTreeReaderArray<Double_t> cscSegments_localY = {fReader, "cscSegments_localY"};
   TTreeReaderArray<Double_t> cscSegments_globalX = {fReader, "cscSegments_globalX"};
   TTreeReaderArray<Double_t> cscSegments_globalY = {fReader, "cscSegments_globalY"};
   TTreeReaderArray<Double_t> cscSegments_globalTheta = {fReader, "cscSegments_globalTheta"};
   TTreeReaderArray<Double_t> cscSegments_globalPhi = {fReader, "cscSegments_globalPhi"};
   TTreeReaderArray<Double_t> cscSegments_localTheta = {fReader, "cscSegments_localTheta"};
   TTreeReaderArray<Double_t> cscSegments_chi2 = {fReader, "cscSegments_chi2"};
   TTreeReaderArray<Double_t> cscSegments_nRecHits = {fReader, "cscSegments_nRecHits"};
   TTreeReaderArray<Int_t> cscSegments_nDOF = {fReader, "cscSegments_nDOF"};
   TTreeReaderArray<Int_t> cscSegments_ID_endcap = {fReader, "cscSegments_ID_endcap"};
   TTreeReaderArray<Int_t> cscSegments_ID_ring = {fReader, "cscSegments_ID_ring"};
   TTreeReaderArray<Int_t> cscSegments_ID_station = {fReader, "cscSegments_ID_station"};
   TTreeReaderArray<Int_t> cscSegments_ID_chamber = {fReader, "cscSegments_ID_chamber"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_endcap = {fReader, "cscSegments_recHitRecord_endcap"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_ring = {fReader, "cscSegments_recHitRecord_ring"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_station = {fReader, "cscSegments_recHitRecord_station"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_chamber = {fReader, "cscSegments_recHitRecord_chamber"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_layer = {fReader, "cscSegments_recHitRecord_layer"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_localY = {fReader, "cscSegments_recHitRecord_localY"};
   TTreeReaderArray<vector<double>> cscSegments_recHitRecord_localX = {fReader, "cscSegments_recHitRecord_localX"};
   TTreeReaderArray<Int_t> cscSegments_ID_chamberSerial = {fReader, "cscSegments_ID_chamberSerial"};
   TTreeReaderArray<Int_t> cscSegments_ID_ringSerial = {fReader, "cscSegments_ID_ringSerial"};
   TTreeReaderArray<Int_t> cscSegments_Resolution_residual = {fReader, "cscSegments_Resolution_residual"};
   TTreeReaderArray<Int_t> cscSegments_Resolution_pull = {fReader, "cscSegments_Resolution_pull"};
   TTreeReaderValue<Int_t> muons_nMuons = {fReader, "muons_nMuons"};
   TTreeReaderArray<Bool_t> muons_isPFMuon = {fReader, "muons_isPFMuon"};
   TTreeReaderArray<Bool_t> muons_isCaloMuon = {fReader, "muons_isCaloMuon"};
   TTreeReaderArray<Bool_t> muons_isTrackerMuon = {fReader, "muons_isTrackerMuon"};
   TTreeReaderArray<Bool_t> muons_isStandAloneMuon = {fReader, "muons_isStandAloneMuon"};
   TTreeReaderArray<Bool_t> muons_isGlobalMuon = {fReader, "muons_isGlobalMuon"};
   TTreeReaderArray<Int_t> muons_numberOfChambers = {fReader, "muons_numberOfChambers"};
   TTreeReaderArray<Int_t> muons_numberOfSegments = {fReader, "muons_numberOfSegments"};
   TTreeReaderArray<Int_t> muons_numberOfMatches = {fReader, "muons_numberOfMatches"};
   TTreeReaderArray<Bool_t> muons_isEnergyValid = {fReader, "muons_isEnergyValid"};
   TTreeReaderArray<Double_t> muons_calEnergyTower = {fReader, "muons_calEnergyTower"};
   TTreeReaderArray<Double_t> muons_calEnergyEm = {fReader, "muons_calEnergyEm"};
   TTreeReaderArray<Double_t> muons_calEnergyHad = {fReader, "muons_calEnergyHad"};
   TTreeReaderArray<Int_t> muons_charge = {fReader, "muons_charge"};
   TTreeReaderArray<Double_t> muons_energy = {fReader, "muons_energy"};
   TTreeReaderArray<Double_t> muons_px = {fReader, "muons_px"};
   TTreeReaderArray<Double_t> muons_py = {fReader, "muons_py"};
   TTreeReaderArray<Double_t> muons_pz = {fReader, "muons_pz"};
   TTreeReaderArray<Double_t> muons_pt = {fReader, "muons_pt"};
   TTreeReaderArray<Double_t> muons_et = {fReader, "muons_et"};
   TTreeReaderArray<Double_t> muons_p = {fReader, "muons_p"};
   TTreeReaderArray<Double_t> muons_phi = {fReader, "muons_phi"};
   TTreeReaderArray<Double_t> muons_eta = {fReader, "muons_eta"};
   TTreeReaderArray<Double_t> muons_theta = {fReader, "muons_theta"};
   TTreeReaderArray<Double_t> muons_vx = {fReader, "muons_vx"};
   TTreeReaderArray<Double_t> muons_vy = {fReader, "muons_vy"};
   TTreeReaderArray<Double_t> muons_vz = {fReader, "muons_vz"};
   TTreeReaderArray<Double_t> muons_globalTrackNormalizedChi2 = {fReader, "muons_globalTrackNormalizedChi2"};
   TTreeReaderArray<Int_t> muons_globalTrackNumberOfValidMuonHits = {fReader, "muons_globalTrackNumberOfValidMuonHits"};
   TTreeReaderArray<Int_t> muons_trackNumberOfValidHits = {fReader, "muons_trackNumberOfValidHits"};
   TTreeReaderArray<Int_t> muons_trackNumberOfLostHits = {fReader, "muons_trackNumberOfLostHits"};
   TTreeReaderArray<Double_t> muons_isoNH03 = {fReader, "muons_isoNH03"};
   TTreeReaderArray<Double_t> muons_isoCH03 = {fReader, "muons_isoCH03"};
   TTreeReaderArray<Double_t> muons_isoPhot03 = {fReader, "muons_isoPhot03"};
   TTreeReaderArray<Double_t> muons_isoPU03 = {fReader, "muons_isoPU03"};
   TTreeReaderArray<Double_t> muons_isoCH04 = {fReader, "muons_isoCH04"};
   TTreeReaderArray<Double_t> muons_isoPhot04 = {fReader, "muons_isoPhot04"};
   TTreeReaderArray<Double_t> muons_isoNH04 = {fReader, "muons_isoNH04"};
   TTreeReaderArray<Double_t> muons_isoPU04 = {fReader, "muons_isoPU04"};
   TTreeReaderArray<Double_t> muons_dz = {fReader, "muons_dz"};
   TTreeReaderArray<Double_t> muons_dxy = {fReader, "muons_dxy"};
   TTreeReaderArray<Int_t> muons_nRecHits = {fReader, "muons_nRecHits"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_nRecHits = {fReader, "muons_cscSegmentRecord_nRecHits"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_ring = {fReader, "muons_cscSegmentRecord_ring"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_station = {fReader, "muons_cscSegmentRecord_station"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_chamber = {fReader, "muons_cscSegmentRecord_chamber"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_endcap = {fReader, "muons_cscSegmentRecord_endcap"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_localY = {fReader, "muons_cscSegmentRecord_localY"};
   TTreeReaderArray<vector<double>> muons_cscSegmentRecord_localX = {fReader, "muons_cscSegmentRecord_localX"};
/*
   TTreeReaderValue<Bool_t> l1Trigger_CSC = {fReader, "l1Trigger_CSC"};
   TTreeReaderValue<Bool_t> l1Trigger_DT = {fReader, "l1Trigger_DT"};
   TTreeReaderValue<Bool_t> l1Trigger_RPCForward = {fReader, "l1Trigger_RPCForward"};
   TTreeReaderValue<Bool_t> l1Trigger_RPCBarrel = {fReader, "l1Trigger_RPCBarrel"};
   TTreeReaderValue<Bool_t> l1Trigger_beamHalo = {fReader, "l1Trigger_beamHalo"};
   TTreeReaderValue<Int_t> hltTrigger_nBits = {fReader, "hltTrigger_nBits"};
   TTreeReaderArray<Int_t> hltTrigger_bits = {fReader, "hltTrigger_bits"};
   TTreeReaderValue<Int_t> standaloneMuons_nMuons = {fReader, "standaloneMuons_nMuons"};
   TTreeReaderArray<Double_t> standaloneMuons_p = {fReader, "standaloneMuons_p"};
   TTreeReaderArray<Double_t> standaloneMuons_pt = {fReader, "standaloneMuons_pt"};
   TTreeReaderArray<Int_t> standaloneMuons_nRecHits = {fReader, "standaloneMuons_nRecHits"};
   TTreeReaderArray<Double_t> standaloneMuons_chi2 = {fReader, "standaloneMuons_chi2"};
   TTreeReaderArray<Double_t> standaloneMuons_normChi2 = {fReader, "standaloneMuons_normChi2"};
   TTreeReaderArray<Int_t> standaloneMuons_nDTHits = {fReader, "standaloneMuons_nDTHits"};
   TTreeReaderArray<Int_t> standaloneMuons_nCSCHits = {fReader, "standaloneMuons_nCSCHits"};
   TTreeReaderArray<Int_t> standaloneMuons_nCSCHitsP = {fReader, "standaloneMuons_nCSCHitsP"};
   TTreeReaderArray<Int_t> standaloneMuons_nCSCHitsM = {fReader, "standaloneMuons_nCSCHitsM"};
   TTreeReaderArray<Int_t> standaloneMuons_nRPCHits = {fReader, "standaloneMuons_nRPCHits"};
   TTreeReaderArray<Int_t> standaloneMuons_nRPCHitsP = {fReader, "standaloneMuons_nRPCHitsP"};
   TTreeReaderArray<Int_t> standaloneMuons_nRPCHitsM = {fReader, "standaloneMuons_nRPCHitsM"};
   TTreeReaderArray<Int_t> standaloneMuons_nHitsM = {fReader, "standaloneMuons_nHitsM"};
   TTreeReaderArray<Int_t> standaloneMuons_nHitsP = {fReader, "standaloneMuons_nHitsP"};
   TTreeReaderArray<Double_t> standaloneMuons_crudeLength = {fReader, "standaloneMuons_crudeLength"};
   TTreeReaderArray<Double_t> standaloneMuons_deltaPhi = {fReader, "standaloneMuons_deltaPhi"};
   TTreeReaderArray<Double_t> standaloneMuons_innerGlobalPolarAngle = {fReader, "standaloneMuons_innerGlobalPolarAngle"};
   TTreeReaderArray<Double_t> standaloneMuons_outerGlobalPolarAngle = {fReader, "standaloneMuons_outerGlobalPolarAngle"};
*/
   TTreeReaderValue<Int_t> firedStripDigis_nStripDigis = {fReader, "firedStripDigis_nStripDigis"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_endcap = {fReader, "firedStripDigis_ID_endcap"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_chamber = {fReader, "firedStripDigis_ID_chamber"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_station = {fReader, "firedStripDigis_ID_station"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_layer = {fReader, "firedStripDigis_ID_layer"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_strip = {fReader, "firedStripDigis_ID_strip"};
   TTreeReaderArray<Int_t> firedStripDigis_ID_ring = {fReader, "firedStripDigis_ID_ring"};
   TTreeReaderArray<Double_t> firedStripDigis_ADCTotal = {fReader, "firedStripDigis_ADCTotal"};
   TTreeReaderArray<Double_t> firedStripDigis_ADCMax = {fReader, "firedStripDigis_ADCMax"};
   TTreeReaderArray<Int_t> firedStripDigis_tbinMax = {fReader, "firedStripDigis_tbinMax"};
   TTreeReaderArray<Double_t> firedStripDigis_localX = {fReader, "firedStripDigis_localX"};


   TTreeReaderValue<Int_t> firedWireDigis_nWireDigis = {fReader, "firedWireDigis_nWireDigis"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_endcap = {fReader, "firedWireDigis_ID_endcap"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_chamber = {fReader, "firedWireDigis_ID_chamber"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_station = {fReader, "firedWireDigis_ID_station"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_wire = {fReader, "firedWireDigis_ID_wire"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_layer = {fReader, "firedWireDigis_ID_layer"};
   TTreeReaderArray<Int_t> firedWireDigis_ID_ring = {fReader, "firedWireDigis_ID_ring"};
   TTreeReaderArray<Int_t> firedWireDigis_timeBin = {fReader, "firedWireDigis_timeBin"};
   TTreeReaderArray<Int_t> firedWireDigis_chamberSerial = {fReader, "firedWireDigis_chamberSerial"};
   TTreeReaderArray<Int_t> firedWireDigis_numberWireTimeBins = {fReader, "firedWireDigis_numberWireTimeBins"};
   TTreeReaderArray<Int_t> firedWireDigis_AFEB = {fReader, "firedWireDigis_AFEB"};
   TTreeReaderArray<Double_t> firedWireDigis_localY = {fReader, "firedWireDigis_localY"};

   TTreeReaderValue<Int_t> comparatorDigis_nDigis = {fReader, "comparatorDigis_nDigis"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_endcap = {fReader, "comparatorDigis_ID_endcap"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_chamber = {fReader, "comparatorDigis_ID_chamber"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_station = {fReader, "comparatorDigis_ID_station"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_strip = {fReader, "comparatorDigis_ID_strip"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_layer = {fReader, "comparatorDigis_ID_layer"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_ring = {fReader, "comparatorDigis_ID_ring"};
   TTreeReaderArray<Int_t> comparatorDigis_timeBin = {fReader, "comparatorDigis_timeBin"};
   TTreeReaderArray<Int_t> comparatorDigis_cfeb = {fReader, "comparatorDigis_cfeb"};
   TTreeReaderArray<Int_t> comparatorDigis_ID_halfStrip = {fReader, "comparatorDigis_ID_halfStrip"};


/*
   TTreeReaderValue<Int_t> alct_nAlcts = {fReader, "alct_nAlcts"};
   TTreeReaderArray<Int_t> alct_BX = {fReader, "alct_BX"};
   TTreeReaderArray<Int_t> alct_fullBX = {fReader, "alct_fullBX"};
   TTreeReaderArray<Int_t> alct_ID_ring = {fReader, "alct_ID_ring"};
   TTreeReaderArray<Int_t> alct_ID_layer = {fReader, "alct_ID_layer"};
   TTreeReaderArray<Int_t> alct_ID_chamberID = {fReader, "alct_ID_chamberID"};
   TTreeReaderArray<Int_t> alct_ID_chamber = {fReader, "alct_ID_chamber"};
   TTreeReaderArray<Int_t> alct_ID_endcap = {fReader, "alct_ID_endcap"};
   TTreeReaderArray<Int_t> alct_ID_station = {fReader, "alct_ID_station"};
   TTreeReaderArray<Int_t> alct_ID_chamberSerial = {fReader, "alct_ID_chamberSerial"};
   TTreeReaderArray<Int_t> alct_ID_ringSerial = {fReader, "alct_ID_ringSerial"};
   TTreeReaderValue<Int_t> clct_nClcts = {fReader, "clct_nClcts"};
   TTreeReaderArray<Int_t> clct_BX = {fReader, "clct_BX"};
   TTreeReaderArray<Int_t> clct_fullBX = {fReader, "clct_fullBX"};
   TTreeReaderArray<Int_t> clct_ID_ring = {fReader, "clct_ID_ring"};
   TTreeReaderArray<Int_t> clct_ID_layer = {fReader, "clct_ID_layer"};
   TTreeReaderArray<Int_t> clct_ID_chamberID = {fReader, "clct_ID_chamberID"};
   TTreeReaderArray<Int_t> clct_ID_chamber = {fReader, "clct_ID_chamber"};
   TTreeReaderArray<Int_t> clct_ID_endcap = {fReader, "clct_ID_endcap"};
   TTreeReaderArray<Int_t> clct_ID_station = {fReader, "clct_ID_station"};
   TTreeReaderArray<Int_t> clct_ID_chamberSerial = {fReader, "clct_ID_chamberSerial"};
   TTreeReaderArray<Int_t> clct_ID_ringSerial = {fReader, "clct_ID_ringSerial"};
   TTreeReaderValue<Int_t> correlatedLct_nLcts = {fReader, "correlatedLct_nLcts"};
   TTreeReaderArray<Int_t> correlatedLct_BX = {fReader, "correlatedLct_BX"};
   TTreeReaderArray<Int_t> correlatedLct_trkNumber = {fReader, "correlatedLct_trkNumber"};
   TTreeReaderArray<Int_t> correlatedLct_quality = {fReader, "correlatedLct_quality"};
   TTreeReaderArray<Int_t> correlatedLct_keyWG = {fReader, "correlatedLct_keyWG"};
   TTreeReaderArray<Int_t> correlatedLct_strip = {fReader, "correlatedLct_strip"};
   TTreeReaderArray<Int_t> correlatedLct_pattern = {fReader, "correlatedLct_pattern"};
   TTreeReaderArray<Int_t> correlatedLct_bend = {fReader, "correlatedLct_bend"};
   TTreeReaderArray<Int_t> correlatedLct_CLCTPattern = {fReader, "correlatedLct_CLCTPattern"};
   TTreeReaderArray<UShort_t> correlatedLct_cscID = {fReader, "correlatedLct_cscID"};
   TTreeReaderArray<UShort_t> correlatedLct_BX0 = {fReader, "correlatedLct_BX0"};
   TTreeReaderArray<UShort_t> correlatedLct_syncErr = {fReader, "correlatedLct_syncErr"};
   TTreeReaderArray<Int_t> correlatedLct_ID_chamber = {fReader, "correlatedLct_ID_chamber"};
   TTreeReaderArray<Int_t> correlatedLct_ID_ring = {fReader, "correlatedLct_ID_ring"};
   TTreeReaderArray<Int_t> correlatedLct_ID_station = {fReader, "correlatedLct_ID_station"};
   TTreeReaderArray<Int_t> correlatedLct_ID_endcap = {fReader, "correlatedLct_ID_endcap"};
   TTreeReaderArray<Int_t> correlatedLct_ID_layer = {fReader, "correlatedLct_ID_layer"};
   TTreeReaderArray<Int_t> correlatedLct_ID_chamberSerial = {fReader, "correlatedLct_ID_chamberSerial"};
   TTreeReaderArray<Int_t> correlatedLct_ID_ringSerial = {fReader, "correlatedLct_ID_ringSerial"};

   TTreeReaderValue<Int_t> tmb_nTmb = {fReader, "tmb_nTmb"};
   TTreeReaderArray<Int_t> tmb_BXNCount = {fReader, "tmb_BXNCount"};
   TTreeReaderArray<Int_t> tmb_ALCTMatchTime = {fReader, "tmb_ALCTMatchTime"};
   TTreeReaderArray<Int_t> tmb_ID_chamberID = {fReader, "tmb_ID_chamberID"};
   TTreeReaderArray<Int_t> tmb_ID_chamber = {fReader, "tmb_ID_chamber"};
   TTreeReaderArray<Int_t> tmb_ID_endcap = {fReader, "tmb_ID_endcap"};
   TTreeReaderArray<Int_t> tmb_ID_station = {fReader, "tmb_ID_station"};
   TTreeReaderArray<Int_t> tmb_ID_ring = {fReader, "tmb_ID_ring"};
   TTreeReaderArray<Int_t> tmb_ID_layer = {fReader, "tmb_ID_layer"};
   TTreeReaderArray<Int_t> tmb_ID_chamberSerial = {fReader, "tmb_ID_chamberSerial"};
   TTreeReaderArray<Int_t> tmb_ID_ringSerial = {fReader, "tmb_ID_ringSerial"};
   TTreeReaderArray<Int_t> tmb_alct0key = {fReader, "tmb_alct0key"};
   TTreeReaderArray<Int_t> tmb_alctRelL1A = {fReader, "tmb_alctRelL1A"};
   TTreeReaderValue<Int_t> calibrations_nCalib = {fReader, "calibrations_nCalib"};
   TTreeReaderArray<Double_t> calibrations_Gain_slope = {fReader, "calibrations_Gain_slope"};
   TTreeReaderArray<Double_t> calibrations_XT_slope_left = {fReader, "calibrations_XT_slope_left"};
   TTreeReaderArray<Double_t> calibrations_XT_slope_right = {fReader, "calibrations_XT_slope_right"};
   TTreeReaderArray<Double_t> calibrations_XT_intercept_left = {fReader, "calibrations_XT_intercept_left"};
   TTreeReaderArray<Double_t> calibrations_XT_intercept_right = {fReader, "calibrations_XT_intercept_right"};
   TTreeReaderArray<Double_t> calibrations_Pedestals_ped = {fReader, "calibrations_Pedestals_ped"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_33 = {fReader, "calibrations_NoiseMatrix_33"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_34 = {fReader, "calibrations_NoiseMatrix_34"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_35 = {fReader, "calibrations_NoiseMatrix_35"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_44 = {fReader, "calibrations_NoiseMatrix_44"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_45 = {fReader, "calibrations_NoiseMatrix_45"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_46 = {fReader, "calibrations_NoiseMatrix_46"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_55 = {fReader, "calibrations_NoiseMatrix_55"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_56 = {fReader, "calibrations_NoiseMatrix_56"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_57 = {fReader, "calibrations_NoiseMatrix_57"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_66 = {fReader, "calibrations_NoiseMatrix_66"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_67 = {fReader, "calibrations_NoiseMatrix_67"};
   TTreeReaderArray<Double_t> calibrations_NoiseMatrix_77 = {fReader, "calibrations_NoiseMatrix_77"};
   TTreeReaderValue<Int_t> assocRecHits_nAssocRH = {fReader, "assocRecHits_nAssocRH"};
   TTreeReaderArray<Int_t> assocRecHits_codeBroad = {fReader, "assocRecHits_codeBroad"};
   TTreeReaderArray<Int_t> assocRecHits_codeNarrow = {fReader, "assocRecHits_codeNarrow"};
   TTreeReaderArray<Int_t> assocRecHits_ID_layer = {fReader, "assocRecHits_ID_layer"};
   TTreeReaderArray<Int_t> assocRecHits_ID_station = {fReader, "assocRecHits_ID_station"};
   TTreeReaderArray<Int_t> assocRecHits_ID_ring = {fReader, "assocRecHits_ID_ring"};
   TTreeReaderArray<Int_t> assocRecHits_ID_chamber = {fReader, "assocRecHits_ID_chamber"};
   TTreeReaderArray<Int_t> assocRecHits_ID_endcap = {fReader, "assocRecHits_ID_endcap"};
   TTreeReaderArray<Int_t> assocRecHits_ID_centerStrip = {fReader, "assocRecHits_ID_centerStrip"};
   TTreeReaderArray<Double_t> assocRecHits_globalX = {fReader, "assocRecHits_globalX"};
   TTreeReaderArray<Double_t> assocRecHits_globalY = {fReader, "assocRecHits_globalY"};
   TTreeReaderArray<Double_t> assocRecHits_localX = {fReader, "assocRecHits_localX"};
   TTreeReaderArray<Double_t> assocRecHits_localY = {fReader, "assocRecHits_localY"};
   TTreeReaderArray<Double_t> assocRecHits_sumQ = {fReader, "assocRecHits_sumQ"};
   TTreeReaderArray<Double_t> assocRecHits_ratioSumQ = {fReader, "assocRecHits_ratioSumQ"};
   TTreeReaderArray<Double_t> assocRecHits_Time = {fReader, "assocRecHits_Time"};
   TTreeReaderArray<Int_t> assocRecHits_width = {fReader, "assocRecHits_width"};
   TTreeReaderValue<Int_t> nonAssocRecHits_nNonAssocRH = {fReader, "nonAssocRecHits_nNonAssocRH"};
   TTreeReaderArray<Int_t> nonAssocRecHits_codeBroad = {fReader, "nonAssocRecHits_codeBroad"};
   TTreeReaderArray<Int_t> nonAssocRecHits_codeNarrow = {fReader, "nonAssocRecHits_codeNarrow"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_layer = {fReader, "nonAssocRecHits_ID_layer"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_station = {fReader, "nonAssocRecHits_ID_station"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_ring = {fReader, "nonAssocRecHits_ID_ring"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_chamber = {fReader, "nonAssocRecHits_ID_chamber"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_endcap = {fReader, "nonAssocRecHits_ID_endcap"};
   TTreeReaderArray<Int_t> nonAssocRecHits_ID_centerStrip = {fReader, "nonAssocRecHits_ID_centerStrip"};
   TTreeReaderArray<Double_t> nonAssocRecHits_globalX = {fReader, "nonAssocRecHits_globalX"};
   TTreeReaderArray<Double_t> nonAssocRecHits_globalY = {fReader, "nonAssocRecHits_globalY"};
   TTreeReaderArray<Double_t> nonAssocRecHits_localX = {fReader, "nonAssocRecHits_localX"};
   TTreeReaderArray<Double_t> nonAssocRecHits_localY = {fReader, "nonAssocRecHits_localY"};
   TTreeReaderArray<Double_t> nonAssocRecHits_sumQ = {fReader, "nonAssocRecHits_sumQ"};
   TTreeReaderArray<Double_t> nonAssocRecHits_ratioSumQ = {fReader, "nonAssocRecHits_ratioSumQ"};
   TTreeReaderArray<Double_t> nonAssocRecHits_Time = {fReader, "nonAssocRecHits_Time"};
   TTreeReaderArray<Int_t> nonAssocRecHits_width = {fReader, "nonAssocRecHits_width"};
   TTreeReaderArray<Double_t> nonAssocRecHits_distToGoodRH = {fReader, "nonAssocRecHits_distToGoodRH"};
   TTreeReaderValue<Int_t> gasGain_nGasGain = {fReader, "gasGain_nGasGain"};
   TTreeReaderArray<Int_t> gasGain_chamberType = {fReader, "gasGain_chamberType"};
   TTreeReaderArray<Int_t> gasGain_HVSegNumber = {fReader, "gasGain_HVSegNumber"};
   TTreeReaderArray<Int_t> gasGain_NmbHVSegments = {fReader, "gasGain_NmbHVSegments"};
   TTreeReaderArray<Int_t> gasGain_location = {fReader, "gasGain_location"};
   TTreeReaderArray<Int_t> gasGain_chamber = {fReader, "gasGain_chamber"};
   TTreeReaderArray<Int_t> gasGain_ring = {fReader, "gasGain_ring"};
   TTreeReaderArray<Int_t> gasGain_station = {fReader, "gasGain_station"};
   TTreeReaderArray<Int_t> gasGain_endcap = {fReader, "gasGain_endcap"};
   TTreeReaderArray<Int_t> gasGain_layer = {fReader, "gasGain_layer"};
   TTreeReaderArray<Double_t> gasGain_ADC3x3Sum = {fReader, "gasGain_ADC3x3Sum"};

*/

//   vector<SegsInChamber> segs;

   cscSelector(TTree * /*tree*/ =0) { }
   virtual ~cscSelector() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   virtual void    FillSegs(int segIndex, int chamberIndex, vector<SegsInChamber>& segs);
   virtual void    SetInputs(int nEntry_ ,TString tag_/*, TString savedir_, bool doME11_*/);
//   virtual void    Initialize();
   virtual void    CountObjectsInCSCs(bool doRH, bool doSeg,
                                      bool doWire, bool doStrip, bool doComparator,
                                      bool doALCT, bool doCLCT, bool LCT);
   virtual void    SaveCSCWithMuon();
   vector<int>     RHsMatching(int endcap, int station, int ring, int chamber, double localX, double localY);
   virtual void    FillWireMatrix(vector<int> wireDigiIndexs, TMatrixDSparse& wireMatrix);
   virtual void    FillComparatorMatrix(vector<int> comparatorDigiIndexs, TMatrixDSparse& comparatorMatrix, bool doStagger, int min=0, int max=120);

//   virtual         vector<CSC1DSeg> MakeScans(TMatrixDSparse inputMatrix, bool reverseRowIndex, int** rows, int** cols, int* nHits, int* ranks, int nPatterns);
//   virtual         vector<CSC1DSeg> ScanPattern(TMatrixDSparse& inputMatrix, int nHitsPerSeg, bool reverseRowIndex, 
//                                                       int* r_index, int* c_index, int nHitsInPattern, int rank);

   virtual         vector<CSC1DSeg> MakeScans(TMatrixDSparse inputMatrix, bool reverseRowIndex, int** rows, int** cols, int* nHits, int* ranks, int nPatterns);
   virtual         /*TMatrixDSparse*/void ScanPattern(TMatrixDSparse& inputMatrix, vector<CSC1DSeg> & csc1DSegs, int nHitsPerSeg, bool reverseRowIndex,
                                                       int* r_index, int* c_index, int nHitsInPattern, int rank);

   virtual int     CountNonZero(int * array, int size);
   virtual void    Print1DSeg(CSC1DSeg seg1D);

   virtual void    PrintSparseMatrix(TMatrixDSparse inputMatrix);
   virtual void    WriteTH2F(TH2F* hist);
   virtual int    ChamberID_converter(int station, int ring);

   // save CSC's ID if there is a muon from Z decay
   vector<int> endcapL; 
   vector<int> stationL;
   vector<int> ringL;
   vector<int> chamberL;
   vector<int> muIndex;
   vector<vector<int> > stripsFromMu;

   vector<int> nRH[540] = {};
   vector<int> nSegmentL[540] = {};
   vector<int> nWire[540] = {};
   vector<int> nStrip[540] = {};
   vector<int> nComparator[540] = {};
   vector<int> nALCT[540] = {};
   vector<int> nCLCT[540] = {};
   vector<int> nLCT[540] = {};

   TH1F* nHitsPerCLCT_wide = new TH1F("nHitsPerCLCT_wide","",7,0,7);
   TH1F* nHitsPerCLCT_narrow = new TH1F("nHitsPerCLCT_narrow","",7,0,7);

   TH1F* nTotal = new TH1F("nTotal","",10,0,10); 
   TH1F* nTotal_wideHasLess = new TH1F("nTotal_wideHasLess","",10,0,10);

   TH1F* eff_layer6 = new TH1F("eff_layer6","",5,1,6);
   TH1F* eff_layer5 = new TH1F("eff_layer5","",5,1,6);
   TH1F* eff_layer4 = new TH1F("eff_layer4","",5,1,6);
   TH1F* eff_layer6_narrow = new TH1F("eff_layer6_narrow","",5,1,6);
   TH1F* eff_layer5_narrow = new TH1F("eff_layer5_narrow","",5,1,6);
   TH1F* eff_layer4_narrow = new TH1F("eff_layer4_narrow","",5,1,6);
 
   TH1F* nCLCT_wide = new TH1F("nCLCT_wide","",10,0,10);
   TH1F* nCLCT_narrow = new TH1F("nCLCT_narrow","",10,0,10);

   TH1F* nCLCT_wide_rank_1_2 = new TH1F("nCLCT_wide_rank_1_2","",10,0,10);
   TH1F* nCLCT_narrow_rank_1_2 = new TH1F("nCLCT_narrow_rank_1_2","",10,0,10);
 
   TH1F* nCLCT_wide_layer_6 = new TH1F("nCLCT_wide_layer_6","",10,0,10);
   TH1F* nCLCT_narrow_layer_6 = new TH1F("nCLCT_narrow_layer_6","",10,0,10);

   TH1F* nCLCT_wide_layer_5= new TH1F("nCLCT_wide_layer_5","",10,0,10);
   TH1F* nCLCT_narrow_layer_5 = new TH1F("nCLCT_narrow_layer_5","",10,0,10);

   TH1F* nCLCT_wide_rank_123_layer_56 = new TH1F("nCLCT_wide_rank_123_layer_56","",10,0,10);
   TH1F* nCLCT_narrow_rank_123_layer_56 = new TH1F("nCLCT_narrow_rank_123_layer_56","",10,0,10);

   TH1F* nCLCT_wide_rank_123_layer_4 = new TH1F("nCLCT_wide_rank_123_layer_4","",10,0,10);
   TH1F* nCLCT_narrow_rank_123_layer_4 = new TH1F("nCLCT_narrow_rank_123_layer_4","",10,0,10);

   TH1F* nCLCT_wide_rank_45_layer_56 = new TH1F("nCLCT_wide_rank_45_layer_56","",10,0,10);
   TH1F* nCLCT_narrow_rank_45_layer_56 = new TH1F("nCLCT_narrow_rank_45_layer_56","",10,0,10);

   TH1F* nSegPerChamber = new TH1F("nSegPerChamebr","",10,0,10); 
   TH1F* nRHPerSeg = new TH1F("nRHPerSeg","",7,0,7);
   TH1F* chi2PerDOF = new TH1F("chi2PerDOF","",100,0,200);

   TH2F* nWireDigi_Layer = new TH2F("nWireDigi_Layer","",10,0,10,6,1,7);
   TH2F* nStripDigi_Layer = new TH2F("nStripDigi_Layer","",10,0,10,6,1,7);
   TH2F* nComparatorDigi_Layer = new TH2F("nComparatorDigi_Layer","",10,0,10,6,1,7);

   TH2F* wireTime_comTime = new TH2F("wireTime_comTime","",16,0,16,16,0,16);

   TH2F* wireTime_comTime_l1 = new TH2F("wireTime_comTime_l1","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_l2 = new TH2F("wireTime_comTime_l2","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_l3 = new TH2F("wireTime_comTime_l3","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_l4 = new TH2F("wireTime_comTime_l4","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_l5 = new TH2F("wireTime_comTime_l5","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_l6 = new TH2F("wireTime_comTime_l6","",16,0,16,16,0,16);

   TH2F* wireTime_comTime_r1 = new TH2F("wireTime_comTime_r1","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_r2 = new TH2F("wireTime_comTime_r2","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_r3 = new TH2F("wireTime_comTime_r3","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_r4 = new TH2F("wireTime_comTime_r4","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_r5 = new TH2F("wireTime_comTime_r5","",16,0,16,16,0,16);
   TH2F* wireTime_comTime_r6 = new TH2F("wireTime_comTime_r6","",16,0,16,16,0,16);

   TH2F* deltaTime = new TH2F("deltaTime","",16,0,16,16,0,16);


   TH2F* deltaTime_l1 = new TH2F("deltaTime_l1","",16,0,16,16,0,16);
   TH2F* deltaTime_l2 = new TH2F("deltaTime_l2","",16,0,16,16,0,16);
   TH2F* deltaTime_l3 = new TH2F("deltaTime_l3","",16,0,16,16,0,16);
   TH2F* deltaTime_l4 = new TH2F("deltaTime_l4","",16,0,16,16,0,16);
   TH2F* deltaTime_l5 = new TH2F("deltaTime_l5","",16,0,16,16,0,16);
   TH2F* deltaTime_l6 = new TH2F("deltaTime_l6","",16,0,16,16,0,16);

   TH2F* deltaTime_r1 = new TH2F("deltaTime_r1","",16,0,16,16,0,16);
   TH2F* deltaTime_r2 = new TH2F("deltaTime_r2","",16,0,16,16,0,16);
   TH2F* deltaTime_r3 = new TH2F("deltaTime_r3","",16,0,16,16,0,16);
   TH2F* deltaTime_r4 = new TH2F("deltaTime_r4","",16,0,16,16,0,16);
   TH2F* deltaTime_r5 = new TH2F("deltaTime_r5","",16,0,16,16,0,16);
   TH2F* deltaTime_r6 = new TH2F("deltaTime_r6","",16,0,16,16,0,16);

   TH2F* wireTime_layer = new TH2F("wireTime_layer","",16,0,16,6,1,7);
   TH2F* comparatorTime_layer = new TH2F("comparatorTime_layer","",16,0,16,6,1,7);
   TH2F* wireTime_comparatorTime = new TH2F("wireTime_comparatorTime","",17,-1,16,17,-1,16);
   TH2F* wireTime_comparatorTime_out = new TH2F("wireTime_comparatorTime_out","",17,-1,16,17,-1,16);

   TH2F* nRH_lumi_ME11a = new TH2F("nRH_lumi_ME11a","",20,0,20,50,0,50);
   TH2F* nRH_lumi_ME11b = new TH2F("nRH_lumi_ME11b","",20,0,20,50,0,50);
   TH2F* nRH_lumi_MEx1 = new TH2F("nRH_lumi_MEx1","",20,0,20,50,0,50);
   TH2F* nRH_lumi_MEx2 = new TH2F("nRH_lumi_MEx2","",20,0,20,50,0,50);
   TH2F* nRH_lumi_ME13 = new TH2F("nRH_lumi_ME13","",20,0,20,50,0,50);

   TH2F* nSeg_lumi_ME11a = new TH2F("nSeg_lumi_ME11a","",20,0,20,20,0,20);
   TH2F* nSeg_lumi_ME11b = new TH2F("nSeg_lumi_ME11b","",20,0,20,20,0,20);
   TH2F* nSeg_lumi_MEx1 = new TH2F("nSeg_lumi_MEx1","",20,0,20,20,0,20);
   TH2F* nSeg_lumi_MEx2 = new TH2F("nSeg_lumi_MEx2","",20,0,20,20,0,20);
   TH2F* nSeg_lumi_ME13 = new TH2F("nSeg_lumi_ME13","",20,0,20,20,0,20);

   TH2F* nALCT_lumi_ME11a = new TH2F("nALCT_lumi_ME11a","",20,0,20,20,0,20);
   TH2F* nALCT_lumi_ME11b = new TH2F("nALCT_lumi_ME11b","",20,0,20,20,0,20);
   TH2F* nALCT_lumi_MEx1 = new TH2F("nALCT_lumi_MEx1","",20,0,20,20,0,20);
   TH2F* nALCT_lumi_MEx2 = new TH2F("nALCT_lumi_MEx2","",20,0,20,20,0,20);
   TH2F* nALCT_lumi_ME13 = new TH2F("nALCT_lumi_ME13","",20,0,20,20,0,20);

   TH2F* nCLCT_lumi_ME11a = new TH2F("nCLCT_lumi_ME11a","",20,0,20,20,0,20);
   TH2F* nCLCT_lumi_ME11b = new TH2F("nCLCT_lumi_ME11b","",20,0,20,20,0,20);
   TH2F* nCLCT_lumi_MEx1 = new TH2F("nCLCT_lumi_MEx1","",20,0,20,20,0,20);
   TH2F* nCLCT_lumi_MEx2 = new TH2F("nCLCT_lumi_MEx2","",20,0,20,20,0,20);
   TH2F* nCLCT_lumi_ME13 = new TH2F("nCLCT_lumi_ME13","",20,0,20,20,0,20);

   TH2F* nLCT_lumi_ME11a = new TH2F("nLCT_lumi_ME11a","",20,0,20,20,0,20);
   TH2F* nLCT_lumi_ME11b = new TH2F("nLCT_lumi_ME11b","",20,0,20,20,0,20);
   TH2F* nLCT_lumi_MEx1 = new TH2F("nLCT_lumi_MEx1","",20,0,20,20,0,20);
   TH2F* nLCT_lumi_MEx2 = new TH2F("nLCT_lumi_MEx2","",20,0,20,20,0,20);
   TH2F* nLCT_lumi_ME13 = new TH2F("nLCT_lumi_ME13","",20,0,20,20,0,20);

   TH1F* OneSeg_1WideCLCT = new TH1F("OneSeg_1WideCLCT","",8,0,8);
   TH1F* OneSeg_1WideALCT = new TH1F("OneSeg_1WideALCT","",7,0,7);

   TH1F* FourSeg_2WideCLCT = new TH1F("FourSeg_2WideCLCT","",8,0,8);
   TH1F* FourSeg_2WideCLCT_l6 = new TH1F("FourSeg_2WideCLCT_l6","",8,0,8);
   TH1F* FourSeg_2WideCLCT_l5 = new TH1F("FourSeg_2WideCLCT_l5","",8,0,8);
   TH1F* FourSeg_2WideCLCT_l4 = new TH1F("FourSeg_2WideCLCT_l4","",8,0,8);
   TH1F* FourSeg_2WideCLCT_l3 = new TH1F("FourSeg_2WideCLCT_l3","",8,0,8);
   TH1F* FourSeg_2WideCLCT_all = new TH1F("FourSeg_2WideCLCT_all","",8,0,8);
   TH1F* FourSeg_2WideCLCT_dn = new TH1F("FourSeg_2WideCLCT_dn","",8,0,8);
   TH1F* FourSeg_2WideCLCT_up = new TH1F("FourSeg_2WideCLCT_up","",8,0,8);

   TH2F* nHitsPerSeg_muonPt = new TH2F("nHitsPerSeg_muonPt","", 20, 0, 100, 3, 4, 7);
   TH2F* SegRanking_muonPt = new TH2F("SegRanking_muonPt","", 20, 0, 100, 5, 1, 6);
   TH2F* nHitsPerSeg_muonPt_old = new TH2F("nHitsPerSeg_muonPt_old","", 20, 0, 100, 3, 4, 7);
   TH2F* SegRanking_muonPt_old = new TH2F("SegRanking_muonPt_old","", 20, 0, 100, 5, 1, 6);

   int nEntry;

   TString tag;
//   TString savedir;

/*
   struct CSC1DSeg{

    int keyPos;
    int hitsPos[6];
    int hitsTime[6];
    int nHits;

   };
*/
//   bool doME11;

   TFile      *outputRootFile;

   ClassDef(cscSelector,0);

};

#endif

#ifdef cscSelector_cxx
void cscSelector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t cscSelector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef cscSelector_cxx
