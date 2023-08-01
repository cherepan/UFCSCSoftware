#define cscSelector_cxx
// The class definition in cscSelector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("cscSelector.C")
// root> T->Process("cscSelector.C","some options")
// root> T->Process("cscSelector.C+")
//


#include "cscSelector.h"
#include <TH2.h>
#include <TStyle.h>
#include <algorithm>  

#include "TMatrixDSparse.h"
#include "clib/fillMatrix.h"
#include "clib/CSCWithMuon.h"
#include "clib/scanPattern.h"

#include "clib/CSCWireSegmentPattern.h"
#include "clib/CSCStripSegmentPattern.h"

#include "libs/MuonsHelper.h"

#include "TLorentzVector.h"


/*
void cscSelector::Initialize()
{

   endcapL.clear(); stationL.clear(); ringL.clear(); chamberL.clear();

}
*/

void cscSelector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

//   nSegPerChamber = new TH1F("nSegPerChamebr","",10,0,10);
//   nRHPerSeg = new TH1F("nRHPerSeg","",7,0,7);

   TString option = GetOption();
}

void cscSelector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

}

Bool_t cscSelector::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetEntry(entry);

   vector<SegsInChamber> segs;
   segs.clear();

   for (int i = 0; i < *cscSegments_nSegments; i++) {

     int endcap = cscSegments_ID_endcap[i];
     int station = cscSegments_ID_station[i];
     int ring = cscSegments_ID_ring[i];
     int chamber = cscSegments_ID_chamber[i];
     int chamberIndex = endcap*10000 + station*1000 + ring*100 + chamber;
     bool isME11 = false;

     if ( (station == 1 && (ring==1 || ring==4) ) ) isME11 = true;

     if ( doME11 && !isME11 ) continue;
     if ( !doME11 && isME11 ) continue;

     FillSegs(i,chamberIndex,segs);
   }


   for (int i = 0; i < int(segs.size()); i++) {
     int index = segs[i].first;
     vector<int> tmpSegs = segs[i].second;
     nSegPerChamber->Fill(tmpSegs.size());
     //     std::cout<<"  Chamber INdex     "<< index << std::endl;


     for (int j = 0; j < tmpSegs.size(); j++) {
       int treeIndex = tmpSegs[j];

       if (tmpSegs.size() != 1) continue;

       chi2PerDOF->Fill(cscSegments_chi2[treeIndex]/cscSegments_nDOF[treeIndex]);

     }
   }



  
//   if (entry > 200000) return kTRUE; 
   if (entry > 20000) return kTRUE;

   if (entry%1000 == 0) cout << tag << " th task: " << entry << "/" << nEntry << endl;
   //cout << "Event: " << *Event << endl;
//   if (*Event != 698451405/*479434223*/) return kTRUE; //cout << *cscSegments_nSegments << endl;

   SaveCSCWithMuon();
   MuonsHelper();


   std::cout<<"  How many sim hits  "<< *simHits_nSimHits <<  "  and selected muons    "<<  Muons_Index.size() <<std::endl;
   for(unsigned int iSimHit =0 ;  iSimHit < *simHits_nSimHits; iSimHit ++ )
     {

     std::cout<< "#hit   "<< iSimHit << "  in chamber   "<< ChamberID(simHits_ID_endcap[iSimHit],simHits_ID_station[iSimHit],simHits_ID_ring[iSimHit],simHits_ID_chamber[iSimHit])   <<std::endl;

     }
   



   std::vector<int>    allChambersWithSegments =   allChambersWithASegment();
   for(auto chamber  : allChambersWithSegments )
     {
       std::vector<int> allsegments_in_a_chamber =   allSegmentsInChamber(chamber);
       nSegmentsPerChamber->Fill(allsegments_in_a_chamber.size());

     }

   nMuons_perEvent->Fill(Muons_Index.size());
   if(Muons_Index.size()==2)
     {
       //       std::cout<<" >>>>>>>>>>>> mass  "<< (Muon_P4(0) + Muon_P4(1)).M()<< std::endl;
       float Mass = (Muon_P4(0) + Muon_P4(1)).M();
       TwoMuons_mass_wide->Fill((Muon_P4(0) + Muon_P4(1)).M());

       if(Mass > 88 && Mass < 94 )
	 {

	   TwoMuons_mass->Fill((Muon_P4(0) + Muon_P4(1)).M());
	   //	   nSegments_Muon1->Fill(allSegments_belonging_toMuon(Muons_Index.at(0)).size());
	   //	   nSegments_Muon2->Fill(allSegments_belonging_toMuon(Muons_Index.at(1)).size());

	   Muon1_PT->Fill(Muon_P4(0).Pt());
	   Muon2_PT->Fill(Muon_P4(1).Pt());

	   for(unsigned int imu=0; imu < Muons_Index.size(); imu++)
	     {

	       int muon_index = Muons_Index.at(imu);
	       std::vector<int>  SegementsMuon = allSegments_belonging_toMuon(Muons_Index.at(imu));
	       nSegments_Muon->Fill(allSegments_belonging_toMuon(Muons_Index.at(imu)).size());
	       for(auto iseg : SegementsMuon)
		 {
		   int nrechit = allrechits_of_segment(iseg).size();
		   nRHPerSeg->Fill(nrechit);
		 }


	       std::vector<int> list_of_chambers_crossed_by_muon = Chambers_crossedByMuon( muon_index  );
	       //	       std::cout<< 	   list_of_chambers_crossed_by_muon.size()<< std::endl;
	       if(list_of_chambers_crossed_by_muon.size()!=0)	       nChambers_crossedbyMuon->Fill(list_of_chambers_crossed_by_muon.size());
	       std::cout<<" chambers crossed by reco muon #"<< imu<< std::endl;

	       for(auto  ch : list_of_chambers_crossed_by_muon)
		 {
		   std::cout<<"   "<< ch<< std::endl;

		   std::vector<int> allsegments_in_a_chamber_crossed_by_muon =   allSegmentsInChamber(ch);
		   nSegmentsPerMuonChamber->Fill(allsegments_in_a_chamber_crossed_by_muon.size());
		   nSegmentsPerMuonChamber_notBelongingToMuon->Fill(allSegments_inChamber_NOT_belonging_toMuon(ch, muon_index).size());


		   for(auto ifalseseg : allSegments_inChamber_NOT_belonging_toMuon(ch, muon_index))
		     {
		       int nrechit = allrechits_of_segment(ifalseseg).size();
		       nRHPerNonMuonSegment->Fill(nrechit);
		     }

		 }
	     }
	 }
     }

   for(unsigned int imu=0; imu < Muons_Index.size(); imu++)
     {

       std::vector<int>  MuonSegments = allSegments_belonging_toMuon(Muons_Index.at(imu));
       std::vector<int>  list_of_chambers_crossed_by_muon = Chambers_crossedByMuon(Muons_Index.at(imu));
       for(auto  ch : list_of_chambers_crossed_by_muon)
	 {
	   std::vector<int> allsegments_in_a_chamber_crossed_by_muon =   allSegmentsInChamber(ch);
	   //	   nSegmentsPerMuonChamber->Fill(allsegments_in_a_chamber_crossed_by_muon.size());
	 }

       for(auto iseg : MuonSegments)
	 {
	   int nrechit = allrechits_of_segment(iseg).size();
	   //	   nRHPerSeg->Fill(nrechit); 
	   
	 }

       //       if(testsegs.size()!=0) allrechits_of_segment(testsegs.at(0));
       for(unsigned int isegment = 0; isegment< Muon_segment_chamber.at(imu).size(); isegment++)
	 {

	   //	   std::cout<<" endcap / station / ring  / chamber "  <<  Muon_segment_endcap.at(imu).at(isegment)  << " /  "
	   //		                                              <<  Muon_segment_station.at(imu).at(isegment)  << " /  "
	   //		                                              <<  Muon_segment_ring.at(imu).at(isegment)  << " /  "
	   //                 		                              <<  Muon_segment_chamber.at(imu).at(isegment)  << std::endl;
	   int thechamber =  ChamberID(Muon_segment_endcap.at(imu).at(isegment),
				       Muon_segment_station.at(imu).at(isegment),
				       Muon_segment_ring.at(imu).at(isegment),
				       Muon_segment_chamber.at(imu).at(isegment));



	   //	   std::vector<int>  rechits_per_segment = 
	   //	   std::cout<<" Muon  segment #   "<< isegment<< "  in chamber   "<< 
	   //	     ChamberID(Muon_segment_endcap.at(imu).at(isegment), 
	   //		       Muon_segment_station.at(imu).at(isegment), 
	   //		       Muon_segment_ring.at(imu).at(isegment), 
	   //		       Muon_segment_chamber.at(imu).at(isegment))  << "  with local X/Y  " 
	   //		    << Muon_segment_localX.at(imu).at(isegment) << "   /   "<< Muon_segment_localY.at(imu).at(isegment)  << std::endl;


	   allSegments_inChamber_NOT_belonging_toMuon(thechamber, Muons_Index.at(imu));

	 }
       
     }


   std::vector<int> Selected_Muons;
   for (int i = 0; i < *muons_nMuons; i++)
     {

       //       if (!(muons_isPFMuon[i] || muons_isGlobalMuon[i] || muons_isTrackerMuon[i]) ) continue;
       if (!(abs(muons_eta[i]) < 2.4)) continue;
       //       if (!(abs(muons_dz[i])  < 1 && abs(muons_dxy[i]) < 0.5)) continue;
       //       std::cout<<"   muon #  "<< i << std::endl;
       //       for(auto j : Chambers_crossedByMuon(i)) std::cout<<"   Chambers  "<< j << std::endl;
       if (muons_pt[i] < 5) continue;
       Selected_Muons.push_back(i);

       muons_pt_resolution->Fill(gen_matchedMuon_P4(i).Pt() - Muon_P4(i).Pt());

     }

   //   std::cout<<"   CSC with muons    "<< endcapL.size() << std::endl;
   // if no CSC contains a muon segment, skip this event
   if (int(endcapL.size()) == 0) return kTRUE;

   CountObjectsInCSCs(true,true,true,true,true,false,false,false); //RH,Seg,Wire,Strip,Comparator,ALCT,CLCT,CLT

   // SOMEHOW CANNOT PROCESS ALL DIGIS TOGHETHER !!!




   //   if(Selected_Muons.size()!=0) std::cout<<"  Run/Event  "<< *Run <<  "  /  "<<   *Event << std::endl;

   //   nMuons_perEvent->Fill(Selected_Muons.size());
   //   std::cout<<"   loop over all muons   "<<endcapL.size() << std::endl;
   for (int i = 0; i < int(endcapL.size()); i++) 
     {

       int endcap_s = endcapL[i];
       int station_s = stationL[i];
       int ring_s = ringL[i];
       int chamber_s = chamberL[i];
       int muons_cross_chambers = endcap_s*10000 + station_s*1000 + ring_s*100 + chamber_s;
       int muonIndex = muIndex[i];
       //       std::cout<<"---------------------->> It should be repeat  in case of several segments in multiple chambers: muonIndex"<< muonIndex <<"    but the chamber is different  "  << muons_cross_chambers <<std::endl;
       vector<int> strips_s = stripsFromMu[i];
       sort(strips_s.begin(), strips_s.end());
       int strip_min = strips_s[0];
       int strip_max = strips_s.back();

       //       cout << strip_min << ", " << strip_max << endl;
       //cout << endcap_s << ", " << station_s << ", " << ring_s << ", " << chamber_s << ", nStrips: " << stripsFromMu[i].size() << endl;
       //if (!(endcap_s ==1 && station_s ==4 && ring_s==1 && chamber_s==2)) continue;

       // use chamber Only with n seg
       //       if (nSegmentL[i].size() != 1) continue;
       //       if (nSegmentL[i].size() != 4) continue; 
       
       //       if (nSegmentL[i].size() < 4) continue;

       int segIndex = nSegmentL[i][0];

       // fill matrix
       //cout << nWire[i].size() << ", " << nComparator[i].size() << endl;

       if (nWire[i].size() <= 0 || nComparator[i].size() <=0) continue;    

       int nWireGroups = -1;
       if (station_s == 1) nWireGroups = 48;
       if (station_s >= 1 && ring_s == 2) nWireGroups = 64;
       if (station_s == 2 && ring_s == 1) nWireGroups = 112;
       if (station_s  > 2 && ring_s == 1) nWireGroups = 96;
       //cout << "nWireGroup " <<  nWireGroups << endl;
       TMatrixDSparse wireMatrix(6,nWireGroups);
       FillWireMatrix(nWire[i], wireMatrix);
       //       wireMatrix.Print();
       int nStrips = 80;
       if (station_s == 1 && ring_s == 4) nStrips = 112;//48;
       if (station_s == 1 && ring_s == 1) nStrips = 112;//64;
       if (station_s == 1 && ring_s == 3) nStrips = 64;

       bool doStagger = true;
       if (station_s == 1 && (ring_s == 1 || ring_s == 4) ) doStagger = false;

       TMatrixDSparse comparatorMatrix(6,2*nStrips+2);
       FillComparatorMatrix(nComparator[i], comparatorMatrix, doStagger);//, strip_min, strip_max);
       //       comparatorMatrix.Print();
       //       TMatrixDSparse comparatorMatrix_full(6,2*nStrips+2);
       //       FillComparatorMatrix(nComparator[i], comparatorMatrix_full, doStagger);


       bool reverseRowIndex = false;
       //       if (station_s == 3 || station_s == 4) reverseRowIndex = true;

       //       vector<CSC1DSeg> allWireSegs = MakeScans(wireMatrix, reverseRowIndex, w_rows, w_cols, nWGsInPatterns, patternRanks_w, 4);
       vector<CSC1DSeg> allComparatorSegs; allComparatorSegs.clear();
       allComparatorSegs = MakeScans(comparatorMatrix, reverseRowIndex, s_rows, s_cols, nHalfStrips, patternRanks_s, 9);

       //       vector<CSC1DSeg> allWireSegs_old = MakeScans(wireMatrix, reverseRowIndex, w_rows_old, w_cols_old, nWGsInPatterns_old, patternRanks_w_old, 1);
       vector<CSC1DSeg> allComparatorSegs_old; allComparatorSegs_old.clear();
       allComparatorSegs_old = MakeScans(comparatorMatrix, reverseRowIndex, s_rows_old, s_cols_old, nHalfStrips_old, patternRanks_s_old, 9);

       int nclct_wide   = allComparatorSegs.size();
       int nclct_narrow = allComparatorSegs_old.size();

       if (nclct_wide == 1 && ceil((allComparatorSegs[0].keyPos-0.1)/2) >= strip_min && ceil((allComparatorSegs[0].keyPos-0.1)/2) <= strip_max)
	 nHitsPerCLCT_wide->Fill(allComparatorSegs[0].nHits);
       if (nclct_narrow == 1 && ceil((allComparatorSegs_old[0].keyPos-0.1)/2) >= strip_min && ceil((allComparatorSegs_old[0].keyPos-0.1)/2) <= strip_max)
	 nHitsPerCLCT_narrow->Fill(allComparatorSegs_old[0].nHits);



       /*
	 if (nclct_wide != 1) continue;
	 int nLayer_wide = allComparatorSegs[0].nHits;
	 int rank_wide = allComparatorSegs[0].patternRank;

	 int nclct_narrow_mod = nclct_narrow;
	 if (nclct_narrow > 1) nclct_narrow_mod = 1;

	 if (nLayer_wide==6) {
	 eff_layer6->Fill(rank_wide);
	 eff_layer6_narrow->Fill(rank_wide,nclct_narrow_mod);
	 } 

	 if (nLayer_wide==5) {
	 eff_layer5->Fill(rank_wide);
	 eff_layer5_narrow->Fill(rank_wide,nclct_narrow_mod);
	 }

	 if (nLayer_wide==4) {
	 eff_layer4->Fill(rank_wide);
	 eff_layer4_narrow->Fill(rank_wide,nclct_narrow_mod);
	 }
       */

       /*       


		bool allBelongsToRank_1_2_3 = true;
		bool allBelongsToRank_4_5 = true;
		bool allBelongsToLayer_6 = true;
		bool allBelongsToLayer_5 = true;
		bool allBelongsToLayer_4 = true;

		int CSCid = ChamberID_converter(station_s, ring_s);

		nTotal->Fill(CSCid);
		if (nclct_wide < nclct_narrow) {
		nTotal_wideHasLess->Fill(CSCid);

		//   cout << "wide: ";
		//   for (int a = 0; a < nclct_wide; a++) cout << allComparatorSegs[a].nHits << " ";
		//   cout << endl;
		//   cout << "narrow: ";
		//   for (int a = 0; a < nclct_narrow; a++) cout << allComparatorSegs_old[a].nHits << " ";
		//   cout << endl;
		//   PrintSparseMatrix(comparatorMatrix);

		}

		for (int irank=0; irank < nclct_wide; irank++) {
		if (allComparatorSegs[irank].patternRank > 2) allBelongsToRank_1_2 = false;
		if (allComparatorSegs[irank].patternRank > 3) allBelongsToRank_1_2_3 = false;
		if (allComparatorSegs[irank].patternRank < 4) allBelongsToRank_4_5 = false;
		if (allComparatorSegs[irank].nHits != 6) allBelongsToLayer_6 = false;
		if (allComparatorSegs[irank].nHits != 5) allBelongsToLayer_5 = false;
		if (allComparatorSegs[irank].nHits != 4) allBelongsToLayer_4 = false;
		}
   
		nCLCT_wide->Fill(CSCid,nclct_wide);
		nCLCT_narrow->Fill(CSCid,nclct_narrow);

		if (allBelongsToRank_1_2) {
		nCLCT_wide_rank_1_2->Fill(CSCid,nclct_wide);
		nCLCT_narrow_rank_1_2->Fill(CSCid,nclct_narrow);
		}

		if (allBelongsToRank_1_2_3 && (allBelongsToLayer_6 || allBelongsToLayer_5) ) {
		nCLCT_wide_rank_123_layer_56->Fill(CSCid,nclct_wide);
		nCLCT_narrow_rank_123_layer_56->Fill(CSCid,nclct_narrow);
		}

		if (allBelongsToRank_1_2_3 && allBelongsToLayer_4) {
		nCLCT_wide_rank_123_layer_4->Fill(CSCid,nclct_wide);
		nCLCT_narrow_rank_123_layer_4->Fill(CSCid,nclct_narrow);
		//if (nclct_wide > 0 || nclct_narrow > 0)PrintSparseMatrix(comparatorMatrix);
		}

		if (allBelongsToRank_4_5 && (allBelongsToLayer_6 || allBelongsToLayer_5) ) {
		nCLCT_wide_rank_45_layer_56->Fill(CSCid,nclct_wide);
		nCLCT_narrow_rank_45_layer_56->Fill(CSCid,nclct_narrow);
		if (nclct_wide > 0 || nclct_narrow > 0) PrintSparseMatrix(comparatorMatrix);
		}

		if (allBelongsToLayer_6) {
		nCLCT_wide_layer_6->Fill(CSCid,nclct_wide);
		nCLCT_narrow_layer_6->Fill(CSCid,nclct_narrow);
		}

		if (allBelongsToLayer_5) {
		nCLCT_wide_layer_5->Fill(CSCid,nclct_wide);
		nCLCT_narrow_layer_5->Fill(CSCid,nclct_narrow);
		}
       */
       /*
	 cout << allComparatorSegs.size() << ", " << allComparatorSegs_old.size() << endl;
	 cout << strip_min << ", " << strip_max << endl;
	 if (allComparatorSegs.size()==2 && allComparatorSegs_old.size()==2) {
	 PrintSparseMatrix(comparatorMatrix_full); cout << endl;
	 PrintSparseMatrix(comparatorMatrix);
	 }
       */





       /* 1 wide com seg 

	  if (allComparatorSegs.size() == 1 && allComparatorSegs[0].patternRank == 1) {
          if (int(allComparatorSegs_old.size()) == 0) {
	  OneSeg_1WideCLCT->Fill(0);
	  cout << "Event: " << *Event << endl;
	  cout << endcap_s << ", " << station_s << ", " << ring_s << ", " << chamber_s << endl;
	  PrintSparseMatrix(comparatorMatrix);
	  cout << endl;
	  }
          if (int(allComparatorSegs_old.size()) == 1) OneSeg_1WideCLCT->Fill(allComparatorSegs_old[0].patternRank);
          if (int(allComparatorSegs_old.size()) > 1) {
	  int nRank1 = 0;
	  for (int r = 0; r < int(allComparatorSegs_old.size()); r++) {if (allComparatorSegs_old[r].patternRank==1) nRank1++;}
	  if (nRank1 == 0) OneSeg_1WideCLCT->Fill(6);
	  else {OneSeg_1WideCLCT->Fill(7); PrintSparseMatrix(comparatorMatrix);}
	  }
	  }

	  double muonPt = muons_pt[muonIndex];

	  if (allComparatorSegs.size() == 1) {
          nHitsPerSeg_muonPt->Fill(muonPt, allComparatorSegs[0].nHits);
          SegRanking_muonPt->Fill(muonPt, allComparatorSegs[0].patternRank);
          }

	  if (allComparatorSegs_old.size() == 1) {
          nHitsPerSeg_muonPt_old->Fill(muonPt, allComparatorSegs_old[0].nHits);
          SegRanking_muonPt_old->Fill(muonPt, allComparatorSegs_old[0].patternRank);
          }
       */

       /* 2 wide com seg

	  if (allWireSegs.size() == 2 && allComparatorSegs.size() == 2) {

          int pRank_wide_1 = allComparatorSegs[0].patternRank;
          int pRank_wide_2 = allComparatorSegs[1].patternRank;

          if (pRank_wide_1 == 1 && pRank_wide_2 == 1) FourSeg_2WideCLCT_all->Fill(1);
          if (pRank_wide_1 == 1 && pRank_wide_2 > 1) FourSeg_2WideCLCT_all->Fill(pRank_wide_2);
          if (pRank_wide_1 > 1 && pRank_wide_2 == 1) FourSeg_2WideCLCT_all->Fill(pRank_wide_1);

          }

	  if (allWireSegs.size() == 2 && allComparatorSegs.size() == 2 && allComparatorSegs_old.size() == 1) {

          int pRank_1 = allComparatorSegs_old[0].patternRank;
          int keyPos_1 = allComparatorSegs_old[0].keyPos;
        
	  //          if (pRank_1 > 1) continue;        
 
          int pRank_wide_1 = allComparatorSegs[0].patternRank; 
          int keyPos_wide_1 = allComparatorSegs[0].keyPos;
          int nHits_wide_1 = allComparatorSegs[0].nHits;

          int pRank_wide_2 = allComparatorSegs[1].patternRank;
          int keyPos_wide_2 = allComparatorSegs[1].keyPos;
          int nHits_wide_2 = allComparatorSegs[1].nHits;


	  //cout << "wide: " << pRank_wide_1 << ", " << pRank_wide_2 << endl;
	  //cout << "widePos: " << keyPos_wide_1 << ", " << keyPos_wide_2 << endl;
	  //cout << "old: " << pRank_1 << endl;
	  //cout << "oldPos: " << keyPos_1 << endl;
	  //
          if (pRank_wide_1 > 1 && pRank_wide_2 > 1) continue;

	  //PrintSparseMatrix(comparatorMatrix);

          if (abs(keyPos_1-keyPos_wide_1) <= 1 && pRank_wide_1 == 1) {
	  FourSeg_2WideCLCT->Fill(pRank_wide_2);
	  if (nHits_wide_2 == 6) FourSeg_2WideCLCT_l6->Fill(pRank_wide_2);
	  if (nHits_wide_2 == 5) FourSeg_2WideCLCT_l5->Fill(pRank_wide_2);
	  if (nHits_wide_2 == 4) FourSeg_2WideCLCT_l4->Fill(pRank_wide_2);
	  //             if (nHits_wide_2 == 3) FourSeg_2WideCLCT_l3->Fill(pRank_wide_2);

	  //             if (pRank_wide_2 == 1) PrintSparseMatrix(comparatorMatrix);
	  //             if (abs(keyPos_1-keyPos_wide_2) <= 1) PrintSparseMatrix(comparatorMatrix);
	  }

          if (abs(keyPos_1-keyPos_wide_2) <= 1 && pRank_wide_2 == 1) {
	  FourSeg_2WideCLCT->Fill(pRank_wide_1);
	  if (nHits_wide_1 == 6) FourSeg_2WideCLCT_l6->Fill(pRank_wide_1);
	  if (nHits_wide_1 == 5) FourSeg_2WideCLCT_l5->Fill(pRank_wide_1);
	  if (nHits_wide_1 == 4) FourSeg_2WideCLCT_l4->Fill(pRank_wide_1);
	  //             if (pRank_wide_1 == 1) PrintSparseMatrix(comparatorMatrix);

	  //             if (abs(keyPos_1-keyPos_wide_1) <= 1) PrintSparseMatrix(comparatorMatrix);
	  }

          }



	  if (allWireSegs.size() == 2 && allComparatorSegs.size() == 2 && allComparatorSegs_old.size() == 2) {

          int pRank_1 = allComparatorSegs_old[0].patternRank;
          int keyPos_1 = allComparatorSegs_old[0].keyPos;
          int pRank_2 = allComparatorSegs_old[1].patternRank;
          int keyPos_2 = allComparatorSegs_old[1].keyPos;

          int pRank_wide_1 = allComparatorSegs[0].patternRank;
          int keyPos_wide_1 = allComparatorSegs[0].keyPos;
          int pRank_wide_2 = allComparatorSegs[1].patternRank;
          int keyPos_wide_2 = allComparatorSegs[1].keyPos;

          if (pRank_wide_1 == 1 && abs(keyPos_wide_1-keyPos_1) <= 1 && pRank_2 > pRank_wide_2 && abs(keyPos_wide_2-keyPos_2) <= 1) FourSeg_2WideCLCT_dn->Fill(pRank_wide_2);
          if (pRank_wide_2 == 1 && abs(keyPos_wide_2-keyPos_2) <= 1 && pRank_1 > pRank_wide_1 && abs(keyPos_wide_1-keyPos_1) <= 1) FourSeg_2WideCLCT_dn->Fill(pRank_wide_1);

          if (pRank_wide_1 == 1 && abs(keyPos_wide_1-keyPos_1) <= 1 && pRank_2 < pRank_wide_2 && abs(keyPos_wide_2-keyPos_2) <= 1) {
	  FourSeg_2WideCLCT_up->Fill(pRank_wide_2); //PrintSparseMatrix(comparatorMatrix);
	  }

          if (pRank_wide_2 == 1 && abs(keyPos_wide_2-keyPos_2) <= 1 && pRank_1 < pRank_wide_1 && abs(keyPos_wide_1-keyPos_1) <= 1) {
	  FourSeg_2WideCLCT_up->Fill(pRank_wide_1); //PrintSparseMatrix(comparatorMatrix);
	  }

          }

       */


       /* print out and check
	  if (allComparatorSegs.size()==2 && allComparatorSegs_old.size()==1) 
	  {
	  // cout << "nWireSeg: " << allWireSegs.size() << ", nStripSeg: " << allComparatorSegs.size() << ", nWireSeg_old: " << allWireSegs_old.size() << ", nStripSeg_old: " << allComparatorSegs_old.size() << endl;

	  cout << "wide pattern ranks: " << allComparatorSegs[0].patternRank << " and " << allComparatorSegs[1].patternRank << endl;
	  cout << "narrow pattern ranks: " << allComparatorSegs_old[0].patternRank << endl;

	  PrintSparseMatrix(comparatorMatrix);

	  }

       */

       /*
	 if (int(allWireSegs.size()) != 1 || int(allComparatorSegs.size()) != 1) continue;
	 CSC1DSeg wireSeg = allWireSegs[0];
	 CSC1DSeg comSeg = allComparatorSegs[0];
	 if (wireSeg.nHits != 6 || comSeg.nHits != 6) continue;

	 wireTime_comTime->Fill(wireSeg.MeanTime(), comSeg.MeanTime());
 
	 wireTime_comTime_l1->Fill((wireSeg.hitsTime)[0], (comSeg.hitsTime)[0]);
	 wireTime_comTime_l2->Fill((wireSeg.hitsTime)[1], (comSeg.hitsTime)[1]);
	 wireTime_comTime_l3->Fill((wireSeg.hitsTime)[2], (comSeg.hitsTime)[2]);
	 wireTime_comTime_l4->Fill((wireSeg.hitsTime)[3], (comSeg.hitsTime)[3]);
	 wireTime_comTime_l5->Fill((wireSeg.hitsTime)[4], (comSeg.hitsTime)[4]);
	 wireTime_comTime_l6->Fill((wireSeg.hitsTime)[5], (comSeg.hitsTime)[5]);

	 vector<int> sortedWireTime = wireSeg.SortedTime();
	 vector<int> sortedComTime = comSeg.SortedTime();

	 wireTime_comTime_r1->Fill(sortedWireTime[0],sortedComTime[0]); 
	 wireTime_comTime_r2->Fill(sortedWireTime[1],sortedComTime[1]);
	 wireTime_comTime_r3->Fill(sortedWireTime[2],sortedComTime[2]);
	 wireTime_comTime_r4->Fill(sortedWireTime[3],sortedComTime[3]);
	 wireTime_comTime_r5->Fill(sortedWireTime[4],sortedComTime[4]);
	 wireTime_comTime_r6->Fill(sortedWireTime[5],sortedComTime[5]);


	 // if having 2 wire and strip segs
	 if (int(allWireSegs.size()) != 2 || int(allComparatorSegs.size()) != 2) continue; 
	 CSC1DSeg wireSeg1 = allWireSegs[0];
	 CSC1DSeg wireSeg2 = allWireSegs[1];
	 CSC1DSeg comSeg1 = allComparatorSegs[0];
	 CSC1DSeg comSeg2 = allComparatorSegs[1];

	 if (wireSeg1.nHits != 6 || comSeg1.nHits != 6 || wireSeg2.nHits != 6 || comSeg2.nHits != 6) continue;

	 vector<int> sortedWireTime1 = wireSeg1.SortedTime();
	 vector<int> sortedComTime1 = comSeg1.SortedTime();
	 vector<int> sortedWireTime2 = wireSeg2.SortedTime();
	 vector<int> sortedComTime2 = comSeg2.SortedTime();

	 cout << sortedWireTime1[2] << ", " << sortedComTime1[2] << ", " << sortedWireTime2[2] << ", " << sortedComTime2[2] << endl;

	 if ( ! (  sortedWireTime1[2] >=7 && sortedWireTime1[2] <= 11 && sortedComTime1[2] >= 6 && sortedComTime1[2] <=10 &&
	 sortedWireTime2[2] >=7 && sortedWireTime2[2] <= 11 && sortedComTime2[2] >= 6 && sortedComTime2[2] <=10) ) continue; 
	 cout << "here" << endl;            
	 deltaTime->Fill(abs(wireSeg1.MeanTime()-wireSeg2.MeanTime()), abs(comSeg1.MeanTime()-comSeg2.MeanTime()));

	 deltaTime_l1->Fill(abs((wireSeg1.hitsTime)[0]-(wireSeg2.hitsTime)[0]), abs((comSeg1.hitsTime)[0]-(comSeg2.hitsTime)[0]));
	 deltaTime_l2->Fill(abs((wireSeg1.hitsTime)[1]-(wireSeg2.hitsTime)[1]), abs((comSeg1.hitsTime)[1]-(comSeg2.hitsTime)[1]));
	 deltaTime_l3->Fill(abs((wireSeg1.hitsTime)[2]-(wireSeg2.hitsTime)[2]), abs((comSeg1.hitsTime)[2]-(comSeg2.hitsTime)[2]));
	 deltaTime_l4->Fill(abs((wireSeg1.hitsTime)[3]-(wireSeg2.hitsTime)[3]), abs((comSeg1.hitsTime)[3]-(comSeg2.hitsTime)[3]));
	 deltaTime_l5->Fill(abs((wireSeg1.hitsTime)[4]-(wireSeg2.hitsTime)[4]), abs((comSeg1.hitsTime)[4]-(comSeg2.hitsTime)[4]));
	 deltaTime_l6->Fill(abs((wireSeg1.hitsTime)[5]-(wireSeg2.hitsTime)[5]), abs((comSeg1.hitsTime)[5]-(comSeg2.hitsTime)[5]));

	 deltaTime_r1->Fill(abs(sortedWireTime1[0]-sortedWireTime2[0]), abs(sortedComTime1[0]-sortedComTime2[0]));       
	 deltaTime_r2->Fill(abs(sortedWireTime1[1]-sortedWireTime2[1]), abs(sortedComTime1[1]-sortedComTime2[1]));
	 deltaTime_r3->Fill(abs(sortedWireTime1[2]-sortedWireTime2[2]), abs(sortedComTime1[2]-sortedComTime2[2]));
	 deltaTime_r4->Fill(abs(sortedWireTime1[3]-sortedWireTime2[3]), abs(sortedComTime1[3]-sortedComTime2[3]));
	 deltaTime_r5->Fill(abs(sortedWireTime1[4]-sortedWireTime2[4]), abs(sortedComTime1[4]-sortedComTime2[4]));
	 deltaTime_r6->Fill(abs(sortedWireTime1[5]-sortedWireTime2[5]), abs(sortedComTime1[5]-sortedComTime2[5]));
       */
       //cout << "endcap: " << endcap_s << ", station: " << station_s << ", ring: " << ring_s << ", chamber: " << chamber_s << endl;
       //cout << "nWireSeg: " << allWireSegs.size() << endl;
       //cout << "nStripSeg: " << allComparatorSegs.size() << endl;

     }//loop over chambers with muon

   return kTRUE;


}

void cscSelector::SlaveTerminate()
{
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

}

void cscSelector::Terminate()
{
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

  TCanvas *c1 = new TCanvas("c1", "", 800,800);//200,10,400,400);
  outputRootFile = new TFile("tmpRootPlots/CSCresults_" + tag + ".root","RECREATE");
  outputRootFile->cd();



  nMuons_perEvent->Write();


  nHitsPerCLCT_narrow->Write();
  nHitsPerCLCT_wide->Write();
  eff_layer6->Write();
  eff_layer5->Write();
  eff_layer4->Write();
  eff_layer6_narrow->Write();
  eff_layer5_narrow->Write();
  eff_layer4_narrow->Write();
   
   
  nTotal->Write();
  nTotal_wideHasLess->Write();
   
  nCLCT_wide_rank_123_layer_56->Write();
  nCLCT_narrow_rank_123_layer_56->Write();
   
  nCLCT_wide_rank_123_layer_4->Write();
  nCLCT_narrow_rank_123_layer_4->Write();
   
  nCLCT_wide_rank_45_layer_56->Write();
  nCLCT_narrow_rank_45_layer_56->Write();
   
  nCLCT_wide->Write();
  nCLCT_narrow->Write();

  nCLCT_wide_rank_1_2->Write();
  nCLCT_narrow_rank_1_2->Write();
  nCLCT_wide_layer_6->Write();
  nCLCT_narrow_layer_6->Write();
  nCLCT_wide_layer_5->Write();
  nCLCT_narrow_layer_5->Write();

  nSegPerChamber->SetMaximum(2000);
  nRHPerSeg->SetMaximum(2000);
  //  nSegPerChamber->Write();
  TwoMuons_mass->Write();
  TwoMuons_mass_wide->Write();
  nSegments_Muon->Write();


  Muon1_PT->Write();
  Muon2_PT->Write();

  muons_pt_resolution->Write();

  nChambers_crossedbyMuon->Write();
  nSegmentsPerMuonChamber_notBelongingToMuon->Write();
  nRHPerSeg->Write();
  nRHPerNonMuonSegment->Write();
  chi2PerDOF->SetMinimum(0.1);
  chi2PerDOF->Write();
   
  nSegmentsPerMuonChamber -> Write();
  nSegmentsPerChamber -> Write();

  /*
    nHitsPerSeg_muonPt->Write();
    SegRanking_muonPt->Write();
    nHitsPerSeg_muonPt_old->Write();
    SegRanking_muonPt_old->Write();

    OneSeg_1WideCLCT->Write();
    FourSeg_2WideCLCT->Write();
    FourSeg_2WideCLCT_all->Write();
    FourSeg_2WideCLCT_up->Write();
    FourSeg_2WideCLCT_dn->Write();
    FourSeg_2WideCLCT_l6->Write();
    FourSeg_2WideCLCT_l5->Write();
    FourSeg_2WideCLCT_l4->Write();
    FourSeg_2WideCLCT_l3->Write();

    //c1->SetLogy();
    //chi2PerDOF->SetMinimum(0.1);
    nSegPerChamber->SetMaximum(9000);
    nRHPerSeg->SetMaximum(8000);
    nSegPerChamber->Write();
    nRHPerSeg->Write();
    //   chi2PerDOF->Write();
    nWireDigi_Layer->Write();
    nStripDigi_Layer->Write();
    nComparatorDigi_Layer->Write();

    wireTime_layer->Write();
    comparatorTime_layer->Write();
    wireTime_comparatorTime->Write();
    wireTime_comparatorTime_out->Write();

    wireTime_comTime->Write();

    wireTime_comTime_l1->Write();
    wireTime_comTime_l2->Write();
    wireTime_comTime_l3->Write();
    wireTime_comTime_l4->Write();
    wireTime_comTime_l5->Write();
    wireTime_comTime_l6->Write();

    wireTime_comTime_r1->Write();
    wireTime_comTime_r2->Write();
    wireTime_comTime_r3->Write();
    wireTime_comTime_r4->Write();
    wireTime_comTime_r5->Write();
    wireTime_comTime_r6->Write();

    deltaTime->Write();

    deltaTime_l1->Write();
    deltaTime_l2->Write();
    deltaTime_l3->Write();
    deltaTime_l4->Write();
    deltaTime_l5->Write();
    deltaTime_l6->Write();

    deltaTime_r1->Write();
    deltaTime_r2->Write();
    deltaTime_r3->Write();
    deltaTime_r4->Write();
    deltaTime_r5->Write();
    deltaTime_r6->Write();

    nRH_lumi_ME11a->Write();
    nRH_lumi_ME11b->Write();
    nRH_lumi_MEx1->Write();
    nRH_lumi_MEx2->Write();
    nRH_lumi_ME13->Write();

    nSeg_lumi_ME11a->Write();
    nSeg_lumi_ME11b->Write();
    nSeg_lumi_MEx1->Write();
    nSeg_lumi_MEx2->Write();
    nSeg_lumi_ME13->Write();

    nALCT_lumi_ME11a->Write();
    nALCT_lumi_ME11b->Write();
    nALCT_lumi_MEx1->Write();
    nALCT_lumi_MEx2->Write();
    nALCT_lumi_ME13->Write();

    nCLCT_lumi_ME11a->Write();
    nCLCT_lumi_ME11b->Write();
    nCLCT_lumi_MEx1->Write();
    nCLCT_lumi_MEx2->Write();
    nCLCT_lumi_ME13->Write();

    nLCT_lumi_ME11a->Write();
    nLCT_lumi_ME11b->Write();
    nLCT_lumi_MEx1->Write();
    nLCT_lumi_MEx2->Write();
    nLCT_lumi_ME13->Write();
  */
  outputRootFile->Close();

  cout << "root file " << outputRootFile->GetName() << " made " << endl;
  //   nSegPerChamber->Draw("hist");
  //   nRHPerSeg->Draw("hist");
  //   chi2PerDOF->Draw("hist");
  //   c1->SaveAs(savedir + "chi2PerDOF_" + tag + ".png");
  //   c1->SaveAs(savedir + "chi2PerDOF_" + tag + ".pdf");



  //   c1->SaveAs(savedir + "nSegsPerChamber_" + tag + ".png");
  //   c1->SaveAs(savedir + "nSegsPerChamber_" + tag + ".pdf");
  //   c1->SaveAs(savedir + "nRHPerSeg_" + tag + ".png");
  //   c1->SaveAs(savedir + "nRHPerSeg_" + tag + ".pdf");

}



// user defined function

void cscSelector::SetInputs(int nEntry_, TString tag_)//, TString savedir_, bool doME11_)
{

  nEntry = nEntry_;


  tag = tag_;

  //     savedir = savedir_;
  //     doME11 = doME11_;

}

TLorentzVector  
cscSelector::Muon_P4(unsigned int i)
{
  return TLorentzVector(muons_px[i],muons_py[i],muons_pz[i],muons_energy[i]);
}



std::vector<int> cscSelector::Chambers_crossedByMuon(unsigned int i)
{

  std::vector<int> out;
  for (int j = 0; j < int(muons_cscSegmentRecord_endcap[i].size()); j++)
    {
      int endcap  = muons_cscSegmentRecord_endcap[i][j];
      int station = muons_cscSegmentRecord_station[i][j];
      int ring    = muons_cscSegmentRecord_ring[i][j];
      int chamber = muons_cscSegmentRecord_chamber[i][j];

      out.push_back(ChamberID(endcap,station,ring,chamber));
    }	  
  return out;
}



int cscSelector::ChamberID(int endcap, int station, int ring, int chamber)
{
  return endcap*10000 + station*1000 + ring*100 + chamber;

}

bool cscSelector::CheckCommon( std::vector< int > inVectorA, std::vector< int > inVectorB )
{
  std::vector< int > *lower, *higher;

  size_t sizeL = 0, sizeH = 0;

  if( inVectorA.size() > inVectorB.size() )
    {
      lower = &inVectorA;
      sizeL = inVectorA.size();
      higher = &inVectorB;
      sizeH = inVectorB.size();
    }
  else
    {
      lower = &inVectorB;
      sizeL = inVectorB.size();
      higher = &inVectorA;
      sizeH = inVectorA.size();
    }

  size_t indexL = 0, indexH = 0;

  for( ; indexH < sizeH; indexH++ )
    {
      bool exists = std::binary_search( lower->begin(), lower->end(), higher->at(indexH) );

      if( exists == true )
	return true;
      else
	continue;
    }
  return false;
}




void cscSelector::FillSegs(int segIndex, int chamberIndex, vector<SegsInChamber> &segs)
{

  if (int(segs.size()) == 0) {

    vector<int> tmpIndex; tmpIndex.push_back(segIndex);
    segs.push_back(make_pair(chamberIndex,tmpIndex));

  } else {

    int savedIndex = -1;
    for (int j = 0; j < int(segs.size()); j++) {
      if (segs[j].first == chamberIndex) savedIndex = j;
    }

    if (savedIndex >= 0) {

      segs[savedIndex].second.push_back(segIndex);

    } else {

      vector<int> tmpIndex2; tmpIndex2.push_back(segIndex);
      segs.push_back(make_pair(chamberIndex,tmpIndex2));

    }

  }


}




/*
  void cscSelector::MakeWireMatrix()
  {


  }
*/
void cscSelector::CountObjectsInCSCs(bool doRH, bool doSeg, 
                                     bool doWire, bool doStrip, bool doComparator, 
                                     bool doALCT, bool doCLCT, bool doLCT)
{

  // count number of seg/alct/clct/lct in CSCs with muon segment

  for (int i = 0; i < int(endcapL.size()); i++) {

    int endcap = endcapL[i];
    int station = stationL[i];
    int ring = ringL[i];
    int chamber = chamberL[i];

    if (doRH) {
      nRH[i].clear();
      for (int j = 0; j < *recHits2D_nRecHits2D; j++) {
	int endcap_rh = recHits2D_ID_endcap[j]; 
	int station_rh = recHits2D_ID_station[j];
	int ring_rh = recHits2D_ID_ring[j];
	int chamber_rh = recHits2D_ID_chamber[j];

	if (endcap==endcap_rh && station == station_rh && ring == ring_rh && chamber == chamber_rh) nRH[i].push_back(j);// += 1;
      }
    }

    if (doSeg) {
      nSegmentL[i].clear();
      for (int j = 0; j < *cscSegments_nSegments; j++) {
	int endcap_s = cscSegments_ID_endcap[j]; 
	int station_s = cscSegments_ID_station[j];
	int ring_s = cscSegments_ID_ring[j];
	int chamber_s = cscSegments_ID_chamber[j];

	if (endcap==endcap_s && station == station_s && ring == ring_s && chamber == chamber_s) nSegmentL[i].push_back(j); // += 1;
      }
    }

    if (doWire) {
      nWire[i].clear();
      for (int j = 0; j < *firedWireDigis_nWireDigis; j++) {

	int endcap_w = firedWireDigis_ID_endcap[j];
	int station_w = firedWireDigis_ID_station[j];
	int ring_w = firedWireDigis_ID_ring[j];
	int chamber_w = firedWireDigis_ID_chamber[j];

	if (endcap==endcap_w && station == station_w && ring == ring_w && chamber == chamber_w) nWire[i].push_back(j); // += 1;
      }
    }

    if (doStrip) {
      nStrip[i].clear();
      for (int j = 0; j < *firedStripDigis_nStripDigis; j++) {
	int endcap_sp = firedStripDigis_ID_endcap[j];
	int station_sp = firedStripDigis_ID_station[j];
	int ring_sp = firedStripDigis_ID_ring[j];
	int chamber_sp = firedStripDigis_ID_chamber[j];

	if (endcap==endcap_sp && station == station_sp && ring == ring_sp && chamber == chamber_sp) nStrip[i].push_back(j); // += 1;
      }
    }

    if (doComparator) {
      nComparator[i].clear();
      for (int j = 0; j < *comparatorDigis_nDigis; j++) {
	int endcap_c = comparatorDigis_ID_endcap[j];
	int station_c = comparatorDigis_ID_station[j];
	int ring_c = comparatorDigis_ID_ring[j];
	int chamber_c = comparatorDigis_ID_chamber[j];

	if (endcap==endcap_c && station == station_c && ring == ring_c && chamber == chamber_c) nComparator[i].push_back(j); // += 1;
      }
    }
    /*
      if (doALCT) {
      nALCT[i].clear();
      for (int j = 0; j < *alct_nAlcts; j++) {
      int endcap_alct = alct_ID_endcap[j];
      int station_alct = alct_ID_station[j];
      int ring_alct = alct_ID_ring[j];
      int chamber_alct = alct_ID_chamber[j];

      if (endcap==endcap_alct && station == station_alct && ring == ring_alct && chamber == chamber_alct) nALCT[i].push_back(j);// += 1;
      }
      }

      if (doCLCT) {
      nCLCT[i].clear();
      for (int j = 0; j < *clct_nClcts; j++) {
      int endcap_clct = clct_ID_endcap[j];
      int station_clct = clct_ID_station[j];
      int ring_clct = clct_ID_ring[j];
      int chamber_clct = clct_ID_chamber[j];

      if (endcap==endcap_clct && station == station_clct && ring == ring_clct && chamber == chamber_clct) nCLCT[i].push_back(j);// += 1;
      }
      }

      if (doLCT) {
      nLCT[i].clear();
      for (int j = 0; j < *correlatedLct_nLcts; j++) {
      int endcap_lct = correlatedLct_ID_endcap[j];
      int station_lct = correlatedLct_ID_station[j];
      int ring_lct = correlatedLct_ID_ring[j];
      int chamber_lct = correlatedLct_ID_chamber[j];

      if (endcap==endcap_lct && station == station_lct && ring == ring_lct && chamber == chamber_lct) nLCT[i].push_back(j);// += 1;
      }
      }
    */
  }


  /*   
       for (int i = 0; i < int(endcapL.size()); i++) {

       // select chamber

       int endcap_s = endcapL[i];
       int station_s = stationL[i];
       int ring_s = ringL[i];
       int chamber_s = chamberL[i];

       if (station_s == 1 && ring_s == 4) {
       nRH_lumi_ME11a->Fill(*instLumi, nRH[i].size() );
       nSeg_lumi_ME11a->Fill(*instLumi, nSegmentL[i].size() );
       nALCT_lumi_ME11a->Fill(*instLumi, nALCT[i].size() );
       nCLCT_lumi_ME11a->Fill(*instLumi, nCLCT[i].size() );
       nLCT_lumi_ME11a->Fill(*instLumi, nLCT[i].size() );
       }

       if (station_s == 1 && ring_s == 1) {
       nRH_lumi_ME11b->Fill(*instLumi, nRH[i].size() );
       nSeg_lumi_ME11b->Fill(*instLumi, nSegmentL[i].size() );
       nALCT_lumi_ME11b->Fill(*instLumi, nALCT[i].size() );
       nCLCT_lumi_ME11b->Fill(*instLumi, nCLCT[i].size() );
       nLCT_lumi_ME11b->Fill(*instLumi, nLCT[i].size() );
       }

       if (station_s != 1 && ring_s == 1) {
       nRH_lumi_MEx1->Fill(*instLumi, nRH[i].size() );
       nSeg_lumi_MEx1->Fill(*instLumi, nSegmentL[i].size() );
       nALCT_lumi_MEx1->Fill(*instLumi, nALCT[i].size() );
       nCLCT_lumi_MEx1->Fill(*instLumi, nCLCT[i].size() );
       nLCT_lumi_MEx1->Fill(*instLumi, nLCT[i].size() );
       }

       if (ring_s == 2) {
       nRH_lumi_MEx2->Fill(*instLumi, nRH[i].size() );
       nSeg_lumi_MEx2->Fill(*instLumi, nSegmentL[i].size() );
       nALCT_lumi_MEx2->Fill(*instLumi, nALCT[i].size() );
       nCLCT_lumi_MEx2->Fill(*instLumi, nCLCT[i].size() );
       nLCT_lumi_MEx2->Fill(*instLumi, nLCT[i].size() );
       }

       if (ring_s == 3) {
       nRH_lumi_ME13->Fill(*instLumi, nRH[i].size() );
       nSeg_lumi_ME13->Fill(*instLumi, nSegmentL[i].size() );
       nALCT_lumi_ME13->Fill(*instLumi, nALCT[i].size() );
       nCLCT_lumi_ME13->Fill(*instLumi, nCLCT[i].size() );
       nLCT_lumi_ME13->Fill(*instLumi, nLCT[i].size() );
       }

       }
  */
}


void cscSelector::PrintSparseMatrix(TMatrixDSparse inputMatrix) 
{

  int * rowIndex = inputMatrix.GetRowIndexArray();
  int * colIndex = inputMatrix.GetColIndexArray();
  double * pData = inputMatrix.GetMatrixArray();

  int nRow = inputMatrix.GetNrows();
  int nCol = inputMatrix.GetNcols();

  TH2F* h_matrix = new TH2F("h_matrix","",nCol,0,nCol,nRow,0,nRow);

  for (int i = 0; i < nRow; i++) {
    int sIndex = rowIndex[i];
    int eIndex = rowIndex[i+1];
    for (int j = sIndex; j < eIndex; j++) {
      int icol = colIndex[j];
      double data = pData[j];
      //             cout << i+inputMatrix.GetRowLwb()+1 << ", " << icol+inputMatrix.GetColLwb() << ", " << data << endl;
      h_matrix->SetBinContent(icol+inputMatrix.GetColLwb(),i+inputMatrix.GetRowLwb()+1,data);
    }
  }
  //cout << h_matrix->Integral() << endl;
  WriteTH2F(h_matrix);
  //     delete h_matrix;      
}

void cscSelector::WriteTH2F(TH2F* hist) {
  //cout << hist->Integral() << endl;

  for (int i = 1; i < hist->GetNbinsY()+1; i++) {
    for (int j = 1; j < hist->GetNbinsX()+1; j++) {
      if (hist->GetBinContent(j,i)==0)
	{std::cout << "-";} else {std::cout << hist->GetBinContent(j,i)-1;}

    }
    std::cout << std::endl;
  }

}


int cscSelector::ChamberID_converter(int station, int ring) {

  int id = -1;

  if (station == 1 && ring == 4) id = 0;   
  if (station == 1 && ring == 1) id = 1;
  if (station == 1 && ring == 2) id = 2;
  if (station == 1 && ring == 3) id = 3;
  if (station == 2 && ring == 1) id = 4;
  if (station == 2 && ring == 2) id = 5;
  if (station == 3 && ring == 1) id = 6;
  if (station == 3 && ring == 2) id = 7;
  if (station == 4 && ring == 1) id = 8;
  if (station == 4 && ring == 2) id = 9;

  return id;
}



/*
std::vector<int> 
cscSelector::allSegmentsInChamber_NOT_fromMuon(unsigned int idchamber, unsigned int muon)
{
  std::vector<int> out;


  return out;
}
*/


std::vector<int> 
cscSelector::allChambersWithASegment()
{
  std::vector<int> out;
  for (unsigned int isegment = 0; isegment < *cscSegments_nSegments; isegment++)
    {
      int chamber = ChamberID(cscSegments_ID_endcap[isegment],cscSegments_ID_station[isegment],cscSegments_ID_ring[isegment],cscSegments_ID_chamber[isegment]);
      if(std::find(out.begin(), out.end(), chamber) != out.end()) continue;
      out.push_back(chamber);
    }
  return out;
}

std::vector<int>
cscSelector::allSegmentsInChamber(unsigned int idchamber)
{
  std::vector<int> out;

  int chamber = idchamber%100;
  int ring    = int(idchamber/100)%10;
  int station = int(idchamber/1000)%10;
  int endcap  = int(idchamber/10000);

  for (unsigned int isegment = 0; isegment < *cscSegments_nSegments; isegment++) 
    {
      int segment_endcap  = cscSegments_ID_endcap[isegment];
      int segment_station = cscSegments_ID_station[isegment];
      int segment_ring    = cscSegments_ID_ring[isegment];
      int segment_chamber = cscSegments_ID_chamber[isegment];
      //      std::cout<< "  >>>>>>>>>>>  In  a chamber   "<<  ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber) << "    segment # " << isegment <<"      with local  X/Y  "<< cscSegments_localX[isegment] <<" /  " << cscSegments_localY[isegment] <<std::endl;


      if( ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber) == idchamber)
	{
	  //	  std::cout<< "  >>>>>>>  In  a chamber   "<< idchamber << "    segment # " << isegment <<"      with local  X/Y  "<< cscSegments_localX[isegment] 
	  //	   <<" /  " << cscSegments_localY[isegment] <<std::endl;
	  out.push_back(isegment);
	}
    }
  
  /*  std::cout<<" decompose the chamber id---------------- endcap / station / ring  / chamber "  <<  endcap  << " /  "
	   <<  station  << " /  "
	   <<  ring  << " /  "
	   <<  chamber  << std::endl;

  */

  return out;

}



std::vector<int>  
cscSelector::allSegments_belonging_toMuon(unsigned int muon)
{


  std::vector<int> out;
  for (unsigned int isegment = 0; isegment < *cscSegments_nSegments; isegment++)
    {
      int segment_endcap     = cscSegments_ID_endcap[isegment];
      int segment_station    = cscSegments_ID_station[isegment];
      int segment_ring       = cscSegments_ID_ring[isegment];
      int segment_chamber    = cscSegments_ID_chamber[isegment];
      float segment_localX   = cscSegments_localX[isegment]; 
      float segment_localY   = cscSegments_localY[isegment];
      int chamber_of_segment = ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber);

      for (unsigned int i_muon_segment = 0; i_muon_segment < muons_cscSegmentRecord_endcap[muon].size(); i_muon_segment++)
	{
	  int muon_segment_endcap     = muons_cscSegmentRecord_endcap[muon][i_muon_segment];
	  int muon_segment_station    = muons_cscSegmentRecord_station[muon][i_muon_segment];
	  int muon_segment_ring       = muons_cscSegmentRecord_ring[muon][i_muon_segment];
	  int muon_segment_chamber    = muons_cscSegmentRecord_chamber[muon][i_muon_segment];
	  float muon_segment_localX   = muons_cscSegmentRecord_localX[muon][i_muon_segment];
	  float muon_segment_localY   = muons_cscSegmentRecord_localY[muon][i_muon_segment];
	  int muon_chamber_of_segment = ChamberID(muon_segment_endcap,muon_segment_station,muon_segment_ring,muon_segment_chamber);

	  if(muon_chamber_of_segment == chamber_of_segment   &&
	     muon_segment_localX     == segment_localX       &&
	     muon_segment_localY     == segment_localY)  
	    {
	      //	      std::cout<<" <<<<<<<<<<<<<<<<<<<<<<   check that cham,bers are different   "<< chamber_of_segment << "  seg #   "<<isegment <<"   with local X/Y   " <<segment_localX << "  \ " <<segment_localY <<std::endl;
	      out.push_back(isegment);

	    }

	}

    }
  return out;
}

std::vector<int> 
cscSelector::allrechits_of_segment(unsigned int segment)
{
  std::vector<int> out;


  int segment_endcap     = cscSegments_ID_endcap[segment];
  int segment_station    = cscSegments_ID_station[segment];
  int segment_ring       = cscSegments_ID_ring[segment];
  int segment_chamber    = cscSegments_ID_chamber[segment];
  int chamber_of_segment = ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber);


  for (unsigned int iRecHit = 0; iRecHit < cscSegments_recHitRecord_endcap[segment].size(); iRecHit++)
    {

      int chamber_of_srechit = ChamberID(cscSegments_recHitRecord_endcap[segment][iRecHit],cscSegments_recHitRecord_endcap[segment][iRecHit],cscSegments_recHitRecord_ring[segment][iRecHit],cscSegments_recHitRecord_chamber[segment][iRecHit]);
      
      //      std::cout<<"  chamber must be as of the segment   "<< chamber_of_srechit<<std::endl;
      //      std::cout<< "------------------------------   rechit in layer  "<< cscSegments_recHitRecord_layer[segment][iRecHit] << " X/Y  "<<cscSegments_recHitRecord_localX[segment][iRecHit]
      //	       <<"  \  " <<cscSegments_recHitRecord_localY[segment][iRecHit] <<std::endl;


      for (int i2DRecHit = 0; i2DRecHit < *recHits2D_nRecHits2D; i2DRecHit++)
	{

	  int layer_2DRecHit     = recHits2D_ID_layer[i2DRecHit];
	  double localX_2DRecHit = recHits2D_localX[i2DRecHit];
	  double localY_2DRecHit = recHits2D_localY[i2DRecHit];
	  if(ChamberID(recHits2D_ID_endcap[i2DRecHit],recHits2D_ID_station[i2DRecHit],recHits2D_ID_ring[i2DRecHit],recHits2D_ID_chamber[i2DRecHit]) == chamber_of_srechit)
	    {
	      if(recHits2D_localX[i2DRecHit] == cscSegments_recHitRecord_localX[segment][iRecHit] && 
		 recHits2D_localY[i2DRecHit] == cscSegments_recHitRecord_localY[segment][iRecHit])
		
		{


		
		  out.push_back(i2DRecHit);
		  //		  std::cout<< "          ------------------------------   in a loop over all rechit in layer  "<< layer_2DRecHit << "   x/y   "<< localX_2DRecHit<< "  :  "<< localY_2DRecHit << std::endl;

		}

	    }

	}

    }


  return out;

}

std::vector<int>  
cscSelector::allSegments_inChamber_NOT_belonging_toMuon(unsigned int idchamber, unsigned int muon)
{

  std::vector<int> out;

  for (unsigned int isegment = 0; isegment < *cscSegments_nSegments; isegment++)
    {
      int segment_endcap     = cscSegments_ID_endcap[isegment];
      int segment_station    = cscSegments_ID_station[isegment];
      int segment_ring       = cscSegments_ID_ring[isegment];
      int segment_chamber    = cscSegments_ID_chamber[isegment];
      float segment_localX   = cscSegments_localX[isegment];
      float segment_localY   = cscSegments_localY[isegment];
      int chamber_of_segment = ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber);
      if(chamber_of_segment == idchamber)
	{
	  std::vector<int> muonsegments = allSegments_belonging_toMuon(muon);
	  if ( std::find(muonsegments.begin(), muonsegments.end(), isegment) != muonsegments.end() ) continue;
	  out.push_back(isegment);
	  //	  std::cout<<"==================  In a chamber  "<< chamber_of_segment << "   not a muon segment    "<< isegment << std::endl;
	}



    }
  return out;
}



TLorentzVector
cscSelector::gen_matchedMuon_P4(unsigned int muon)
{

  TLorentzVector out(0,0,0,0);
  int mc_index =-1;
  double dR =999.;
  for (unsigned int igen = 0; igen < *gen_muons_nMuons; igen++)
    {
      TLorentzVector igenLV(gen_muons_px[igen],gen_muons_py[igen],gen_muons_pz[igen],muons_energy[igen]);
      if(igenLV.DeltaR(Muon_P4(muon)) < dR)
	{
	  dR =  igenLV.DeltaR(Muon_P4(muon));
	  mc_index = igen;
	}
    }
  std::cout<<"minimal dR   "<<  dR   <<std::endl;
  if(mc_index !=-1)
    {
      out.SetPxPyPzE(gen_muons_px[mc_index],gen_muons_py[mc_index],gen_muons_pz[mc_index],muons_energy[mc_index]);
    }
  return out;
}
