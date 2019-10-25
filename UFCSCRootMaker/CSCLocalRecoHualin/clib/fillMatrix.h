#include <vector>
#include <TROOT.h>
#include "TMatrixDSparse.h"
#include "TArrayI.h"
#include "TArrayD.h"

void cscSelector::FillWireMatrix(vector<int> wireDigiIndexs, TMatrixDSparse& wireMatrix)
{

  const int nWires = int(wireDigiIndexs.size());
  TArrayI row(nWires),col(nWires);
  TArrayD data(nWires);

  for (int i = 0; i < nWires; i++) {
      int index = wireDigiIndexs[i];
      int wLayer = firedWireDigis_ID_layer[index];
      int wireNumber = firedWireDigis_ID_wire[index];
      int wireTime = firedWireDigis_timeBin[index];

      row[i] = wLayer-1;
      col[i] = wireNumber-1;
      data[i] = wireTime+1; //count from 1 instead of 0      
//cout << col[i] << endl;
      }

  wireMatrix.SetMatrixArray(nWires,row.GetArray(),col.GetArray(),data.GetArray());
//cout <<"wire"<<endl;  wireMatrix.Print();
}


void cscSelector::FillComparatorMatrix(vector<int> comparatorDigiIndexs, TMatrixDSparse& comparatorMatrix, bool doStagger, int min=0, int max=120)
{

  int comNum_min = min*2-1; comNum_min -= 2;
  int comNum_max = max*2;   comNum_max += 2;

  const int nComparators = int(comparatorDigiIndexs.size());
  TArrayI row(nComparators),col(nComparators);
  TArrayD data(nComparators);

  for (int i = 0; i < nComparators; i++) {
      int index = comparatorDigiIndexs[i];
      int cLayer = comparatorDigis_ID_layer[index];
      int comparatorNumber = comparatorDigis_ID_halfStrip[index];
      int comparatorTime = comparatorDigis_timeBin[index];

      if (min!=0 && max!=120 && comparatorNumber >= comNum_min && comparatorNumber <= comNum_max) continue;
      // skip an area, do not fill with comparator information for scan

      if (doStagger && (cLayer == 1 || cLayer == 3 || cLayer == 5)) comparatorNumber += 1;

      row[i] = cLayer-1;
      col[i] = comparatorNumber;//-1;
      data[i] = comparatorTime+1; //count from 1

//cout << comparatorNumber << "," << col[i] << ", " << row[i] << endl;
      }
  comparatorMatrix.SetMatrixArray(nComparators,row.GetArray(),col.GetArray(),data.GetArray());
//cout <<"comparator"<<endl;  comparatorMatrix.Print();
}

