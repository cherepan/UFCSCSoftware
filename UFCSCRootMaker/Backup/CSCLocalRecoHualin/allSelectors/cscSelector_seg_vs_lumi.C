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
   
   // typedef pair<int, vector<int> > SegsInChamber;
   // long : 1-2-3-45
   //cout << "Event: " << *Event << endl;

   segs.clear();
//if (*Event == 59284848/*479434223*/) cout << *cscSegments_nSegments << endl;


   vector<int> ZmuIndex; ZmuIndex.clear();
     
   for (int i = 0; i < *muons_nMuons; i++) {

       if (!(muons_isPFMuon[i] || muons_isGlobalMuon[i]) ) continue;
       if (!(muons_dz[i] < 1 && muons_dxy[i] < 0.05)) continue;
       if (muons_pt[i] < 5) continue;

       ZmuIndex.push_back(i);

   }

   if (int(ZmuIndex.size()) != 2) return kTRUE;

   int index1 = ZmuIndex[0]; int index2 = ZmuIndex[1];
   if (muons_charge[index1] + muons_charge[index2] != 0) return kTRUE;

   TLorentzVector mu1, mu2;
   mu1.SetPtEtaPhiE(muons_pt[index1], muons_eta[index1], muons_phi[index1], muons_energy[index1]);
   mu2.SetPtEtaPhiE(muons_pt[index2], muons_eta[index2], muons_phi[index2], muons_energy[index2]);
   TLorentzVector Z = mu1 + mu2;

   if (Z.M() > 100 || Z.M() < 80) return kTRUE;

   vector<int> endcapL; endcapL.clear();
   vector<int> stationL; stationL.clear();
   vector<int> ringL; ringL.clear();
   vector<int> chamberL; chamberL.clear();

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

       if ( (find(endcapL.begin(), endcapL.end(), endcap) == endcapL.end() ) &&
            (find(stationL.begin(), stationL.end(), station) == stationL.end() ) &&
            (find(ringL.begin(), ringL.end(), ring) == ringL.end() ) &&
            (find(chamberL.begin(), chamberL.end(), chamber) == chamberL.end() ) 
           ) continue;

       endcapL.push_back(endcap); 
       stationL.push_back(station);
       ringL.push_back(ring);    
       chamberL.push_back(chamber);

       }

//   vector<int> nSegmentL;
   const int nCSC = int(endcapL.size());
   int nSegmentL[540] = {};

   for (int i = 0; i < int(endcapL.size()); i++) {

       int endcap = endcapL[i];
       int station = stationL[i];
       int ring = ringL[i];
       int chamber = chamberL[i];

       nSegmentL[i] = 0;

       for (int j = 0; j < *cscSegments_nSegments; j++) {

           int endcap_s = cscSegments_ID_endcap[j]; 
           int station_s = cscSegments_ID_station[j];
           int ring_s = cscSegments_ID_ring[j];
           int chamber_s = cscSegments_ID_chamber[j];

           if (endcap==endcap_s && station == station_s && ring == ring_s && chamber == chamber_s) nSegmentL[i] += 1;
       }

   }

   
   for (int i = 0; i < int(endcapL.size()); i++) {

       // select chamber

       int endcap_s = cscSegments_ID_endcap[i];
       int station_s = cscSegments_ID_station[i];
       int ring_s = cscSegments_ID_ring[i];
       int chamber_s = cscSegments_ID_chamber[i];

       if (station_s == 1 && (/* ring_s == 1 ||*/ ring_s ==4))
          nSeg_lumi->Fill(*instLumi, nSegmentL[i]);

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
//   nRHPerSeg->Write();
//   chi2PerDOF->Write();
   nSeg_lumi->Write();
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
