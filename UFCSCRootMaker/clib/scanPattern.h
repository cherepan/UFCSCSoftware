#include <vector>
#include <TROOT.h>
#include "TMatrixDSparse.h"
#include "TArrayI.h"
#include "TArrayD.h"
#include <vector>
#include <utility>      // std::pair, std::make_pair
#include <algorithm>    // std::find

vector<CSC1DSeg> cscSelector::MakeScans(TMatrixDSparse inputMatrix, bool reverseRowIndex, int** rows, int** cols, int* nHits, int* ranks, int nPatterns) {
  
    vector<CSC1DSeg> allSegs1D; 
    vector<TMatrixDSparse> inputMatrixs;
    inputMatrixs.push_back(inputMatrix);

    for (int i = 6; i >= 4; i--) { // nHits/Seg loop
//    for (int i = 6; i >= 3; i--) { // nHits/Seg loop
     for (int j = 0; j < nPatterns; j++) { // patterns loop

         int* rowIndex = rows[j];
         int* colIndex = cols[j];
         int nhits = nHits[j];
         int rank = ranks[j];

//         TMatrixDSparse inputMatrix_ = inputMatrixs.back();
//         PrintSparseMatrix(inputMatrix_);
/*         TMatrixDSparse tmpMatrix = */ScanPattern(inputMatrix, allSegs1D, i, reverseRowIndex, rowIndex, colIndex, nhits, rank);
//         inputMatrixs.push_back(tmpMatrix);
//PrintSparseMatrix(inputMatrix);         // add to allSegs1D
//         for (int k = 0; k < int(new1DSegs.size()); k++) allSegs1D.push_back(new1DSegs[k]);
//cout << "allSegs1D size: " << allSegs1D.size() << endl;
         }
        } 

    return allSegs1D;
}


/*TMatrixDSparse*/ void cscSelector::ScanPattern(TMatrixDSparse& inputMatrix, vector<CSC1DSeg> & csc1DSeg, int nHitsPerSeg, bool reverseRowIndex, //for ME 3 and ME 4
                                                         int* r_index, int* c_index, int nHitsInPattern, int patternRank) {
//PrintSparseMatrix(inputMatrix);
//cout << endl;

//     vector<CSC1DSeg> cscSegs1D; // container saving 1D segment
     vector<int> usedCols; // save used cols (wire group or half strip number), avoid repeat scan
     const int* rowArray = inputMatrix.GetRowIndexArray(); // https://root.cern.ch/root/html534/guides/users-guide/LinearAlgebra.html
     const int* colArray = inputMatrix.GetColIndexArray();
     const double* dataArray = inputMatrix.GetMatrixArray();

     const int nElement = rowArray[inputMatrix.GetNrows()]; // only scan cols with non-zero element


//cout << "nElement: " << nElement << ", " << inputMatrix.GetNrows() << endl;

/// !!!!! //
// this is keyStep, after access inputMatrix and set element to 0, row and colArray got messed up !!!! 
     vector<int> colArray_v; for (int i = 0; i < nElement; i++) {colArray_v.push_back(colArray[i]);}

     int nCols = inputMatrix.GetNcols();
//cout << "nCols: " << nCols << endl;
//      for (int i = 0; i < nElement; i++) {
//          cout << colArray_v[i] << endl; }

     for (int i = 0; i < nElement; i++) {
//cout << "i: " << i << endl;
//      for (int k = 0; k < nElement; k++) {  cout << colArray_v[k] << endl; }


         int keyPos = colArray_v[i];
         if (find(usedCols.begin(), usedCols.end(), keyPos) != usedCols.end() ) continue;  
//if (keyPos > 161) cout << "keyPos: " << keyPos << endl;

         int timeHits[6] = {0,0,0,0,0,0};
         int nNonZeroHits[6] = {0,0,0,0,0,0};
         vector<pair<int, int> > nonZeroIndexs;

         for (int j = 0; j < nHitsInPattern; j++) {
             int c_index_tmp = c_index[j] + keyPos;
           
             if (c_index_tmp < 0 || c_index_tmp >= nCols) continue;
             
             int rowIndex = r_index[j];
             int colIndex = c_index_tmp;
//cout << "row: " << rowIndex << ", col: " << colIndex << endl;
             if (reverseRowIndex) rowIndex = 5-rowIndex;
             int thisElement = inputMatrix[rowIndex][colIndex]; // if wire group or comparator/strip fired, this value should be positive (by construction), other wise 0
             timeHits[rowIndex] += thisElement;
             if (thisElement > 0) {
                nNonZeroHits[rowIndex]+=1;
                nonZeroIndexs.push_back(make_pair(rowIndex,colIndex));
//cout << rowIndex << ", " << colIndex << endl;
                }
             }

         int nHits = CountNonZero(nNonZeroHits,6);         
//cout << "nHits: " << nHits << endl;
//      for (int k = 0; k < nElement; k++) {  cout << colArray_v[k] << endl; }

         usedCols.push_back(keyPos);

         if (nHits < nHitsPerSeg) continue; // a segment is found only if number of hits is bigger than nHitsPerSeg (6,5,4,3)

         CSC1DSeg tmp1DSeg;
         tmp1DSeg.keyPos = keyPos; //usedCols.push_back(keyPos);
         tmp1DSeg.nHits = nHits;
         tmp1DSeg.patternRank = patternRank; 

         for (int k = 0; k < 6; k++) {
             if (nNonZeroHits[k]>0) (tmp1DSeg.hitsTime)[k] = (timeHits[k]/nNonZeroHits[k]);
             else (tmp1DSeg.hitsTime)[k] = 0;
             } // note, this is int, may need to think to change it to double      
         // clean up used wire/strip hits
         for (int k = 0; k < int(nonZeroIndexs.size()); k++) inputMatrix[nonZeroIndexs[k].first][nonZeroIndexs[k].second] = 0;
//         Print1DSeg(tmp1DSeg);
         csc1DSeg.push_back(tmp1DSeg);

         }
 
    return inputMatrix;  
}


int cscSelector::CountNonZero(int * array, int size) {

    int count = 0;

    for (int i = 0; i < size; i++) {

     if (array[i] > 0) count+=1;

    }

    return count;
}


void cscSelector::Print1DSeg(CSC1DSeg seg1D) {

     cout << "keyPos: " << seg1D.keyPos << endl;
     cout << "nHits: "  << seg1D.nHits << endl;
     cout << "time: ";
     for (int i = 0; i < 6; i++) cout << (seg1D.hitsTime)[i] << " ";

     cout << endl;
     cout << seg1D.MeanTime() << endl;
     cout << "patternRank: " << seg1D.patternRank << endl;
}

