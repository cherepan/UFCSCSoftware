void cscSelector::SaveCSCWithMuon()
{


   endcapL.clear(); stationL.clear(); ringL.clear(); chamberL.clear(); muIndex.clear(); stripsFromMu.clear();
   vector<int> ZmuIndex; ZmuIndex.clear();

   for (int i = 0; i < *muons_nMuons; i++) {

       if (!(muons_isPFMuon[i] || muons_isGlobalMuon[i] || muons_isTrackerMuon[i]) ) continue;
       if (!(abs(muons_eta[i]) < 2.4 && abs(muons_eta[i]) < 2.4)) continue;
       if (!(abs(muons_dz[i]) < 1 && abs(muons_dxy[i]) < 0.5)) continue;
       if (muons_pt[i] < 5) continue;

       ZmuIndex.push_back(i);

   }


   for (int i = 0; i < int(ZmuIndex.size()); i++) {
       int tmpIndex = ZmuIndex[i];
       for (int j = 0; j < int(muons_cscSegmentRecord_endcap[tmpIndex].size()); j++) {
           int endcap = muons_cscSegmentRecord_endcap[tmpIndex][j];
           int station = muons_cscSegmentRecord_station[tmpIndex][j];
           int ring = muons_cscSegmentRecord_ring[tmpIndex][j];
           int chamber = muons_cscSegmentRecord_chamber[tmpIndex][j];
           double localX = muons_cscSegmentRecord_localX[tmpIndex][j];
           double localY = muons_cscSegmentRecord_localY[tmpIndex][j];

           vector<int> tmpStrips = RHsMatching(endcap, station, ring, chamber, localX, localY);          
// do seg - rh - strip matching here, save all associated strips
// if is from a new chamber, push back a vector to end
// if is from a repeated chamber, append to the end before next continue
           if ( (find(endcapL.begin(), endcapL.end(), endcap) != endcapL.end() ) &&
                (find(stationL.begin(), stationL.end(), station) != stationL.end() ) &&
                (find(ringL.begin(), ringL.end(), ring) != ringL.end() ) &&
                (find(chamberL.begin(), chamberL.end(), chamber) != chamberL.end() )
              ) {
                
                int tmpIndex = find(endcapL.begin(), endcapL.end(), endcap) - endcapL.begin();
                vector<int> oldStrips = stripsFromMu[tmpIndex];
//cout << "before: " << stripsFromMu[tmpIndex].size() << endl;
                oldStrips.insert(oldStrips.end(), tmpStrips.begin(), tmpStrips.end());
                stripsFromMu[tmpIndex] = oldStrips;
//cout << "after: " << stripsFromMu[tmpIndex].size() << endl; cout << endl;

                continue;
                }

           endcapL.push_back(endcap);
           stationL.push_back(station);
           ringL.push_back(ring);
           chamberL.push_back(chamber);
           muIndex.push_back(tmpIndex);
           stripsFromMu.push_back(tmpStrips);

           }
       }


}


vector<int> cscSelector::RHsMatching(int endcap, int station, int ring, int chamber, double localX, double localY) {

      vector<int> strips; strips.clear();

      for (int i = 0; i < *cscSegments_nSegments; i++) {

          int endcap_ = cscSegments_ID_endcap[i];
          int station_ = cscSegments_ID_station[i];
          int ring_ = cscSegments_ID_ring[i];
          int chamber_ = cscSegments_ID_chamber[i];
          double localX_ = cscSegments_localX[i];
          double localY_ = cscSegments_localY[i];

          if (endcap != endcap_ || station != station_ || ring != ring_ || chamber != chamber_ ||
              localX != localX_ || localY != localY_) continue;
       
          for (int j = 0; j < int(cscSegments_recHitRecord_endcap[i].size()); j ++) {

              int layer_rh = cscSegments_recHitRecord_layer[i][j];
              double localX_rh = cscSegments_recHitRecord_localX[i][j];
              double localY_rh = cscSegments_recHitRecord_localY[i][j];

              for (int k = 0; k < *recHits2D_nRecHits2D; k++) {

                  int endcap_r = recHits2D_ID_endcap[k];
                  int station_r = recHits2D_ID_station[k];
                  int ring_r = recHits2D_ID_ring[k];
                  int chamber_r = recHits2D_ID_chamber[k];
                  int layer_r = recHits2D_ID_layer[k];
                  double localX_r = recHits2D_localX[k];
                  double localY_r = recHits2D_localY[k];

                  if (endcap_r != endcap || station_r != station || ring_r != ring || chamber_r != chamber || layer_r != layer_rh ||
                      localX_r != localX_rh || localY_r != localY_rh) continue;

                     int nearestStrip = recHits2D_nearestStrip[k];
                     // save it in a vector, then you are done !
                     strips.push_back(nearestStrip);

                  }
              }
          }

      return strips;
}
