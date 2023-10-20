#ifndef CSCSegment_CSCWireSegment_H
#define CSCSegment_CSCWireSegment_H

#include "TH2F.h"

class CSCWireSegment
{

public:

  CSCWireSegment();
  CSCWireSegment(int wg, int nLayer, TH2F* wireSegHist);

  int keyWG() const { return theKeyWG; }
  int nLayersWithHits() const { return nlayersWithHits; }
  double* wireHits() {return wHits;}
  int* nLayerHits() {return nHits;}

  void updateWHits(double* wHits2, int* nHits2);
  double comHitLow();
  double comHitHigh();

  ~CSCWireSegment();

private:

  int theKeyWG;
  int nlayersWithHits;
  double wHits[6] ; // whits position in each layer
  int nHits[6]; // number of whits in each layer

  double GetMean(TH1D* h1);
//  TH2F* wirePattern;

};
#endif
