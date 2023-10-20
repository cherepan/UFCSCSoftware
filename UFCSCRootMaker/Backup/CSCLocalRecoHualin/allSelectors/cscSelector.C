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
   
   //cout << "Event: " << *Event << endl;
   //if (*Event == 59284848/*479434223*/) cout << *cscSegments_nSegments << endl;

   SaveCSCWithMuon();

   // if no CSC contains a muon segment, skip this event
   if (int(endcapL.size()) == 0) return kTRUE;

   CountObjectsInCSCs(true,true,true,true,true,false,false,false); //RH,Seg,Wire,Strip,Comparator,ALCT,CLCT,CLT

// SOMEHOW CANNOT PROCESS ALL DIGIS TOGHETHER !!!

   for (int i = 0; i < int(endcapL.size()); i++) {

       int endcap_s = endcapL[i];
       int station_s = stationL[i];
       int ring_s = ringL[i];
       int chamber_s = chamberL[i];

       // use chamber Only with n seg
//       if (nSegmentL[i].size() != 1) continue;
       if (nSegmentL[i].size() != 4) continue;
       int segIndex = nSegmentL[i][0];
       // use chamber only if nRH/Seg == nRH/Chamber
//       if (cscSegments_nRecHits[segIndex] != nRH[i].size()) continue;
//       if (!(cscSegments_nRecHits[segIndex] == 6 && nRH[i].size() == 6 ) ) continue;
              

       if (!(cscSegments_nRecHits[nSegmentL[i][0]] == 6 && 
             cscSegments_nRecHits[nSegmentL[i][1]] == 6 && 
             cscSegments_nRecHits[nSegmentL[i][2]] == 6 && 
             cscSegments_nRecHits[nSegmentL[i][3]] == 6 && nRH[i].size() == 24) ) continue;

       nRHPerSeg->Fill(nRH[i].size());

       vector<int> nWireDigi_layer[6] = {};
       for (int j = 0; j < nWire[i].size(); j++) {
           int wireIndex = nWire[i][j];
           nWireDigi_layer[firedWireDigis_ID_layer[wireIndex] -1].push_back(wireIndex);
           
           }

       vector<int> nStripDigi_layer[6] = {};
       for (int j = 0; j < nStrip[i].size(); j++) {
           int stripIndex = nStrip[i][j];
           nStripDigi_layer[firedStripDigis_ID_layer[stripIndex] -1].push_back(stripIndex);

           }

       vector<int> nComparatorDigi_layer[6] = {};
       for (int j = 0; j < nComparator[i].size(); j++) {
           int comparatorIndex = nComparator[i][j];
           nComparatorDigi_layer[comparatorDigis_ID_layer[comparatorIndex] -1].push_back(comparatorIndex);

           }

       for (int j = 0; j < 6; j++) {

           nWireDigi_Layer->Fill(nWireDigi_layer[j].size(),j+1);
           nStripDigi_Layer->Fill(nStripDigi_layer[j].size(),j+1);
           nComparatorDigi_Layer->Fill(nComparatorDigi_layer[j].size(),j+1);

           }


// at most one wire/strip digi per layer
/*
       if (nWireDigi_layer[0].size() > 1 || nComparatorDigi_layer[0].size() > 1 || 
           nWireDigi_layer[1].size() > 1 || nComparatorDigi_layer[1].size() > 1 ||
           nWireDigi_layer[2].size() > 1 || nComparatorDigi_layer[2].size() > 1 ||
           nWireDigi_layer[3].size() > 1 || nComparatorDigi_layer[3].size() > 1 ||
           nWireDigi_layer[4].size() > 1 || nComparatorDigi_layer[4].size() > 1 ||
           nWireDigi_layer[5].size() > 1 || nComparatorDigi_layer[5].size() > 1
          ) return kTRUE;
*/

// exact 2 wg and 2 comparator per layer

       if ( !(nWireDigi_layer[0].size() == 2 && nComparatorDigi_layer[0].size() == 2 && 
              nWireDigi_layer[1].size() == 2 && nComparatorDigi_layer[1].size() == 2 &&
              nWireDigi_layer[2].size() == 2 && nComparatorDigi_layer[2].size() == 2 &&
              nWireDigi_layer[3].size() == 2 && nComparatorDigi_layer[3].size() == 2 &&
              nWireDigi_layer[4].size() == 2 && nComparatorDigi_layer[4].size() == 2 &&
              nWireDigi_layer[5].size() == 2 && nComparatorDigi_layer[5].size() == 2 )
          ) return kTRUE;


/*
       int wireTime[6] = {}; int comparatorTime[6] = {};
       vector<int> wireTime_sort; vector<int> comparatorTime_sort;
       for (int j = 0; j < 6; j++) {
           wireTime[j] = -1;
           comparatorTime[j] = -1;
           if (nWireDigi_layer[j].size() == 1 && nComparatorDigi_layer[j].size() == 1) {
              int tmpWireTime = firedWireDigis_timeBin[nWireDigi_layer[j][0]];
              int tmpComparatorTime = comparatorDigis_timeBin[nComparatorDigi_layer[j][0]];
              wireTime[j] = tmpWireTime;
              comparatorTime[j] = tmpComparatorTime;
              wireTime_sort.push_back(tmpWireTime);
              comparatorTime_sort.push_back(tmpComparatorTime);

              }
           }

       sort(wireTime_sort.begin(), wireTime_sort.end() );
       sort(comparatorTime_sort.begin(), comparatorTime_sort.end() );
*/

       int wg1 = firedWireDigis_ID_wire[nWireDigi_layer[2][0]];
       int wg2 = firedWireDigis_ID_wire[nWireDigi_layer[2][1]];
       if (wg1>wg2) {
          int tmpwg = wg1;
          wg1 = wg2; wg2 = tmpwg;
          }
       int com1 = comparatorDigis_ID_strip[nComparatorDigi_layer[2][0]];
       int com2 = comparatorDigis_ID_strip[nComparatorDigi_layer[2][1]];
       if (com1>com2) {
          int tmpcom = com1;
          com1 = com2; com2 = tmpcom;
          }

       if (abs(wg1-wg2)<5 || abs(com1-com2)<5) continue;

       int wireTime1[6] = {}; int wireTime2[6] = {};
       int comparatorTime1[6] = {}; int comparatorTime2[6] = {};
       vector<int> wireTime_sort1; vector<int> wireTime_sort2;
       vector<int> comparatorTime_sort1; vector<int> comparatorTime_sort2;

       for (int j = 0; j < 6; j++) {

           wireTime1[j] = -1; wireTime2[j] = -1;
           comparatorTime1[j] = -1; comparatorTime2[j] = -1;

           int tmpWG1 = firedWireDigis_ID_wire[nWireDigi_layer[j][0]];
           int tmpWG2 = firedWireDigis_ID_wire[nWireDigi_layer[j][1]];
           int tmpTime1_w = firedWireDigis_timeBin[nWireDigi_layer[j][0]];
           int tmpTime2_w = firedWireDigis_timeBin[nWireDigi_layer[j][1]];
           int tmpCom1 = comparatorDigis_ID_strip[nComparatorDigi_layer[j][0]];
           int tmpCom2 = comparatorDigis_ID_strip[nComparatorDigi_layer[j][1]];
           int tmpTime1_c = comparatorDigis_timeBin[nComparatorDigi_layer[j][0]];
           int tmpTime2_c = comparatorDigis_timeBin[nComparatorDigi_layer[j][1]];

           if (tmpWG1<tmpWG2) {
              wireTime1[j] = tmpTime1_w; wireTime2[j] = tmpTime2_w;
              } else {
                     wireTime1[j] = tmpTime2_w; wireTime2[j] = tmpTime1_w;
                     wireTime_sort1.push_back(tmpTime2_w); wireTime_sort2.push_back(tmpTime1_w);
                     }

           if (tmpCom1<tmpCom2) {
              comparatorTime1[j] = tmpTime1_c; comparatorTime2[j] = tmpTime2_c;
              } else {
                     comparatorTime1[j] = tmpTime2_c; comparatorTime2[j] = tmpTime1_c;
                     comparatorTime_sort1.push_back(tmpTime2_c); comparatorTime_sort2.push_back(tmpTime1_c);
                     }

           }
     
       sort(wireTime_sort1.begin(), wireTime_sort1.end() );
       sort(comparatorTime_sort1.begin(), comparatorTime_sort1.end() );
       sort(wireTime_sort2.begin(), wireTime_sort2.end() );
       sort(comparatorTime_sort2.begin(), comparatorTime_sort2.end() );

       deltaTime_l1->Fill(abs(wireTime1[0]-wireTime2[0]), abs(comparatorTime1[0]-comparatorTime2[0]));
       deltaTime_l2->Fill(abs(wireTime1[1]-wireTime2[1]), abs(comparatorTime1[1]-comparatorTime2[1]));
       deltaTime_l3->Fill(abs(wireTime1[2]-wireTime2[2]), abs(comparatorTime1[2]-comparatorTime2[2]));
       deltaTime_l4->Fill(abs(wireTime1[3]-wireTime2[3]), abs(comparatorTime1[3]-comparatorTime2[3]));
       deltaTime_l5->Fill(abs(wireTime1[4]-wireTime2[4]), abs(comparatorTime1[4]-comparatorTime2[4]));
       deltaTime_l6->Fill(abs(wireTime1[5]-wireTime2[5]), abs(comparatorTime1[5]-comparatorTime2[5]));

/*
       deltaTime_r1->Fill(abs(wireTime_sort1[0]-wireTime_sort2[0]), abs(comparatorTime_sort1[0]-comparatorTime_sort2[0]));
       deltaTime_r2->Fill(abs(wireTime_sort1[1]-wireTime_sort2[1]), abs(comparatorTime_sort1[1]-comparatorTime_sort2[1]));
       deltaTime_r3->Fill(abs(wireTime_sort1[2]-wireTime_sort2[2]), abs(comparatorTime_sort1[2]-comparatorTime_sort2[2]));
       deltaTime_r4->Fill(abs(wireTime_sort1[3]-wireTime_sort2[3]), abs(comparatorTime_sort1[3]-comparatorTime_sort2[3]));
       deltaTime_r5->Fill(abs(wireTime_sort1[4]-wireTime_sort2[4]), abs(comparatorTime_sort1[4]-comparatorTime_sort2[4]));
       deltaTime_r6->Fill(abs(wireTime_sort1[5]-wireTime_sort2[5]), abs(comparatorTime_sort1[5]-comparatorTime_sort2[5]));
*/

/*
       wireTime_comTime_l1->Fill(wireTime[0],comparatorTime[0]);
       wireTime_comTime_l2->Fill(wireTime[1],comparatorTime[1]);
       wireTime_comTime_l3->Fill(wireTime[2],comparatorTime[2]);
       wireTime_comTime_l4->Fill(wireTime[3],comparatorTime[3]);
       wireTime_comTime_l5->Fill(wireTime[4],comparatorTime[4]);
       wireTime_comTime_l6->Fill(wireTime[5],comparatorTime[5]);

       if (int(wireTime_sort.size()) >= 1) wireTime_comTime_r1->Fill(wireTime_sort[0],comparatorTime_sort[0]);
       if (int(wireTime_sort.size()) >= 2) wireTime_comTime_r2->Fill(wireTime_sort[1],comparatorTime_sort[1]);
       if (int(wireTime_sort.size()) >= 3) wireTime_comTime_r3->Fill(wireTime_sort[2],comparatorTime_sort[2]);
       if (int(wireTime_sort.size()) >= 4) wireTime_comTime_r4->Fill(wireTime_sort[3],comparatorTime_sort[3]);
       if (int(wireTime_sort.size()) >= 5) wireTime_comTime_r5->Fill(wireTime_sort[4],comparatorTime_sort[4]);
       if (int(wireTime_sort.size()) == 6) wireTime_comTime_r6->Fill(wireTime_sort[5],comparatorTime_sort[5]);
*/
       }

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
//c1->SetLogy();
//chi2PerDOF->SetMinimum(0.1);
//nSegPerChamber->SetMaximum(9000);
//nRHPerSeg->SetMaximum(8000);
//   nSegPerChamber->Write();
   nRHPerSeg->Write();
//   chi2PerDOF->Write();
   nWireDigi_Layer->Write();
   nStripDigi_Layer->Write();
   nComparatorDigi_Layer->Write();

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

void cscSelector::SetInputs(TString tag_, TString savedir_, bool doME11_)
{

     tag = tag_;
     savedir = savedir_;
     doME11 = doME11_;

}



void cscSelector::FillSegs(int segIndex, int chamberIndex, vector<SegsInChamber>& segs)
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



void cscSelector::SaveCSCWithMuon()
{


   endcapL.clear(); stationL.clear(); ringL.clear(); chamberL.clear();
   vector<int> ZmuIndex; ZmuIndex.clear();
     
   for (int i = 0; i < *muons_nMuons; i++) {

       if (!(muons_isPFMuon[i] || muons_isGlobalMuon[i] || muons_isTrackerMuon[i]) ) continue;
       if (!(abs(muons_eta[i]) < 2.4 && abs(muons_eta[i]) < 2.4)) continue;
       if (!(abs(muons_dz[i]) < 1 && abs(muons_dxy[i]) < 0.05)) continue;
//       if (muons_pt[i] < 20) continue;
       if (muons_pt[i] < 5) continue;
 
       ZmuIndex.push_back(i);

   }

   if (int(ZmuIndex.size()) != 2) return;
//   if (int(ZmuIndex.size()) < 4 ) return;
   
   int index1 = ZmuIndex[0]; int index2 = ZmuIndex[1];
//   int index1 = ZmuIndex[2]; int index2 = ZmuIndex[3];

   if (muons_charge[index1] + muons_charge[index2] != 0) return;

   TLorentzVector mu1, mu2;
   mu1.SetPtEtaPhiE(muons_pt[index1], muons_eta[index1], muons_phi[index1], muons_energy[index1]);
   mu2.SetPtEtaPhiE(muons_pt[index2], muons_eta[index2], muons_phi[index2], muons_energy[index2]);
   TLorentzVector Z = mu1 + mu2;

   if (Z.M() > 100 || Z.M() < 80) return;
//   if (int(ZmuIndex.size()) == 2 && muons_charge[index1] + muons_charge[index2] == 0 && Z.M() > 80 && Z.M() < 100 ) return;

   // select chamber with muon segment


   for (int i = 0; i < int(muons_cscSegmentRecord_endcap[index1].size()); i++) {

       endcapL.push_back(muons_cscSegmentRecord_endcap[index1][i]);       
       stationL.push_back(muons_cscSegmentRecord_station[index1][i]); 
       ringL.push_back(muons_cscSegmentRecord_ring[index1][i]); 
       chamberL.push_back(muons_cscSegmentRecord_chamber[index1][i]); 

       }

   for (int i = 0; i < int(muons_cscSegmentRecord_endcap[index2].size()); i++) {

       int endcap = muons_cscSegmentRecord_endcap[index2][i];
       int station = muons_cscSegmentRecord_station[index2][i];
       int ring = muons_cscSegmentRecord_ring[index2][i];
       int chamber = muons_cscSegmentRecord_chamber[index2][i];

       if ( (find(endcapL.begin(), endcapL.end(), endcap) != endcapL.end() ) &&
            (find(stationL.begin(), stationL.end(), station) != stationL.end() ) &&
            (find(ringL.begin(), ringL.end(), ring) != ringL.end() ) &&
            (find(chamberL.begin(), chamberL.end(), chamber) != chamberL.end() ) 
           ) continue;

       endcapL.push_back(endcap); 
       stationL.push_back(station);
       ringL.push_back(ring);    
       chamberL.push_back(chamber);

       }

/*
   for (int i = 0; i < int(ZmuIndex.size()); i++) {
       int tmpIndex = ZmuIndex[i];
       for (int j = 0; j < int(muons_cscSegmentRecord_endcap[tmpIndex].size()); i++) {
           int endcap = muons_cscSegmentRecord_endcap[tmpIndex][j];
           int station = muons_cscSegmentRecord_station[tmpIndex][j];
           int ring = muons_cscSegmentRecord_ring[tmpIndex][j];
           int chamber = muons_cscSegmentRecord_chamber[tmpIndex][j];

           if ( (find(endcapL.begin(), endcapL.end(), endcap) != endcapL.end() ) &&
                (find(stationL.begin(), stationL.end(), station) != stationL.end() ) &&
                (find(ringL.begin(), ringL.end(), ring) != ringL.end() ) &&
                (find(chamberL.begin(), chamberL.end(), chamber) != chamberL.end() )
              ) continue;

           endcapL.push_back(endcap);
           stationL.push_back(station);
           ringL.push_back(ring);
           chamberL.push_back(chamber);

           }
       }
*/

}



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
