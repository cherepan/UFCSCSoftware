#include <algorithm>    // std::sort
#include <vector>       // std::vector

   struct CSC1DSeg{

    int keyPos;
    int hitsPos[6];
    int hitsTime[6];
    int nHits;
    int patternRank;

    int MeanTime() {

        double mean = 0;
        double count = 0; 
        for (int i = 0; i < 6; i++) {
            if (hitsTime[i] > 0) {
               count++;
               mean += hitsTime[i];
               }
            }
        mean = mean/count; return mean;
        }

    vector<int> SortedTime() {
 
        vector<int> sortedTime;
        for (int i = 0; i < 6; i++) {
            if (hitsTime[i] > 0) sortedTime.push_back(hitsTime[i]);
            }

        sort(sortedTime.begin(), sortedTime.end());
        return sortedTime;
        } 

   };

