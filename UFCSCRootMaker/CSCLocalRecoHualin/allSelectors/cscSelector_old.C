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
   for (int i = 0; i < *cscSegments_nSegments; i++) {

       int endcap = cscSegments_ID_endcap[i];
       int station = cscSegments_ID_station[i];
       int ring = cscSegments_ID_ring[i];
       int chamber = cscSegments_ID_chamber[i];
       int chamberIndex = endcap*10000 + station*1000 + ring*100 + chamber;
//       cout << i << ", " << chamberIndex << ", " << segs.size() << endl;

       bool isME11 = false;

       if ( (station == 1 && (ring==1 || ring==4) ) ) isME11 = true;

       if ( doME11 && !isME11 ) continue;
       if ( !doME11 && isME11 ) continue;
              
       FillSegs(i,chamberIndex,segs);

//       nRHPerSeg->Fill(cscSegments_nRecHits[i]);
//       chi2PerDOF->Fill(cscSegments_chi2[i]/cscSegments_nDOF[i]);

       }

   for (int i = 0; i < int(segs.size()); i++) {
       int index = segs[i].first;
       vector<int> tmpSegs = segs[i].second;
       nSegPerChamber->Fill(tmpSegs.size());

       for (int j = 0; j < tmpSegs.size(); j++) {
           int treeIndex = tmpSegs[j];

           if (tmpSegs.size() != 1) continue;
           nRHPerSeg->Fill(cscSegments_nRecHits[treeIndex]);
           chi2PerDOF->Fill(cscSegments_chi2[treeIndex]/cscSegments_nDOF[treeIndex]);

           }
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
   nSegPerChamber->Write();
   nRHPerSeg->Write();
   chi2PerDOF->Write();

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
