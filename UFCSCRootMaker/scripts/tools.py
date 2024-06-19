import array
import multiprocessing
import os
import time

import ROOT
import sys, pwd, commands
import optparse, shlex, re
import math
from ROOT import *
import ROOT
from array import array
from numpy import sqrt




def findMuonsFromZ(tree):  # find gen Muon from Z unt the   forward region and pt > 15
        Index = []
        for k in range(0, tree.gen_muons_nMuons):
            if (tree.gen_muons_mother_pdgId[k] == 23):
                LV = genMuonLV(tree, k)
                if(LV.Pt() > 15 and math.fabs(LV.Eta()) > 1.1 and math.fabs(LV.Eta()) < 2.3):
                    Index.append(k)
        return Index


def genMuonLV(tree, index):                      # LV of GEN muon
        if index > tree.gen_muons_nMuons or index == -1:
            print("============= >  genMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        genMuon = TLorentzVector(tree.gen_muons_px[index],
                                 tree.gen_muons_py[index],
                                 tree.gen_muons_pz[index],
                                 tree.gen_muons_energy[index])
        return genMuon


def recMuonLV(tree, index):                      # LV of RECO muon
        if index > tree.muons_nMuons or index == -1:
            print("============= >recMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        recMuon = TLorentzVector(tree.muons_px[index],
                                 tree.muons_py[index],
                                 tree.muons_pz[index],
                                 tree.muons_energy[index])
        return recMuon



def recoMuonMatchedIndex(tree, index_genMuon):    #  returns the index of reco Muon matched to given GEN muon
        list_dR_muon=[]
        genMuon = genMuonLV(tree, index_genMuon)

        for n in range(tree.muons_nMuons):
            recMatchedMuon = TLorentzVector(tree.muons_px[n], tree.muons_py[n], tree.muons_pz[n],tree.muons_energy[n])
            list_dR_muon.append([recMatchedMuon.DeltaR(genMuon), n, abs(recMatchedMuon.Pt() - genMuon.Pt())])
        list_dR_muon.sort(key=lambda element : element[0])
        if len(list_dR_muon)!=0  and  list_dR_muon[0][2] < 2 :return  list_dR_muon[0][1]
        return -1



def linked_gen_mu_index(tree, i):                 #
        if i == -1:return -1
        for k in range(0, tree.gen_muons_nMuons):
            if tree.gen_muons_genindex[k] == i: return k
        return -1




def simHitBelongToGenMuon(tree, isimHit, igenMuon ):
        simHit_genIndex = tree.simHits_genmuonindex[isimHit]
        if simHit_genIndex == -1: return False
        genMuon_genIndex = tree.gen_muons_genindex[igenMuon]
        if genMuon_genIndex == -1: return False
        if simHit_genIndex == genMuon_genIndex:return True
        return False




def LoopOverChambers(tree):
        chamberList = []
        for ec in range(0,2):
                for st in range(0,4):
                    for rg in range(0,4):
                        if st+1 > 1 and rg+1 > 2: continue
                        for ch in range(0,36):
                            if st+1 > 1 and rg+1 == 1 and ch+1 > 18: continue
#                            print '  EC  ', ec+1,'  st:  ', st+1 ,' rg:  ', rg+1, ' ch:  ', ch+1
                            chamber  = ChamberID(ec+1,st+1,rg+1,ch+1)
                            NSimHits = all_simhits_in_a_chamber(tree, chamber)
                            if(len(NSimHits)!=0):chamberList.append([len(NSimHits),chamber])
                            chamberList.sort(key=lambda element : element[0])
        return chamberList


def ChamberID(endcap, station, ring, chamber):
        return endcap*10000 + 1000*station + 100*ring + chamber


def Chamber_station(ChamberID):
        endcap  = round(ChamberID/10000)
        station = round( (ChamberID - endcap*10000)/1000)
        return station


def Chamber_ring(ChamberID):
        endcap  = round(ChamberID/10000)
        station = round( (ChamberID - endcap*10000)/1000)
        ring    = round( (ChamberID - endcap*10000 - station*1000)/100)
        return ring



def Chambers_crossedByGenMuon(tree, gen_muon_index):
        chamberList = []
        for n in range(0,tree.simHits_nSimHits):
            if simHitBelongToGenMuon(tree, n, gen_muon_index):
                endcap  = tree.simHits_ID_endcap[n]
                station = tree.simHits_ID_station[n]
                ring    = tree.simHits_ID_ring[n]
                chamber = tree.simHits_ID_chamber[n]
                chamberList.append(ChamberID(endcap,station,ring,chamber))
        out = [i for n, i in enumerate(chamberList) if i not in chamberList[:n]]  # remove duplicates as there are 6 entries if I count by simhits
        return out

#    def Chambers_Not_crossedByGenMuon(tree, gen_muon_index):
#        chamberList = []
#        for n in range(0,tree.simHits_nSimHits):
#            if simHitBelongToGenMuon(tree, n, gen_muon_index):
#                endcap  = tree.simHits_ID_endcap[n]
#                station = tree.simHits_ID_station[n]
#                ring    = tree.simHits_ID_ring[n]
#                chamber = tree.simHits_ID_chamber[n]
#                chamberList.append(ChamberID(endcap,station,ring,chamber))
#        out = [i for n, i in enumerate(chamberList) if i not in chamberList[:n]]  # remove duplicates as there are 6 entries if I count by simhits
#        return out





def Chambers_crossedByMuon(tree, muon_index):
        out = []
        for j in range(0, len(tree.muons_cscSegmentRecord_endcap[muon_index])):
            endcap  = tree.muons_cscSegmentRecord_endcap[muon_index][j];
            station = tree.muons_cscSegmentRecord_station[muon_index][j];
            ring    = tree.muons_cscSegmentRecord_ring[muon_index][j];
            chamber = tree.muons_cscSegmentRecord_chamber[muon_index][j];
            out.append(ChamberID(endcap,station,ring,chamber))
        return out




def AllGenRecoMuonsMap(tree):                     # matchig map btw reco-gen muons;  gen muon index comes first
        out = []
        for igen in range(tree.gen_muons_nMuons):
            recoMuIndex = recoMuonMatchedIndex(tree,igen)
            out.append([igen,recoMuIndex])
        return out




def SelectedGenRecoMuonsMap(tree, gen_muon_list):  # gen muon index comes first
        out = []
        for igen in gen_muon_list:
            recoMuIndex = recoMuonMatchedIndex(tree,igen)
            out.append([igen,recoMuIndex])
        return out



def GenCSCRecoMuonsMap(tree):                      #   GEN-RECO (in CSC)  Muons Map with some pre-selection;
        out = []
        for igen in range(tree.gen_muons_nMuons):
            muon = genMuonLV(tree,igen)


            if muon.Pt()> 15 and math.fabs(muon.Eta()) > 1.1 and math.fabs(muon.Eta()) < 2.4:
                recoMuIndex = recoMuonMatchedIndex(tree,igen)
                if recoMuIndex!=-1:
                        out.append([igen,recoMuIndex])
        return out


def allRecHits_belonging_toMuon(tree, muon_index):
        muon_rechits = []
        muon_segments = allSegments_belonging_toMuon(tree, muon_index)
        for s in muon_segments:
            for rc in allRechits_of_segment(tree, s):
                muon_rechits.append(rc)
        return muon_rechits



def allSimHits_belonging_toGenMuon(tree, gen_muon_index):
        muon_simhits = []
        for n in range(0,tree.simHits_nSimHits):
            if simHitBelongToGenMuon(tree,n,gen_muon_index):
                muon_simhits.append(n)
        return muon_simhits


def MuonSimSegment(tree, simhits, segment): #  sim semgent is a vector of simHits
        sim_segment = []
        segment_endcap     = tree.cscSegments_ID_endcap[segment]
        segment_station    = tree.cscSegments_ID_station[segment]
        segment_ring       = tree.cscSegments_ID_ring[segment]
        segment_chamber    = tree.cscSegments_ID_chamber[segment]
        chamber_of_segment = ChamberID(segment_endcap, segment_station, segment_ring, segment_chamber)

        for sh in simhits:
            Chamber = ChamberID(tree.simHits_ID_endcap[sh],tree.simHits_ID_station[sh],tree.simHits_ID_ring[sh], tree.simHits_ID_chamber[sh])
            if(Chamber == chamber_of_segment):
                sim_segment.append(sh)
        return sim_segment





def allSegments_belonging_toMuon(tree, muon_index):
        muon_segments = []
        if muon_index > tree.muons_nMuons:
            print("==== > allSegments_belonging_toMuon: Muon index out of range, return empty list  ")
            return muon_segments


        for s in range(tree.cscSegments_nSegments):

            segmentRing          = tree.cscSegments_ID_ring[s]
            segmentStation       = tree.cscSegments_ID_station[s]
            segmentEndcap        = tree.cscSegments_ID_endcap[s]
            segmentChamber       = tree.cscSegments_ID_chamber[s]

            segmenLocalX         = tree.cscSegments_localX[s]
            segmenLocalY         = tree.cscSegments_localY[s]

            segmentChamberID     = ChamberID(segmentEndcap, segmentStation, segmentRing, segmentChamber )

            for ms in range(0, len(tree.muons_cscSegmentRecord_endcap[muon_index])):
                 muon_segment_endcap     = tree.muons_cscSegmentRecord_endcap[muon_index][ms];
                 muon_segment_station    = tree.muons_cscSegmentRecord_station[muon_index][ms];
                 muon_segment_ring       = tree.muons_cscSegmentRecord_ring[muon_index][ms];
                 muon_segment_chamber    = tree.muons_cscSegmentRecord_chamber[muon_index][ms];
                 muon_segment_localX     = tree.muons_cscSegmentRecord_localX[muon_index][ms];
                 muon_segment_localY     = tree.muons_cscSegmentRecord_localY[muon_index][ms];

                 muonsegmentChamberID = ChamberID(muon_segment_endcap,muon_segment_station,muon_segment_ring,muon_segment_chamber)

#                 if (muonsegmentChamberID == segmentChamberID and
#                     segmenLocalX == muon_segment_localX      and
#                     segmenLocalY == muon_segment_localY): muon_segments.append(s)

                 if (muonsegmentChamberID == segmentChamberID): muon_segments.append(s) # relaxed


        return muon_segments

def allSegments_InChamber(tree,chamber):
        out = []
        for s in range(tree.cscSegments_nSegments):

            segmentRing          = tree.cscSegments_ID_ring[s]
            segmentStation       = tree.cscSegments_ID_station[s]
            segmentEndcap        = tree.cscSegments_ID_endcap[s]
            segmentChamber       = tree.cscSegments_ID_chamber[s]

            segmentChamberID     = ChamberID(segmentEndcap, segmentStation, segmentRing, segmentChamber )
            if segmentChamberID == chamber:
                out.append(s)
        return out


def allRechits_of_segment(tree, segment_index):

        segment_rechits = []
#        print("Segment:   ", segment_index,"", tree.cscSegments_nSegments)
        if segment_index > tree.cscSegments_nSegments:
            print("==== > allRechits_of_segment: Segment index out of range, return empty list  ")
            return segment_rechits

        segment_endcap     = tree.cscSegments_ID_endcap[segment_index]
        segment_station    = tree.cscSegments_ID_station[segment_index]
        segment_ring       = tree.cscSegments_ID_ring[segment_index]
        segment_chamber    = tree.cscSegments_ID_chamber[segment_index]
        chamber_of_segment = ChamberID(segment_endcap, segment_station, segment_ring, segment_chamber)


        for isegment_rechit in range(0 , len(tree.cscSegments_recHitRecord_endcap[segment_index])):
            chamber_of_srechit = ChamberID(tree.cscSegments_recHitRecord_endcap[segment_index][isegment_rechit],
                                                tree.cscSegments_recHitRecord_station[segment_index][isegment_rechit],
                                                tree.cscSegments_recHitRecord_ring[segment_index][isegment_rechit],
                                                tree.cscSegments_recHitRecord_chamber[segment_index][isegment_rechit])
            segment_rechit_localX = tree.cscSegments_recHitRecord_localX[segment_index][isegment_rechit]
            segment_rechit_localY = tree.cscSegments_recHitRecord_localY[segment_index][isegment_rechit]
            segment_rechit_layer  = tree.cscSegments_recHitRecord_layer[segment_index][isegment_rechit]


            for i2DRecHit in range(0, tree.recHits2D_nRecHits2D):
                layer_2DRecHit     = tree.recHits2D_ID_layer[i2DRecHit]
                localX_2DRecHit    = tree.recHits2D_localX[i2DRecHit]
                localY_2DRecHit    = tree.recHits2D_localY[i2DRecHit]

                localXerr_2DRecHit    = math.sqrt(tree.recHits2D_localXXerr[i2DRecHit])
                localYerr_2DRecHit    = math.sqrt(tree.recHits2D_localYYerr[i2DRecHit])
                if ChamberID(tree.recHits2D_ID_endcap[i2DRecHit],
                                  tree.recHits2D_ID_station[i2DRecHit],
                                  tree.recHits2D_ID_ring[i2DRecHit],
                                  tree.recHits2D_ID_chamber[i2DRecHit]) == chamber_of_srechit:


                    if(layer_2DRecHit == segment_rechit_layer   and
                       localX_2DRecHit == segment_rechit_localX and
                       localY_2DRecHit == segment_rechit_localY):

                        # mathc rechhits and segments withing 2 sigma, not exact as above (not very right)
#                    if(layer_2DRecHit == segment_rechit_layer  and (math.fabs(localX_2DRecHit -  segment_rechit_localX) < 3*sqrt(localXerr_2DRecHit)) and  
#                                                                   (math.fabs(localY_2DRecHit -  segment_rechit_localY) < 2*sqrt(localYerr_2DRecHit))):
#                        print('I would expect one to one equalk rechits:  ', localX_2DRecHit, '',' segment_rechit_localX   ', segment_rechit_localX, '  diff ', localX_2DRecHit - segment_rechit_localX)
                        segment_rechits.append(i2DRecHit)

        return segment_rechits




        


def allSegments_inChamber_NOT_belonging_toMuon(tree, chamber, muon):
        outlist = []
        muon_segments = allSegments_belonging_toMuon(tree, muon)
        for isegment in range(tree.cscSegments_nSegments):
            segment_endcap     = tree.cscSegments_ID_endcap[isegment]
            segment_station    = tree.cscSegments_ID_station[isegment]
            segment_ring       = tree.cscSegments_ID_ring[isegment]
            segment_chamber    = tree.cscSegments_ID_chamber[isegment]

            chamber_of_segment = ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber)
            if chamber_of_segment == chamber:
                if isegment not in muon_segments:
                    outlist.append(isegment)
        return outlist


def allSegments_NOT_belonging_toMuon(tree, muon):
        outlist = []
        muon_segments = allSegments_belonging_toMuon(tree, muon)
        for isegment in range(tree.cscSegments_nSegments):
            if isegment not in muon_segments:
                outlist.append(isegment)
        return outlist



def muonHasCSCSegements(tree, muon):
        if len(allSegments_belonging_toMuon(tree, muon))!=0: return True
        return False



def rechit_is_from_chamber(tree, rechit):
        chamber_rechit   = ChamberID(tree.recHits2D_ID_endcap[rechit],
                                          tree.recHits2D_ID_station[rechit],
                                          tree.recHits2D_ID_ring[rechit],
                                          tree.recHits2D_ID_chamber[rechit])
        return chamber_rechit


def all_rechits_in_a_chamber(tree, chamber):
        rechit_list = []
        for i2DRecHit in range(0, tree.recHits2D_nRecHits2D):
            if ChamberID(tree.recHits2D_ID_endcap[i2DRecHit],
                              tree.recHits2D_ID_station[i2DRecHit],
                              tree.recHits2D_ID_ring[i2DRecHit],
                              tree.recHits2D_ID_chamber[i2DRecHit] ) == chamber:
                rechit_list.append(i2DRecHit)
        return rechit_list





def all_muon_simhits_in_a_chamber(tree, chamber, gen_muon_index):
        simhit_list = []
        for n in range(0,tree.simHits_nSimHits):
            if( ChamberID(tree.simHits_ID_endcap[n],
                              tree.simHits_ID_station[n],
                              tree.simHits_ID_ring[n],
                              tree. simHits_ID_chamber[n]) == chamber and  simHitBelongToGenMuon(tree,n,gen_muon_index) ):
                simhit_list.append(n)
        return simhit_list



def all_simhits_in_a_chamber(tree, chamber):
        simhit_list = []
        for n in range(0,tree.simHits_nSimHits):
            if ChamberID(tree.simHits_ID_endcap[n],
                              tree.simHits_ID_station[n],
                              tree.simHits_ID_ring[n],
                              tree. simHits_ID_chamber[n] ) == chamber:
                simhit_list.append(n)
        return simhit_list

def RecHit_closest_SimHit(tree, rechit, SimHitsCollection): 
        chamber_rechit   = ChamberID(tree.recHits2D_ID_endcap[rechit],
                                     tree.recHits2D_ID_station[rechit],
                                     tree.recHits2D_ID_ring[rechit],
                                     tree.recHits2D_ID_chamber[rechit])
        layer_rechit     = tree.recHits2D_ID_layer[rechit]
        localX_rechit    = tree.recHits2D_localX[rechit]
        localY_rechit    = tree.recHits2D_localY[rechit]

#        simHits_inThisChamber = all_simhits_in_a_chamber(tree, chamber_rechit)
        simHits_inThisChamber = SimHitsCollection

        mindiff = 1000;  # why these values ?? 
        mindiffX = 99;
        mindiffY = 10;
        minR = 1000
        minX = 99
        indexX = -1  
        indexY = -1
        indexR = -1
        indexRX10 = -1
        for simhit in simHits_inThisChamber:
                if tree.simHits_ID_layer[simhit]  != layer_rechit: continue
                localX_simhit = tree.simHits_localX[simhit]
                localY_simhit = tree.simHits_localY[simhit]



#                if sqrt ( math.pow( localX_simhit - localX_rechit ,2)  + math.pow( localY_simhit - localY_rechit, 2 ))  <  mindiff:
#                        mindiff = math.pow( localX_simhit - localX_rechit ,2)  + math.pow( localY_simhit - localY_rechit, 2)
#                        indexR = simhit


#                if math.fabs( localX_simhit - localX_rechit ) < mindiffX:
#                        mindiffX =  math.fabs( localX_simhit - localX_rechit )
#                        indexX = simhit


#                if math.fabs( localY_simhit - localY_rechit ) < mindiffY:
#                        mindiffY = math.fabs( localY_simhit - localY_rechit )
#                        indexY = simhit



                if( sqrt(math.pow( localX_simhit - localX_rechit ,2)  + math.pow( localY_simhit - localY_rechit, 2))  <  minR and 
                    math.fabs( localX_simhit - localX_rechit ) < minX and 
                    math.fabs( localY_simhit - localY_rechit ) < 10 ): 
                        minR = sqrt(math.pow( localX_simhit - localX_rechit ,2)  + math.pow( localY_simhit - localY_rechit, 2))
                        minX = math.fabs( localX_simhit - localX_rechit )
                        indexRX10 = simhit


        return indexRX10  #return one of three



#def RecoSegmentAndSimHitMatch(tree, SegmentsAndSimHits): 
        
#        if




def rechit_is_from_segment(tree, rechit):

        SegmentIndex = -1

        chamber_rechit   = ChamberID(tree.recHits2D_ID_endcap[rechit],
                                          tree.recHits2D_ID_station[rechit],
                                          tree.recHits2D_ID_ring[rechit],
                                          tree.recHits2D_ID_chamber[rechit])
        layer_rechit     = tree.recHits2D_ID_layer[rechit]
        localX_rechit    = tree.recHits2D_localX[rechit]
        localY_rechit    = tree.recHits2D_localY[rechit]


        for s in range(tree.cscSegments_nSegments):

            chamber_segment = ChamberID(tree.cscSegments_ID_endcap[s],
                                             tree.cscSegments_ID_station[s],
                                             tree.cscSegments_ID_ring[s],
                                             tree.cscSegments_ID_chamber[s])

            if chamber_rechit == chamber_segment:

                for isegment_rechit in range(0 , len(tree.cscSegments_recHitRecord_endcap[s])):
                    chamber_of_srechit = ChamberID(tree.cscSegments_recHitRecord_endcap[s][isegment_rechit],
                                                        tree.cscSegments_recHitRecord_station[s][isegment_rechit],
                                                        tree.cscSegments_recHitRecord_ring[s][isegment_rechit],
                                                        tree.cscSegments_recHitRecord_chamber[s][isegment_rechit])
                    segment_rechit_localX = tree.cscSegments_recHitRecord_localX[s][isegment_rechit]
                    segment_rechit_localY = tree.cscSegments_recHitRecord_localY[s][isegment_rechit]
                    segment_rechit_layer  = tree.cscSegments_recHitRecord_layer[s][isegment_rechit]

                    if(chamber_of_srechit   == chamber_rechit        and
                       segment_rechit_layer == layer_rechit          and
                       localX_rechit        == segment_rechit_localX and
                       localY_rechit        == segment_rechit_localY ):
                        SegmentIndex = s



        return SegmentIndex

def MuonHasRecoSegmentInTheChamber(tree, good_chambers, recoMuIndex, allMuonSimHitsInChamber ): # check if segment is reconstructed for efficiency
        Segment_index = -1
        AllSegments = allSegments_InChamber(tree, good_chambers)
        for sg in AllSegments:
            RecoMuonIndexOfThisSegment = segment_is_from_muon(tree, sg)
#            print('check indices consistency  ', recoMuIndex,RecoMuonIndexOfThisSegment)
            if(RecoMuonIndexOfThisSegment == recoMuIndex):
                Segment_index = sg
        return Segment_index



def FoundMatchedSegment(tree, simsegment, chamber):

        AllSegments = allSegments_InChamber(tree, chamber)
        FoundMatchedSegment = False
        MatchedSegmentIndex = -1
        ThirdLayerSimHit = -1

        for isim in simsegment:
                if tree.simHits_ID_layer[isim]  == 3:  ThirdLayerSimHit = isim

        if ThirdLayerSimHit == -1: return -1


        XPull       =  3.5

        UpPullLow   = -1.5
        UpPullHigh  =  4

        MidPullLow   = -1.0
        MidPullHigh  =  4.0 

        BotPullLow   = -0.5
        BotPullHigh  =  3.5 

        minDiffX = 100.
        minDiffY = 100.


        for segment_index in AllSegments:
                if( math.fabs(tree.cscSegments_localX[segment_index] - tree.simHits_localX[ThirdLayerSimHit]) < minDiffX and 
                    math.fabs(tree.cscSegments_localY[segment_index] - tree.simHits_localY[ThirdLayerSimHit]) < minDiffY ):
                        minDiffX =  math.fabs(tree.cscSegments_localX[segment_index] - tree.simHits_localX[ThirdLayerSimHit])
                        minDiffY =  math.fabs(tree.cscSegments_localY[segment_index] - tree.simHits_localY[ThirdLayerSimHit])
                        MatchedSegmentIndex = segment_index




        if MatchedSegmentIndex!=-1:
                if math.fabs((tree.cscSegments_localX[segment_index] - tree.simHits_localX[ThirdLayerSimHit])/sqrt(tree.cscSegments_localXerr[segment_index])) < XPull:
                        if  tree.simHits_localY[ThirdLayerSimHit] < -30:
                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  BotPullLow and
                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  BotPullHigh:
                                        FoundMatchedSegment = True
                        if tree.simHits_localY[ThirdLayerSimHit] > -30 and tree.simHits_localY[ThirdLayerSimHit] < 30:
                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  MidPullLow and
                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  MidPullHigh:
                                        FoundMatchedSegment = True
                        if tree.simHits_localY[ThirdLayerSimHit] > 30:
                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  UpPullLow and
                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  UpPullHigh:
                                        FoundMatchedSegment = True


#        for segment_index in AllSegments:
#                if math.fabs((tree.cscSegments_localX[segment_index] - tree.simHits_localX[ThirdLayerSimHit])/sqrt(tree.cscSegments_localXerr[segment_index])) < XPull:
#                        if  tree.simHits_localY[ThirdLayerSimHit] < -30:
#                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  BotPullLow and
#                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  BotPullHigh:
#                                        FoundMatchedSegment = True
#                        if tree.simHits_localY[ThirdLayerSimHit] > -30 and tree.simHits_localY[ThirdLayerSimHit] < 30:
#                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  MidPullLow and
#                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  MidPullHigh:
#                                        FoundMatchedSegment = True
#                        if tree.simHits_localY[ThirdLayerSimHit] > 30:
#                                if( (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index] )   >  UpPullLow and
#                                    (tree.cscSegments_localY[segment_index]  - tree.simHits_localY[ThirdLayerSimHit])/sqrt(tree.cscSegments_localYerr[segment_index])  ) <  UpPullHigh:
#                                        FoundMatchedSegment = True

        if(FoundMatchedSegment == True):
                return MatchedSegmentIndex
        return -1


def SegmentFinderWithinAConeToMuon(tree, good_chambers , simsegment, genMuLV):  # NSegments in the viciinity of Gen Muon
        AllSegments = allSegments_InChamber(tree, good_chambers)
        MatchedSegments=[]
        for segment_index in AllSegments:
#            print('segment: ', segment_index, ' rec segment theta: ',  tree.cscSegments_localTheta[segment_index],  ' simHits_theta ', tree.simHits_theta[simsegment[0]])
#            print('segment: ', segment_index, ' rec segment phi: ',  tree.cscSegments_localPhi[segment_index],  ' simHits_phi ', tree.simHits_phi[simsegment[0]])
#            print('segment: ', segment_index, ' rec segment phi: ',  tree.cscSegments_globalPhi[segment_index], '  genMuLV:   ', genMuLV.Phi())
#            print("in the Cone ??? ")

            SegmentDir = TVector3(1,1,1)
            SegmentDir.SetTheta(tree.cscSegments_localTheta[segment_index])
            SegmentDir.SetPhi(tree.cscSegments_localPhi[segment_index])
            SegmentDir.SetMag(1)

            SimSegmentDir = TVector3(1,1,1)
            SimSegmentDir.SetTheta(tree.simHits_theta[simsegment[0]])
            SimSegmentDir.SetPhi(tree.simHits_phi[simsegment[0]])
            SimSegmentDir.SetMag(1)


            deltaT = SimSegmentDir.Theta() - SegmentDir.Theta()
            deltaP = SimSegmentDir.Phi() - SegmentDir.Phi()


            dR = math.sqrt( math.pow(deltaT,2)  + math.pow(deltaP,2)  )
            sorted_hists1D['MuSegmentdR'].Fill( dR )
            if( dR < 0.2 ): # 0.1
                MatchedSegments.append(segment_index)
        return MatchedSegments


def RecHitMatcher(tree, recosegments, simsegment):
        
        segment = recosegments[0]
        segment_rechits =  allRechits_of_segment( tree, segment )

        MatchedRechits = []
        for simhit in simsegment:
            simhit_layer = tree.simHits_ID_layer[simhit]
            for rechit in segment_rechits:
                rechit_layer   =   tree.recHits2D_ID_layer[rechit]
                if  rechit_layer != simhit_layer: continue
                if(math.fabs(tree.recHits2D_localX[rechit] - tree.simHits_localX[simhit]) < 3*sqrt(tree.recHits2D_localXXerr[rechit])  and
                   math.fabs(tree.recHits2D_localY[rechit] - tree.simHits_localY[simhit]) < 3*sqrt(tree.recHits2D_localYYerr[rechit])):
                    MatchedRechits.append(rechit)

        return MatchedRechits

def SegmentMatcher(tree, good_chambers , simsegment, genMuLV):
        
        AllSegments = allSegments_InChamber(tree, good_chambers)



#        print('--------------------------------- How many segments  ', len(AllSegments))
        for segment_index in AllSegments:
            N_matched_rechits = 0


            segment_rechits =  allRechits_of_segment( tree, segment_index )

            for rechit in segment_rechits:
              rechit_layer   =   tree.recHits2D_ID_layer[rechit]
              for simhit in simsegment:
                  simhit_layer = tree.simHits_ID_layer[simhit]
                  if simhit_layer != rechit_layer: continue
#                  print('delta X  ', (math.fabs(tree.recHits2D_localX[rechit] - tree.simHits_localX[simhit]) < 3*sqrt(tree.recHits2D_localXXerr[rechit])))
#                  print('delta Y  ', (math.fabs(tree.recHits2D_localY[rechit] - tree.simHits_localY[simhit]) < 3*sqrt(tree.recHits2D_localYYerr[rechit])))
                  if(math.fabs(tree.recHits2D_localX[rechit] - tree.simHits_localX[simhit]) < 3*sqrt(tree.recHits2D_localXXerr[rechit])  and
                     math.fabs(tree.recHits2D_localY[rechit] - tree.simHits_localY[simhit]) < 3*sqrt(tree.recHits2D_localYYerr[rechit])):                     N_matched_rechits += 1
#              print("N_matched_rechits  ", N_matched_rechits)
              if(N_matched_rechits == 3): return [True, segment_index]  # at least one hit
        return [False, -1]


def FindSegmentMatchedToSim(tree, good_chambers, simsegment):  # returns  index of matched reco segment and pulls
        matched_reco_segment_index = -1
        pullX = -5
        pullY = -5

        dX = -50
        dY = -50
        out = []
        AllSegments = allSegments_InChamber(tree, good_chambers)
#        print('How many segments  ', len(AllSegments))
        for segment in AllSegments:
#            print(' reco Segment Local X / Y', tree.cscSegments_localX[segment], '/', tree.cscSegments_localY[segment])
            for ss in simsegment:
                if tree.simHits_ID_layer[ss]==3:
                    pullX = (tree.simHits_localX[ss] - tree.cscSegments_localX[segment])/sqrt(tree.cscSegments_localXerr[segment])
                    pullY = (tree.simHits_localY[ss] - tree.cscSegments_localY[segment])/sqrt(tree.cscSegments_localYerr[segment])
                    dX = (tree.simHits_localX[ss] - tree.cscSegments_localX[segment])
                    dY = (tree.simHits_localY[ss] - tree.cscSegments_localY[segment])
                    if(math.fabs(tree.simHits_localX[ss] - tree.cscSegments_localX[segment]) < 4*sqrt(tree.cscSegments_localXerr[segment]) and
                       math.fabs(tree.simHits_localY[ss] - tree.cscSegments_localY[segment]) < 4*sqrt(tree.cscSegments_localYerr[segment])) :
                        matched_reco_segment_index = segment
        out.append(matched_reco_segment_index)
        out.append(pullX)
        out.append(pullY)
        out.append(dX)
        out.append(dY)
        return out


def SimRecoSegmentMatching(tree, chamber, simsegment, recoMuIndex):
        recosegment = MuonHasRecoSegmentInTheChamber(tree, chamber, recoMuIndex, simsegment)
        Matched = False
#        print('_____________________________________________________________________________________ ')
        if(recosegment!=-1):
            rechits_of_segment = allRechits_of_segment(tree, recosegment)

            RecHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;  3 - localErrXX; 4 - localErrYY
            SimHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;

#            print(' reco segment,   ', len(rechits_of_segment), '  sim_segment   ', len(simsegment) )
#            if(len(rechits_of_segment)!=len(simsegment)): print(" Attention!!!!!!!!!!!!!!!!!!!!!! ")
#            print("rec:")
            for rc in rechits_of_segment:
#                if(len(rechits_of_segment) >6 ): print("Attention!")
#                print(' layer  ', tree.recHits2D_ID_layer[rc], "  X : Y ", tree.recHits2D_localX[rc],"  :  ", tree.recHits2D_localY[rc])

                RecHitMatrix.append([ tree.recHits2D_ID_layer[rc], tree.recHits2D_localX[rc], tree.recHits2D_localY[rc], tree.recHits2D_localXXerr[rc], tree.recHits2D_localYYerr[rc] ])
#            print('-------')
#            print("sim:")
            for sh in simsegment:
#                print(' layer  ', tree.simHits_ID_layer[sh], "  X : Y ", tree.simHits_localX[sh],"  :  ", tree.simHits_localY[sh])
                SimHitMatrix.append([ tree.simHits_ID_layer[sh], tree.simHits_localX[sh], tree.simHits_localY[sh]])

            RecHitMatrix.sort(key=lambda element : element[0])
            SimHitMatrix.sort(key=lambda element : element[0])
            # Lets start from a simple case when NSimHits == NRecHits
            RecHitsLayers = []
            if(len(RecHitMatrix) <= len(SimHitMatrix)):
                MatchedInAllLayers = True

                for i in range(len(RecHitMatrix)):
                    RecHitsLayers.append(RecHitMatrix[i][0])
#                    print(' layer  rec  ', RecHitMatrix[i][0] , '  X / Y ',RecHitMatrix[i][1], ' / ', RecHitMatrix[i][2]  )
#                    print(' layer  sim  ', SimHitMatrix[i][0] , '  X / Y ',SimHitMatrix[i][1], ' / ', SimHitMatrix[i][2]  )
#                    print(' Delta X    ', math.fabs(RecHitMatrix[i][1] - SimHitMatrix[i][1]), ' +-  ', 2*sqrt(RecHitMatrix[i][3]),
#                          ' DeltaY     ', math.fabs(RecHitMatrix[i][2] - SimHitMatrix[i][2]), ' +-  ', 2*sqrt(RecHitMatrix[i][4]))
                    if(math.fabs(RecHitMatrix[i][1] - SimHitMatrix[i][1]) > 3*sqrt(RecHitMatrix[i][3]) or math.fabs(RecHitMatrix[i][2] - SimHitMatrix[i][2]) > 3*sqrt(RecHitMatrix[i][4])):
#                        print(' Layer is not matched  !  ')
                        MatchedInAllLayers = False
                Matched = MatchedInAllLayers

#            print('  Duplicate layers in rec segment   ', len(RecHitsLayers)!= len(set(RecHitsLayers)))

            if(len(RecHitsLayers)!= len(set(RecHitsLayers)) and not Matched):
                duplist = []  #  save only duplicated layers ( I suppose that other layers are well matched)
                newlist = []
                for k in RecHitsLayers:
                    if k not in newlist:
                        newlist.append(k)
                    else:
                        duplist.append(k)

                MatchedInDuplicatedLayers = False
                for i in range(len(RecHitMatrix)):
                    for j in range(len(SimHitMatrix)):
                        if(SimHitMatrix[j][0] == RecHitMatrix[i][0] and RecHitMatrix[i][0] in duplist): # layers are equal
#                            print(' attempt to resolve duplicates  in layer  ', )
#                            print(' layer  ', RecHitMatrix[i][0],  ' Delta X    ', math.fabs(RecHitMatrix[i][1] - SimHitMatrix[j][1]), ' +-  ', 2*sqrt(RecHitMatrix[i][3]),
#                                  ' Delta Y     ', math.fabs(RecHitMatrix[i][2] - SimHitMatrix[j][2]), ' +-  ', 2*sqrt(RecHitMatrix[i][4]))
                            if(math.fabs(RecHitMatrix[i][1] - SimHitMatrix[j][1]) < 3*sqrt(RecHitMatrix[i][3]) or math.fabs(RecHitMatrix[i][2] - SimHitMatrix[j][2]) < 3*sqrt(RecHitMatrix[i][4])):
                                MatchedInDuplicatedLayers = True
#                                print('Matched in duplicated  ', MatchedInDuplicatedLayers)
                Matched = MatchedInDuplicatedLayers


            if(len(RecHitMatrix) >  len(SimHitMatrix)): # it means certainly there are duplicates, then check SIM to REC matching, if 6 times found declare segment as matched
                n=0
                for j in range(len(SimHitMatrix)):
                    FoundMatchedLayer = False
                    for i in range(len(RecHitMatrix)):
                        if(math.fabs(RecHitMatrix[i][1] - SimHitMatrix[j][1]) < 3*sqrt(RecHitMatrix[i][3]) or math.fabs(RecHitMatrix[i][2] - SimHitMatrix[j][2]) < 3*sqrt(RecHitMatrix[i][4])):
#                            print(' attempt to resolve duplicates  in layer when Nrec > NSim  ', )
#                            print(' layer  ', RecHitMatrix[i][0],  ' Delta X    ', math.fabs(RecHitMatrix[i][1] - SimHitMatrix[j][1]), ' +-  ', 2*sqrt(RecHitMatrix[i][3]),
#                                  ' Delta Y     ', math.fabs(RecHitMatrix[i][2] - SimHitMatrix[j][2]), ' +-  ', 2*sqrt(RecHitMatrix[i][4]))
                            FoundMatchedLayer = True
                    if(FoundMatchedLayer):n=n+1
                if(n==6):
#                    print('  Matched  n ', n)
                    Matched = True
#        print('Finally what do i return  ', Matched)
        return Matched



def DublicateLayersInRecoSegment(tree, chamber, simsegment, recoMuIndex):
        recosegment = MuonHasRecoSegmentInTheChamber(tree, chamber, recoMuIndex, simsegment)
        RecHitsLayers = []
        if(recosegment!=-1):
            rechits_of_segment = allRechits_of_segment(tree, recosegment)
            RecHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;  3 - localErrXX; 4 - localErrYY

            for rc in rechits_of_segment:
                RecHitMatrix.append([ tree.recHits2D_ID_layer[rc], tree.recHits2D_localX[rc], tree.recHits2D_localY[rc], tree.recHits2D_localXXerr[rc], tree.recHits2D_localYYerr[rc] ])

            RecHitMatrix.sort(key=lambda element : element[0])
            for i in range(len(RecHitMatrix)):
                    RecHitsLayers.append(RecHitMatrix[i][0])
        return len(RecHitsLayers)!= len(set(RecHitsLayers))


def segment_is_from_muon(tree, segment):
        MuonIndex = -1
        segment_endcap     = tree.cscSegments_ID_endcap[segment]
        segment_station    = tree.cscSegments_ID_station[segment]
        segment_ring       = tree.cscSegments_ID_ring[segment]
        segment_chamber    = tree.cscSegments_ID_chamber[segment]
        segment_LocalX     = tree.cscSegments_localX[segment]
        segment_LocalY     = tree.cscSegments_localY[segment]

        chamberID_of_segment = ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber)
        for m in range(tree.muons_nMuons):
            for s in range(0, len(tree.muons_cscSegmentRecord_endcap[m])):
                 muon_segment_endcap     = tree.muons_cscSegmentRecord_endcap[m][s];
                 muon_segment_station    = tree.muons_cscSegmentRecord_station[m][s];
                 muon_segment_ring       = tree.muons_cscSegmentRecord_ring[m][s];
                 muon_segment_chamber    = tree.muons_cscSegmentRecord_chamber[m][s];

                 muon_segment_localX     = tree.muons_cscSegmentRecord_localX[m][s];
                 muon_segment_localY     = tree.muons_cscSegmentRecord_localY[m][s];

                 muonsegmentChamberID = ChamberID(muon_segment_endcap,muon_segment_station,muon_segment_ring,muon_segment_chamber)
                 if muonsegmentChamberID == chamberID_of_segment:
                     if muon_segment_localX == segment_LocalX:
                         if segment_LocalY == muon_segment_localY:
                             MuonIndex = m
        return  MuonIndex


#    def rechit_is_from_muon(tree, rechit):


def link_rechits_to_segments(tree, list_of_segments):
        outlist = []
        for i in list_of_segments:
            outlist.append([i,allRechits_of_segment(tree, i)])
        return outlist


