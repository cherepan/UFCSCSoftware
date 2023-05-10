
void cscSelector::MuonsHelper()
{

  Muons_Index.clear();
  Muon_segment_endcap.clear();
  Muon_segment_station.clear();
  Muon_segment_ring.clear();
  Muon_segment_chamber.clear();
  Muon_segment_localX.clear();
  Muon_segment_localY.clear();
  //Muon_segment

   // keep muons with the following selection : 
   for (int i = 0; i < *muons_nMuons; i++) {
     if (!(muons_isPFMuon[i] || muons_isGlobalMuon[i] || muons_isTrackerMuon[i]) ) continue;
     if (!(abs(muons_eta[i]) < 2.4 && abs(muons_eta[i]) < 2.4)) continue;
     if (!(abs(muons_dz[i]) < 1 && abs(muons_dxy[i]) < 0.5)) continue;
     if (muons_pt[i] < 5) continue;
     Muons_Index.push_back(i);
   }



   for (unsigned int imu = 0; imu < Muons_Index.size() ; imu++) {

     int selected_muon = Muons_Index.at(imu);
     std::vector<int> iMuon_endcap;
     std::vector<int> iMuon_station;
     std::vector<int> iMuon_ring;
     std::vector<int> iMuon_chamber;

     std::vector<float> iMuon_localX;
     std::vector<float> iMuon_localY;
       

     for (unsigned int iSegment = 0; iSegment < muons_cscSegmentRecord_endcap[selected_muon].size(); iSegment++) 
       {
	 int endcap    = muons_cscSegmentRecord_endcap[selected_muon][iSegment];
	 int station   = muons_cscSegmentRecord_station[selected_muon][iSegment];
	 
	 int ring      = muons_cscSegmentRecord_ring[selected_muon][iSegment];
	 int chamber   = muons_cscSegmentRecord_chamber[selected_muon][iSegment];

	 double localX = muons_cscSegmentRecord_localX[selected_muon][iSegment];
	 double localY = muons_cscSegmentRecord_localY[selected_muon][iSegment];

	 // -------------  match to the global segments index ----------------



	 // -------------  match to the global segments index ----------------




	 iMuon_endcap.push_back(endcap);
	 iMuon_station.push_back(station);
	 iMuon_ring.push_back(ring);

	 iMuon_chamber.push_back(chamber);
	 iMuon_localX.push_back(localX);
	 iMuon_localY.push_back(localY);

	 //	 vector<int> tmpStrips = RHsMatching(endcap, station, ring, chamber, localX, localY);          

	 std::vector<int> iStrips;
	 std::vector<int> iWire;
	 std::vector<int> iWiresGroup;

	 RecHitInSegmentMatching(endcap, station, ring, chamber,  localX, localY, iStrips, iWire, iWiresGroup);
	   // do seg - rh - strip matching here, save all associated strips
	   // if is from a new chamber, push back a vector to end
	   // if is from a repeated chamber, append to the end before next continue
	 //	 std::cout<<"  number of strips of a segment  " << iStrips.size() << std::endl;
          


	 //  check this later
	 /*
           if ( (find(endcapL.begin(), endcapL.end(), endcap) != endcapL.end() ) &&
                (find(stationL.begin(), stationL.end(), station) != stationL.end() ) &&
                (find(ringL.begin(), ringL.end(), ring) != ringL.end() ) &&
                (find(chamberL.begin(), chamberL.end(), chamber) != chamberL.end() )
              ) {
                
                int selected_muon = find(endcapL.begin(), endcapL.end(), endcap) - endcapL.begin();
                vector<int> oldStrips = stripsFromMu[selected_muon];
//cout << "before: " << stripsFromMu[selected_muon].size() << endl;
                oldStrips.insert(oldStrips.end(), tmpStrips.begin(), tmpStrips.end());
                stripsFromMu[selected_muon] = oldStrips;
//cout << "after: " << stripsFromMu[selected_muon].size() << endl; cout << endl;

                continue;
	   }
	 
	 

           endcapL.push_back(endcap);
           stationL.push_back(station);
           ringL.push_back(ring);
           chamberL.push_back(chamber);
           muIndex.push_back(selected_muon);
           stripsFromMu.push_back(tmpStrips);
	 */
       }

     
     Muon_segment_endcap.push_back(iMuon_endcap);
     Muon_segment_station.push_back(iMuon_station);
     Muon_segment_ring.push_back(iMuon_ring);
     Muon_segment_chamber.push_back(iMuon_chamber);
     
     Muon_segment_localX.push_back(iMuon_localX);
     Muon_segment_localY.push_back(iMuon_localY);


   }

}



void
cscSelector::RecHitInSegmentMatching(int endcap, int station, int ring, int chamber, double localX, double localY, 
				     std::vector<int> &strips, std::vector<int> &wires, std::vector<int>  &wiresgroup) {

  //  std::vector<int> strips;     strips.clear();
  //  std::vector<int> wires;      wires.clear();
  //  std::vector<int> wiresgroup; wiresgroup.clear();

      // loop over all segments
      for (int i = 0; i < *cscSegments_nSegments; i++)
	{

          int    segment_endcap   = cscSegments_ID_endcap[i];
          int    segment_station  = cscSegments_ID_station[i];
          int    segment_ring     = cscSegments_ID_ring[i];
          int    segment_chamber  = cscSegments_ID_chamber[i];
          double segment_localX   = cscSegments_localX[i];
          double segment_localY   = cscSegments_localY[i];

          if (endcap  != segment_endcap    || 
	      station != segment_station   || 
	      ring    != segment_ring      || 
	      chamber != segment_chamber   ||
              localX  != segment_localX    || 
	      localY  != segment_localY)     continue; // check that the strip belong to a muon segment
	  //loop over the rec hit belonging to the segment
          for (unsigned int iRecHit = 0; iRecHit < cscSegments_recHitRecord_endcap[i].size(); iRecHit++) 
	    {
              int    rechit_layer  = cscSegments_recHitRecord_layer[i][iRecHit];
              double rechit_localX = cscSegments_recHitRecord_localX[i][iRecHit];
              double rechit_localY = cscSegments_recHitRecord_localY[i][iRecHit];

              for (int i2DRecHit = 0; i2DRecHit < *recHits2D_nRecHits2D; i2DRecHit++)
		{

                  int endcap_2DRecHit    = recHits2D_ID_endcap[i2DRecHit];
                  int station_2DRecHit   = recHits2D_ID_station[i2DRecHit];
                  int ring_2DRecHit      = recHits2D_ID_ring[i2DRecHit];
                  int chamber_2DRecHit   = recHits2D_ID_chamber[i2DRecHit];
                  int layer_2DRecHit     = recHits2D_ID_layer[i2DRecHit];
                  double localX_2DRecHit = recHits2D_localX[i2DRecHit];
                  double localY_2DRecHit = recHits2D_localY[i2DRecHit];

		  //   match to the rechit in the full collection
                  if (endcap_2DRecHit   != endcap        || 
		      station_2DRecHit  != station       || 
		      ring_2DRecHit     != ring          || 
		      chamber_2DRecHit  != chamber       || 
		      layer_2DRecHit    != rechit_layer  ||
                      localX_2DRecHit   != rechit_localX || 
		      localY_2DRecHit   != rechit_localY)  continue;
		  
                     int nearestStrip     = recHits2D_nearestStrip[i2DRecHit];
                     int nearestWire      = recHits2D_nearestWire[i2DRecHit];
                     int nearestWireGroup = recHits2D_nearestWireGroup[i2DRecHit];
                     // save it in a vector, then you are done !
                     strips.push_back(nearestStrip);
                     wires.push_back(nearestWire);
                     wiresgroup.push_back(nearestWireGroup);

                  }
              }
          }

}


