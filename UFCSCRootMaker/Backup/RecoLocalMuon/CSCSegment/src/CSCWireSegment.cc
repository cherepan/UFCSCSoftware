#include <iostream>
#include "RecoLocalMuon/CSCSegment/src/CSCWireSegment.h"

CSCWireSegment::CSCWireSegment() {}

CSCWireSegment::CSCWireSegment(int wg,
                               int nLayer,
                               TH2F* wireSegHist) :
   theKeyWG( wg ),
   nlayersWithHits( nLayer )
  
{

   TH1D* wHitHists[6];
   TH1D* nHitHists = wireSegHist->ProjectionY("nLayerHits",0,-1);
   for (int i = 0; i < 6; i++) {

       wHitHists[i] = wireSegHist->ProjectionX("layer"+TString(i+1),i+1,i+1);
       wHits[i] = wHitHists[i]->GetMean()+0.5; 
       if (wHitHists[i]->GetMean() == 0) wHits[i] = 0;
//       wHits[i] = GetMean(wHitHists[i]);
       // first number is layer, second number is wPos in unit of wire group
       // +0.5 is because of ROOT histogram property, GetMean() returns 4.5 for example if fill only one entry at 4 
       nHits[i] = nHitHists->GetBinContent(i+1);

       }

}


CSCWireSegment::~CSCWireSegment() {}

void CSCWireSegment::updateWHits(double* wHits2, int* nHits2) 
{

   for (int i = 0; i < 6; i++) {

       if (nHits[i]+nHits2[i])
          {wHits[i] = (wHits[i]*nHits[i] + wHits2[i]*nHits2[i] )/(nHits[i]+nHits2[i]);}
       nHits[i] = nHits[i]+nHits2[i];

       }

}



double CSCWireSegment::comHitLow()
{

  double low = 120;

  for (int i = 0; i < 6; i++) {

      double tmpHit = wHits[i];
      if (tmpHit < low && wHits[i] > 0) low = tmpHit;

      }

  return low;

}


double CSCWireSegment::comHitHigh()
{

  double high = -1;

  for (int i = 0; i < 6; i++) {

      double tmpHit = wHits[i];
      if (tmpHit > high && wHits[i] > 0) high = tmpHit;

      }

  return high;

}


double CSCWireSegment::GetMean(TH1D* h1)
{

  double mean = 0;
  double count = 0;
  double sum = 0;

//std::cout << h1->GetNbinsX() << std::endl;
  for (int i = 0; i < h1->GetNbinsX(); i++) {

      if (h1->GetBinContent(i+1) > 0) {
         count += 1; sum += (h1->GetBinLowEdge(i+1) + 1);
//std::cout << "count: " << count << ", sum: " << sum << std::endl;
         }
      }

  if (count > 0) mean = sum/count;
//std::cout << mean << std::endl;
  return mean;
}
