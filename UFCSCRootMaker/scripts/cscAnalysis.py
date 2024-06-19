#!/usr/bin/env python


import sys, os, pwd, commands
import optparse, shlex, re
import math
from ROOT import *
import ROOT
from array import array
from numpy import sqrt 
ROOT.gStyle.SetTitleYOffset(1.5)


def parseOptions():
    
    usage = ('usage: %prog [options] \n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    parser.add_option('-b', action='store_true', dest='noX', default=True ,help='no X11 windows')
    parser.add_option('-m','--isMC', dest='isMC', type='int', default=1 ,help='isMC default:0')
    parser.add_option('-f','--file', dest='file', type='string', default='cscRootMaker.root' ,help='file default:blank')
    parser.add_option('-n','--maxEvents', dest='maxEvents', type='int', default=10000000 ,help='maxEvents default:100000')
    parser.add_option('-d','--outDir', dest='outDir', type='string',
                      default='output/' ,help='out directory default:CSC')
    parser.add_option('-j','--jobName',dest='jobName',type='string', default='cscOverview',help='name of job and output files')

    parser.add_option('--isDigi', dest='isDigi', type='int', default=1 ,help='isDigi default:1')
    parser.add_option('--isLocalReco', dest='isLocalReco', type='int', default=1 ,help='isLocalReco default:1')
    parser.add_option('--isFullReco', dest='isFullReco', type='int', default=1 ,help='isFullReco default:1')
    parser.add_option('-c','--condition', dest='condition', type='int', default=1 ,help='condition: 1')
    parser.add_option('-r','--ME11', dest='ME11', type='int', default=1 ,help='Include    ME11 chambers: 0')
    parser.add_option('-k','--ME21', dest='ME21', type='int', default=1 ,help='Only       ME21 chambers: 1')
        
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    


class Analysis():

    def __init__(self):

        self.hists1D = {}
        self.hists2D = {}

        self.sorted_hists1D    = {}
        self.sorted_hists2D    = {}
        self.sorted_efficiency = {}

        self.eff_denum_hists1D = {}

        self.totalEvents = 0

        self.simHitsOverallEffDen = 0
        self.simHitsOverallEffNum = 0
        self.simHitsEffDen = [0] * 600
        self.simHitsEffNum = [0] * 600
        self.simHitsLayerEffDen = [[0 for dim1 in range(6)] for dim2 in range(600)]
        self.simHitsLayerEffNum = [[0 for dim1 in range(6)] for dim2 in range(600)]

        self.simHitsChamberEffNum = [[[[[0 for dim1 in range(6)] for dim2 in range(36)] for dim3 in range(4)] for dim4 in range(4)] for dim5 in range(2)]
        self.simHitsChamberEffDen = [[[[[0 for dim1 in range(6)] for dim2 in range(36)] for dim3 in range(4)] for dim4 in range(4)] for dim5 in range(2)]



        self.stationRings = ['ME-1/4','ME-1/3','ME-4/2','ME-3/2','ME-2/2','ME-1/2','ME-4/1','ME-3/1','ME-2/1','ME-1/1',
                             'ME+1/1','ME+2/1','ME+3/1','ME+4/1','ME+1/2','ME+2/2','ME+3/2','ME+4/2','ME+1/3','ME+1/4']
        self.stations = ['ME-1','ME-2','ME-3','ME-4','ME+1','ME+2','ME+3','ME+4']

        self.nChambers = {}
        self.nChambers['ME-1/1'] = 36
        self.nChambers['ME-1/2'] = 36
        self.nChambers['ME-1/3'] = 36
        self.nChambers['ME-1/4'] = 36
        self.nChambers['ME-2/1'] = 18
        self.nChambers['ME-2/2'] = 36
        self.nChambers['ME-3/1'] = 18
        self.nChambers['ME-3/2'] = 36
        self.nChambers['ME-4/1'] = 18
        self.nChambers['ME-4/2'] = 36
        self.nChambers['ME+1/1'] = 36
        self.nChambers['ME+1/2'] = 36
        self.nChambers['ME+1/3'] = 36
        self.nChambers['ME+1/4'] = 36
        self.nChambers['ME+2/1'] = 18
        self.nChambers['ME+2/2'] = 36
        self.nChambers['ME+3/1'] = 18
        self.nChambers['ME+3/2'] = 36
        self.nChambers['ME+4/1'] = 18
        self.nChambers['ME+4/2'] = 36

        self.nRecHitsPerStation = {}
        self.nRecHitsPerLayer   = [[[[[0 for dim1 in range(6)] for dim2 in range(36)] for dim3 in range(4)] for dim4 in range(4)] for dim5 in range(2)]
        for key in self.stationRings:
            self.nRecHitsPerStation[key] = 0

        self.defineHistos()

        self.simHits_muonMatched = []
        self.recHits_muonMatched = []

    def findMuonsFromZ(self, tree):  #  forward region and pt > 15
        Index = []
        for k in range(0, tree.gen_muons_nMuons):
            if (tree.gen_muons_mother_pdgId[k] == 23):
                LV = self.genMuonLV(tree, k)
                if(LV.Pt() > 15 and math.fabs(LV.Eta()) > 1.1 and math.fabs(LV.Eta()) < 2.3):
                    Index.append(k)
        return Index


    def genMuonLV(self, tree, index):                      # LV of GEN muon
        if index > tree.gen_muons_nMuons or index == -1:
            print("============= >  genMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        genMuon = TLorentzVector(tree.gen_muons_px[index],
                                 tree.gen_muons_py[index],
                                 tree.gen_muons_pz[index],
                                 tree.gen_muons_energy[index])
        return genMuon


    def recMuonLV(self, tree, index):                      # LV of RECO muon
        if index > tree.muons_nMuons or index == -1:
            print("============= >recMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        recMuon = TLorentzVector(tree.muons_px[index],
                                 tree.muons_py[index],
                                 tree.muons_pz[index],
                                 tree.muons_energy[index])
        return recMuon



    def recoMuonMatchedIndex(self, tree, index_genMuon):    #  returns the index of reco Muon matched to given GEN muon
        list_dR_muon=[]
        genMuon = self.genMuonLV(tree, index_genMuon)

        for n in range(tree.muons_nMuons):
            recMatchedMuon = TLorentzVector(tree.muons_px[n], tree.muons_py[n], tree.muons_pz[n],tree.muons_energy[n])
            list_dR_muon.append([recMatchedMuon.DeltaR(genMuon), n, abs(recMatchedMuon.Pt() - genMuon.Pt())])
        list_dR_muon.sort(key=lambda element : element[0])    
        if len(list_dR_muon)!=0  and  list_dR_muon[0][2] < 2 :return  list_dR_muon[0][1]
        return -1
        


    def linked_gen_mu_index(self, tree, i):                 #     
        if i == -1:return -1
        for k in range(0, tree.gen_muons_nMuons):
            if tree.gen_muons_genindex[k] == i: return k
        return -1




    def simHitBelongToGenMuon(self, tree, isimHit, igenMuon ):
        simHit_genIndex = tree.simHits_genmuonindex[isimHit]
        if simHit_genIndex == -1: return False
        genMuon_genIndex = tree.gen_muons_genindex[igenMuon]
        if genMuon_genIndex == -1: return False
        if simHit_genIndex == genMuon_genIndex:return True
        return False


    def LoopOverChambers(self, tree):
        chamberList = []
        for ec in range(0,2):
                for st in range(0,4):
                    for rg in range(0,4):
                        if st+1 > 1 and rg+1 > 2: continue
                        for ch in range(0,36):
                            if st+1 > 1 and rg+1 == 1 and ch+1 > 18: continue
#                            print '  EC  ', ec+1,'  st:  ', st+1 ,' rg:  ', rg+1, ' ch:  ', ch+1
                            chamber  = self.ChamberID(ec+1,st+1,rg+1,ch+1)
                            NSimHits = self.all_simhits_in_a_chamber(tree, chamber)
                            if(len(NSimHits)!=0):chamberList.append([len(NSimHits),chamber])
                            chamberList.sort(key=lambda element : element[0])
        return chamberList


    def ChamberID(self, endcap, station, ring, chamber):
        return endcap*10000 + 1000*station + 100*ring + chamber


    def Chamber_station(self, ChamberID):
        endcap  = round(ChamberID/10000)
        station = round( (ChamberID - endcap*10000)/1000)
        return station

    def Chamber_ring(self, ChamberID):
        endcap  = round(ChamberID/10000)
        station = round( (ChamberID - endcap*10000)/1000)
        ring    = round( (ChamberID - endcap*10000 - station*1000)/100)
        return ring



    def Chambers_crossedByGenMuon(self, tree, gen_muon_index):
        chamberList = []
        for n in range(0,tree.simHits_nSimHits):
            if self.simHitBelongToGenMuon(tree, n, gen_muon_index):
                endcap  = tree.simHits_ID_endcap[n]
                station = tree.simHits_ID_station[n]
                ring    = tree.simHits_ID_ring[n]
                chamber = tree.simHits_ID_chamber[n]
                chamberList.append(self.ChamberID(endcap,station,ring,chamber))
        out = [i for n, i in enumerate(chamberList) if i not in chamberList[:n]]  # remove duplicates as there are 6 entries if I count by simhits
        return out

#    def Chambers_Not_crossedByGenMuon(self, tree, gen_muon_index):
#        chamberList = []
#        for n in range(0,tree.simHits_nSimHits):
#            if self.simHitBelongToGenMuon(tree, n, gen_muon_index):
#                endcap  = tree.simHits_ID_endcap[n]
#                station = tree.simHits_ID_station[n]
#                ring    = tree.simHits_ID_ring[n]
#                chamber = tree.simHits_ID_chamber[n]
#                chamberList.append(self.ChamberID(endcap,station,ring,chamber))
#        out = [i for n, i in enumerate(chamberList) if i not in chamberList[:n]]  # remove duplicates as there are 6 entries if I count by simhits
#        return out





    def Chambers_crossedByMuon(self, tree, muon_index):
        out = []
        for j in range(0, len(tree.muons_cscSegmentRecord_endcap[muon_index])):
            endcap  = tree.muons_cscSegmentRecord_endcap[muon_index][j];
            station = tree.muons_cscSegmentRecord_station[muon_index][j];
            ring    = tree.muons_cscSegmentRecord_ring[muon_index][j];
            chamber = tree.muons_cscSegmentRecord_chamber[muon_index][j];
            out.append(self.ChamberID(endcap,station,ring,chamber))
        return out




    def AllGenRecoMuonsMap(self, tree):                     # matchig map btw reco-gen muons;  gen muon index comes first
        out = []
        for igen in range(tree.gen_muons_nMuons):
            recoMuIndex = self.recoMuonMatchedIndex(tree,igen)
            out.append([igen,recoMuIndex])
        return out




    def SelectedGenRecoMuonsMap(self, tree, gen_muon_list):  # gen muon index comes first
        out = []
        for igen in gen_muon_list:
            recoMuIndex = self.recoMuonMatchedIndex(tree,igen)
            out.append([igen,recoMuIndex])
        return out



    def GenCSCRecoMuonsMap(self, tree):                      #   GEN-RECO (in CSC)  Muons Map with some pre-selection;
        out = []
        for igen in range(tree.gen_muons_nMuons):
            muon = self.genMuonLV(tree,igen)


            if muon.Pt()> 15 and math.fabs(muon.Eta()) > 1.1 and math.fabs(muon.Eta()) < 2.4:
                recoMuIndex = self.recoMuonMatchedIndex(tree,igen)
                if recoMuIndex!=-1:
                        out.append([igen,recoMuIndex])
        return out


    def allRecHits_belonging_toMuon(self, tree, muon_index):
        muon_rechits = []
        muon_segments = self.allSegments_belonging_toMuon(tree, muon_index)
        for s in muon_segments:
            for rc in self.allRechits_of_segment(tree, s):
                muon_rechits.append(rc)
        return muon_rechits



    def allSimHits_belonging_toGenMuon(self, tree, gen_muon_index):
        muon_simhits = []
        for n in range(0,tree.simHits_nSimHits):
            if self.simHitBelongToGenMuon(tree,n,gen_muon_index):
                muon_simhits.append(n)
        return muon_simhits


    def MuonSimSegment(self, tree, simhits, segment): #  sim semgent is a vector of simHits
        sim_segment = []
        segment_endcap     = tree.cscSegments_ID_endcap[segment]
        segment_station    = tree.cscSegments_ID_station[segment]
        segment_ring       = tree.cscSegments_ID_ring[segment]
        segment_chamber    = tree.cscSegments_ID_chamber[segment]
        chamber_of_segment = self.ChamberID(segment_endcap, segment_station, segment_ring, segment_chamber)

        for sh in simhits:
            Chamber = self.ChamberID(tree.simHits_ID_endcap[sh],tree.simHits_ID_station[sh],tree.simHits_ID_ring[sh], tree.simHits_ID_chamber[sh])
            if(Chamber == chamber_of_segment):
                sim_segment.append(sh)
        return sim_segment





    def allSegments_belonging_toMuon(self, tree, muon_index):
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

            segmentChamberID     = self.ChamberID(segmentEndcap, segmentStation, segmentRing, segmentChamber )

            for ms in range(0, len(tree.muons_cscSegmentRecord_endcap[muon_index])):
                 muon_segment_endcap     = tree.muons_cscSegmentRecord_endcap[muon_index][ms];
                 muon_segment_station    = tree.muons_cscSegmentRecord_station[muon_index][ms];
                 muon_segment_ring       = tree.muons_cscSegmentRecord_ring[muon_index][ms];
                 muon_segment_chamber    = tree.muons_cscSegmentRecord_chamber[muon_index][ms];
                 muon_segment_localX     = tree.muons_cscSegmentRecord_localX[muon_index][ms];
                 muon_segment_localY     = tree.muons_cscSegmentRecord_localY[muon_index][ms];

                 muonsegmentChamberID = self.ChamberID(muon_segment_endcap,muon_segment_station,muon_segment_ring,muon_segment_chamber)

#                 if (muonsegmentChamberID == segmentChamberID and  
#                     segmenLocalX == muon_segment_localX      and  
#                     segmenLocalY == muon_segment_localY): muon_segments.append(s)

                 if (muonsegmentChamberID == segmentChamberID): muon_segments.append(s) # relaxed


        return muon_segments
                     
    def allSegments_InChamber(self,tree,chamber):
        out = []
        for s in range(tree.cscSegments_nSegments):

            segmentRing          = tree.cscSegments_ID_ring[s]
            segmentStation       = tree.cscSegments_ID_station[s]
            segmentEndcap        = tree.cscSegments_ID_endcap[s] 
            segmentChamber       = tree.cscSegments_ID_chamber[s]

            segmentChamberID     = self.ChamberID(segmentEndcap, segmentStation, segmentRing, segmentChamber )
            if segmentChamberID == chamber:
                out.append(s)
        return out
        

    def allRechits_of_segment(self, tree, segment_index):

        segment_rechits = []
#        print("Segment:   ", segment_index,"", tree.cscSegments_nSegments)
        if segment_index > tree.cscSegments_nSegments:
            print("==== > allRechits_of_segment: Segment index out of range, return empty list  ")
            return segment_rechits

        segment_endcap     = tree.cscSegments_ID_endcap[segment_index]
        segment_station    = tree.cscSegments_ID_station[segment_index]
        segment_ring       = tree.cscSegments_ID_ring[segment_index]
        segment_chamber    = tree.cscSegments_ID_chamber[segment_index]
        chamber_of_segment = self.ChamberID(segment_endcap, segment_station, segment_ring, segment_chamber)


        for isegment_rechit in range(0 , len(tree.cscSegments_recHitRecord_endcap[segment_index])):
            chamber_of_srechit = self.ChamberID(tree.cscSegments_recHitRecord_endcap[segment_index][isegment_rechit],
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
                if self.ChamberID(tree.recHits2D_ID_endcap[i2DRecHit],
                                  tree.recHits2D_ID_station[i2DRecHit],
                                  tree.recHits2D_ID_ring[i2DRecHit],
                                  tree.recHits2D_ID_chamber[i2DRecHit]) == chamber_of_srechit:
                          
                          
#                    if(layer_2DRecHit == segment_rechit_layer   and 
#                       localX_2DRecHit == segment_rechit_localX and 
#                       localY_2DRecHit == segment_rechit_localY):

# mathc rechhits and segments withing 2 sigma, not exact as above
                    if(layer_2DRecHit == segment_rechit_layer  and (math.fabs(localX_2DRecHit -  segment_rechit_localX) < 3*sqrt(localXerr_2DRecHit)) and  (math.fabs(localY_2DRecHit -  segment_rechit_localY) < 2*sqrt(localYerr_2DRecHit))):
#                        print('I would expect one to one equalk rechits:  ', localX_2DRecHit, '',' segment_rechit_localX   ', segment_rechit_localX, '  diff ', localX_2DRecHit - segment_rechit_localX)
                        segment_rechits.append(i2DRecHit)

        return segment_rechits



#    def allSegmentsInChamber(self, tree, chamber):
#        outlist = []
#        chamber = idchamber%100;
#        ring    = int(idchamber/100)%10;
#        station = int(idchamber/1000)%10;
#        endcap  = int(idchamber/10000);


    def allSegments_inChamber_NOT_belonging_toMuon(self, tree, chamber, muon):
        outlist = []
        muon_segments = self.allSegments_belonging_toMuon(tree, muon)
        for isegment in range(tree.cscSegments_nSegments):
            segment_endcap     = tree.cscSegments_ID_endcap[isegment]
            segment_station    = tree.cscSegments_ID_station[isegment]
            segment_ring       = tree.cscSegments_ID_ring[isegment]
            segment_chamber    = tree.cscSegments_ID_chamber[isegment]

            chamber_of_segment = self.ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber)
            if chamber_of_segment == chamber:
                if isegment not in muon_segments:
                    outlist.append(isegment)
        return outlist


    def allSegments_NOT_belonging_toMuon(self, tree, muon):
        outlist = []
        muon_segments = self.allSegments_belonging_toMuon(tree, muon)
        for isegment in range(tree.cscSegments_nSegments):
            if isegment not in muon_segments:
                outlist.append(isegment)
        return outlist



    def muonHasCSCSegements(self, tree, muon):
        if len(self.allSegments_belonging_toMuon(tree, muon))!=0: return True
        return False



    def rechit_is_from_chamber(self, tree, rechit):
        chamber_rechit   = self.ChamberID(tree.recHits2D_ID_endcap[rechit],
                                          tree.recHits2D_ID_station[rechit],
                                          tree.recHits2D_ID_ring[rechit],
                                          tree.recHits2D_ID_chamber[rechit])
        return chamber_rechit


    def all_rechits_in_a_chamber(self, tree, chamber):
        rechit_list = []
        for i2DRecHit in range(0, tree.recHits2D_nRecHits2D):
            if self.ChamberID(tree.recHits2D_ID_endcap[i2DRecHit],
                              tree.recHits2D_ID_station[i2DRecHit],
                              tree.recHits2D_ID_ring[i2DRecHit],
                              tree.recHits2D_ID_chamber[i2DRecHit] ) == chamber:
                rechit_list.append(i2DRecHit)
        return rechit_list




        
    def all_muon_simhits_in_a_chamber(self, tree, chamber, gen_muon_index):
        simhit_list = []
        for n in range(0,tree.simHits_nSimHits):
            if( self.ChamberID(tree.simHits_ID_endcap[n],
                              tree.simHits_ID_station[n],
                              tree.simHits_ID_ring[n],
                              tree. simHits_ID_chamber[n]) == chamber and  self.simHitBelongToGenMuon(tree,n,gen_muon_index) ):
                simhit_list.append(n)
        return simhit_list



    def all_simhits_in_a_chamber(self, tree, chamber):
        simhit_list = []
        for n in range(0,tree.simHits_nSimHits):
            if self.ChamberID(tree.simHits_ID_endcap[n],
                              tree.simHits_ID_station[n],
                              tree.simHits_ID_ring[n],
                              tree. simHits_ID_chamber[n] ) == chamber:
                simhit_list.append(n)
        return simhit_list

        

    def rechit_is_from_segment(self, tree, rechit):

        SegmentIndex = -1

        chamber_rechit   = self.ChamberID(tree.recHits2D_ID_endcap[rechit],
                                          tree.recHits2D_ID_station[rechit],
                                          tree.recHits2D_ID_ring[rechit],
                                          tree.recHits2D_ID_chamber[rechit])
        layer_rechit     = tree.recHits2D_ID_layer[rechit]
        localX_rechit    = tree.recHits2D_localX[rechit]
        localY_rechit    = tree.recHits2D_localY[rechit]


        for s in range(tree.cscSegments_nSegments):

            chamber_segment = self.ChamberID(tree.cscSegments_ID_endcap[s],
                                             tree.cscSegments_ID_station[s],
                                             tree.cscSegments_ID_ring[s],
                                             tree.cscSegments_ID_chamber[s])

            if chamber_rechit == chamber_segment:
                
                for isegment_rechit in range(0 , len(tree.cscSegments_recHitRecord_endcap[s])):
                    chamber_of_srechit = self.ChamberID(tree.cscSegments_recHitRecord_endcap[s][isegment_rechit],
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

    def MuonHasRecoSegmentInTheChamber(self, tree, good_chambers, recoMuIndex, allMuonSimHitsInChamber ): # check if segment is reconstructed for efficiency
        Segment_index = -1
        AllSegments = self.allSegments_InChamber(tree, good_chambers)
        for sg in AllSegments:
            RecoMuonIndexOfThisSegment = self.segment_is_from_muon(tree, sg)
#            print('check indices consistency  ', recoMuIndex,RecoMuonIndexOfThisSegment)
            if(RecoMuonIndexOfThisSegment == recoMuIndex):
                Segment_index = sg
        return Segment_index


    def FindSegmentMatchedToSim(self, tree, good_chambers, simsegment):  # returns  index of matched reco segment and pulls 
        matched_reco_segment_index = -1 
        pullX = -5
        pullY = -5

        dX = -50
        dY = -50
        out = []
        AllSegments = self.allSegments_InChamber(tree, good_chambers)
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


    def SimRecoSegmentMatching(self, tree, chamber, simsegment, recoMuIndex):
        recosegment = self.MuonHasRecoSegmentInTheChamber(tree, chamber, recoMuIndex, simsegment)
        Matched = False
#        print('_____________________________________________________________________________________ ')
        if(recosegment!=-1):
            rechits_of_segment = self.allRechits_of_segment(tree, recosegment)

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



    def DublicateLayersInRecoSegment(self, tree, chamber, simsegment, recoMuIndex):
        recosegment = self.MuonHasRecoSegmentInTheChamber(tree, chamber, recoMuIndex, simsegment)
        RecHitsLayers = []
        if(recosegment!=-1):
            rechits_of_segment = self.allRechits_of_segment(tree, recosegment)
            RecHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;  3 - localErrXX; 4 - localErrYY

            for rc in rechits_of_segment:
                RecHitMatrix.append([ tree.recHits2D_ID_layer[rc], tree.recHits2D_localX[rc], tree.recHits2D_localY[rc], tree.recHits2D_localXXerr[rc], tree.recHits2D_localYYerr[rc] ]) 

            RecHitMatrix.sort(key=lambda element : element[0])
            for i in range(len(RecHitMatrix)):
                    RecHitsLayers.append(RecHitMatrix[i][0])
        return len(RecHitsLayers)!= len(set(RecHitsLayers))


    def segment_is_from_muon(self, tree, segment):
        MuonIndex = -1
        segment_endcap     = tree.cscSegments_ID_endcap[segment]
        segment_station    = tree.cscSegments_ID_station[segment]
        segment_ring       = tree.cscSegments_ID_ring[segment]
        segment_chamber    = tree.cscSegments_ID_chamber[segment]
        segment_LocalX     = tree.cscSegments_localX[segment] 
        segment_LocalY     = tree.cscSegments_localY[segment] 

        chamberID_of_segment = self.ChamberID(segment_endcap,segment_station,segment_ring,segment_chamber)
        for m in range(tree.muons_nMuons):
            for s in range(0, len(tree.muons_cscSegmentRecord_endcap[m])):
                 muon_segment_endcap     = tree.muons_cscSegmentRecord_endcap[m][s];
                 muon_segment_station    = tree.muons_cscSegmentRecord_station[m][s];
                 muon_segment_ring       = tree.muons_cscSegmentRecord_ring[m][s];
                 muon_segment_chamber    = tree.muons_cscSegmentRecord_chamber[m][s];

                 muon_segment_localX     = tree.muons_cscSegmentRecord_localX[m][s];
                 muon_segment_localY     = tree.muons_cscSegmentRecord_localY[m][s];

                 muonsegmentChamberID = self.ChamberID(muon_segment_endcap,muon_segment_station,muon_segment_ring,muon_segment_chamber)
                 if muonsegmentChamberID == chamberID_of_segment:
                     if muon_segment_localX == segment_LocalX:
                         if segment_LocalY == muon_segment_localY:
                             MuonIndex = m
        return  MuonIndex


#    def rechit_is_from_muon(self, tree, rechit):


    def link_rechits_to_segments(self, tree, list_of_segments):
        outlist = []
        for i in list_of_segments:
            outlist.append([i,self.allRechits_of_segment(tree, i)])
        return outlist    



                      
    def doAnalysis(self,file):
        global opt, args
  
        tfile = ROOT.TFile(file,"READ")
        print("   ==============!!!!!!!!!!!!!!!!!!!!!+===============   ")
        if not tfile:
            raise RunTimeError,"No input file specified or root file could not be found!"

        print "Opened file ", file
        
        if opt.isMC:
            tree = tfile.Get("cscRootMaker/Events")
        else:
            tree = tfile.Get("cscRootMaker/Events")

        if not tree:
            raise RunTimeError,"Tree not found!"




        #Analysis Loop
        for i in range( tree.GetEntries() ):
#            print('===============================    Event loop    ========================================= ')
            tree.GetEntry(i)

            if i%100 == 0:
                 print "Event ",i
            if self.totalEvents > opt.maxEvents:
                break
            self.totalEvents+=1
            recMuon_segments_rechits = []
            if opt.isLocalReco or opt.isFullReco:

                #Muons
                #AvgRH/Seg
                self.simHits_muonMatched[:]=[]
                self.recHits_muonMatched[:]=[]


#                self.sorted_hists1D['nSegmentsTotal'].Fill(tree.cscSegments_nSegments)

                MuonSegmentsRechitsList = []
                for n in range(tree.muons_nMuons):

                    if tree.muons_isStandAloneMuon[n] and len(self.allSegments_belonging_toMuon(tree, n) ) > 0:
#                        print("# muon ", n)
#                        print(" Muon n   ", n, "  has   ", self.allSegments_belonging_toMuon(tree,n)," segments  ")
#                        for k in self.allSegments_belonging_toMuon(tree,n):
#                            print("  Segment  #   ", k  , "  has    ", self.allRechits_of_segment(tree,k), "  rechits " ) # 

                        MuonSegmentsRechitsList.append([n, self.link_rechits_to_segments(tree, self.allSegments_belonging_toMuon(tree,n))])

                        segmentCounter = 0
                        recHitsCounter = 0
                        for m in range(len(tree.muons_cscSegmentRecord_nRecHits[n])):
                            self.hists1D['recHitsPerSegment_saMuon_Norm'].Fill(tree.muons_cscSegmentRecord_nRecHits[n][m])
                            segmentCounter += 1
                            recHitsCounter += tree.muons_cscSegmentRecord_nRecHits[n][m]

                        self.hists1D['segmentsPerSaMuon_Norm'].Fill(segmentCounter)
                        self.hists2D['recHitsVSp'].Fill(tree.muons_p[n],tree.muons_nRecHits[n])
                        self.hists2D['recHitsVSpT'].Fill(tree.muons_pt[n],tree.muons_nRecHits[n])
                        self.hists2D['recHitsVSEta'].Fill(tree.muons_eta[n],tree.muons_nRecHits[n])
                        avgRHpSeg = -1
                        if segmentCounter > 0:
                            avgRHpSeg = recHitsCounter/float(segmentCounter)
                        self.hists2D['recHitsPerSegVSp'].Fill(tree.muons_p[n],avgRHpSeg)
                        self.hists2D['recHitsPerSegVSpT'].Fill(tree.muons_pt[n],avgRHpSeg)
                        
                        rechits_segments_list = [[]]

#                if len(list_test)!=0: print("lllllllllllllll:   ", list_test[1])
                #CSCSegments
                CSC_SegmentCounter = [0] * 600
                CSC_SegmentMap = [''] * 600
                for n in range(tree.cscSegments_nSegments):
#                    print(" segment#   ", n, "   from muon# ",self.segment_is_from_muon(tree,n))
                    serialRecord = tree.cscSegments_ID_chamberSerial[n]
                    CSC_SegmentCounter[serialRecord] = CSC_SegmentCounter[serialRecord]+1
                    CSC_SegmentMap[serialRecord]+=str(n)+'.'
                    sRing = str(tree.cscSegments_ID_ring[n])
                    sStation = str(tree.cscSegments_ID_station[n])
                    sEndcap = '+'
                    if tree.cscSegments_ID_endcap[n] == 2:
                        sEndcap = '-'
                    string = 'ME'+sEndcap+sStation+'-'+sRing+'_recHitsPerSegment_Norm'
                    self.hists1D[string].Fill(tree.cscSegments_nRecHits[n])
                    self.hists1D['recHitsPerSegment_Norm'].Fill(tree.cscSegments_nRecHits[n])

                for n in range(0,600):
                    if CSC_SegmentCounter[n] == 1:
                        line = CSC_SegmentMap[n].split('.')
                        Identifier=int(line[0])
                        nLayers=0
                        missingLayers = []
                        for m in range(len(tree.cscSegments_recHitRecord_layer[Identifier])):
                            layer = tree.cscSegments_recHitRecord_layer[Identifier][m]
                            missingLayers.append(layer)
                            nLayers+=1
                        if nLayers > 0:
                            self.hists1D['OneSegmentChambers_nRecHitLayers_Norm'].Fill(nLayers)
                            #if not all 6 layers are reconstructed, plot missing layers
                            if nLayers < 6:
                                for j in range(len(missingLayers)):
                                    self.hists1D['OneSegmentChambers_missingLayer_Norm'].Fill(missingLayers[j])

                #2DRecHits
                for n in range(0,tree.recHits2D_nRecHits2D):

                    sEndcap = tree.recHits2D_ID_endcap[n]
                    if sEndcap == 2: sEndcap = '-'
                    else: sEndcap = '+'
                    sStation = str(tree.recHits2D_ID_station[n])
                    sChamber = str(tree.recHits2D_ID_chamber[n])
                    sLayer   = str(tree.recHits2D_ID_layer[n])
                    sRing    = str(tree.recHits2D_ID_ring[n])
                    #Average 2D per station
                    string   = 'ME' + sEndcap + sStation + '/' + sRing
                    self.nRecHitsPerStation[string] += 1
                    self.nRecHitsPerLayer[tree.recHits2D_ID_endcap[n]-1][tree.recHits2D_ID_station[n]-1][tree.recHits2D_ID_ring[n]-1][tree.recHits2D_ID_chamber[n]-1][tree.recHits2D_ID_layer[n]-1] += 1
                    #locations
                    x  = tree.recHits2D_localX[n]
                    y  = tree.recHits2D_localY[n]

                    gx = tree.recHits2D_globalX[n]
                    gy = tree.recHits2D_globalY[n]
                    
                    string = 'ME'+sEndcap+sStation+'_l'+sLayer+'_recHits2D'
                    self.hists2D[string].Fill(gx,gy)
                    string = 'ME'+sEndcap+sStation+'_recHits2D'
                    self.hists2D[string].Fill(gx,gy)


                #2DSimHits

                if opt.isMC:
                    MuonsFromZ = self.findMuonsFromZ(tree)
#                    print(' Event Number  ', float(tree.Event)/100)

                    for mu in MuonsFromZ:
                        MuLVGen = self.genMuonLV(tree, mu);

                        self.eff_denum_hists1D['MuonReconstruction_MuonPt_den'].Fill(MuLVGen.Pt())
                        self.eff_denum_hists1D['MuonReconstruction_MuonEta_den'].Fill(math.fabs(MuLVGen.Eta()))
                        recoMu = self.recoMuonMatchedIndex(tree,mu)
                        if( recoMu !=-1 ):
                            RMuLV = self.recMuonLV(tree, recoMu);
                            self.sorted_hists1D['MuonReconstruction_MuonPt'].Fill(MuLVGen.Pt())
                            self.sorted_hists1D['MuonReconstruction_MuonEta'].Fill( math.fabs(MuLVGen.Eta()))
                            self.sorted_hists1D['MuonReconstruction_PtResolution'].Fill(MuLVGen.Pt() - RMuLV.Pt())





                    GRMuonsMap = self.GenCSCRecoMuonsMap(tree)
#                    if len(GRMuonsMap)!=0:
#                        for pair in GRMuonsMap:                        
#                            recoMuIndex = pair[1]
#                            genMuIndex  = pair[0]
                    if True:
                        for mu in MuonsFromZ:                        


                            genMuIndex  = mu
                            recoMuIndex = self.recoMuonMatchedIndex(tree,mu)

#                            print("========================================================================= ", tree.Event)
#                            print("genMuon  genMuonindex ", tree.gen_muons_genindex[genMuIndex])
                            ########################################  to be rremoved it's all for debbuging

#                            print("  GEN and RECO Mu's LV")
                            if( recoMuIndex!=-1 ):
                                RMuLV = self.recMuonLV(tree, recoMuIndex);
                                self.sorted_hists1D["RecMuPt_Debug"].Fill(RMuLV.Pt() )
                            GMuLV = self.genMuonLV(tree, genMuIndex);

#                            RMuLV.Print();
#                            GMuLV.Print();
 


                            if recoMuIndex!=-1:
                                ChambersCrossedByMuon    = self.Chambers_crossedByMuon(tree, recoMuIndex)
                                AllRecHitOfTheMuon = self.allRecHits_belonging_toMuon(tree, recoMuIndex)
                                self.sorted_hists1D["nChambers_crossedByRecMuon"].Fill(len(ChambersCrossedByMuon) )

                            ChambersCrossedByGenMuon = self.Chambers_crossedByGenMuon(tree, genMuIndex)
                            AllSimHitOfTheMuon       = self.allSimHits_belonging_toGenMuon(tree, genMuIndex)
                            self.sorted_hists1D["nChambers_crossedByGenMuon"].Fill(len(ChambersCrossedByGenMuon) )

#                            print('----------- ')
#                            print(' Gen  chambers  ', ChambersCrossedByGenMuon)
#                            print(' Rec  chambers  ', ChambersCrossedByMuon)

                            
                            CleanSimChambers = []


#    parser.add_option('-me11','--ME11', dest='ME11', type='int', default=1 ,help='Include ME11 chambers: 0')
#    parser.add_option('-me12','--ME12', dest='ME12', type='int', default=1 ,help='Only over  ME12 chambers: 1')


#                            for good_chambers in ChambersCrossedByGenMuon:
                            for good_chambers in ChambersCrossedByGenMuon:

                                allSimHitsInChamber     = self.all_simhits_in_a_chamber(tree, good_chambers)
                                allMuonSimHitsInChamber = self.all_muon_simhits_in_a_chamber(tree, good_chambers, genMuIndex )
                                allRecHitsInChamber     = self.all_rechits_in_a_chamber(tree, good_chambers)
                                allSegmentsInChamber    = self.allSegments_InChamber(tree, good_chambers)
                                Chamber_station         = self.Chamber_station(good_chambers)
                                Chamber_ring            = self.Chamber_ring(good_chambers)

                                if(opt.ME11 == 0 and ( Chamber_station ==1 and Chamber_ring == 1) ): continue  # non ME11
                                if(opt.ME21 == 1 and (  Chamber_station !=2 or Chamber_ring != 1)  ): continue  # selecti either ME21 or all except ME11


#                                print(' nonME11  ', opt.ME11  , ' ME21 ', opt.ME21, ' good chamber  ' , good_chambers, 'station: ', Chamber_station, Chamber_ring, 'SimHits Here ', allSimHitsInChamber)
                                if(Chamber_station==1):
                                    self.sorted_hists1D['allSimHitsInStation_1'].Fill(len(allSimHitsInChamber) )
                                    if(Chamber_ring == 1):
                                        self.sorted_hists1D['allSimHitsInStation_ME11'].Fill(len(allSimHitsInChamber) )
                                    if(Chamber_ring == 2):
                                        self.sorted_hists1D['allSimHitsInStation_ME12'].Fill(len(allSimHitsInChamber) )
                                if(Chamber_station==2):
                                    self.sorted_hists1D['allSimHitsInStation_2'].Fill(len(allSimHitsInChamber) )


                                self.sorted_hists1D['allSimHitsInChamber'].Fill(len(allSimHitsInChamber) )
                                self.sorted_hists1D['allMuonSimHitsInChamber'].Fill(len(allMuonSimHitsInChamber) )
                                self.sorted_hists1D['allRecHitsInChamber'].Fill(len(allRecHitsInChamber) )
                                self.sorted_hists2D['SimHitsVsMuonSimHits'].Fill(len(allSimHitsInChamber),len(allMuonSimHitsInChamber) )
#                                self.sorted_hists2D['SimHitsVsRecHits'].Fill(len(allSimHitsInChamber), len(allRecHitsInChamber) )


                                for n in allSimHitsInChamber:
                                    Type = math.fabs(tree.simHits_particleType[n])
                                    if(math.fabs(tree.simHits_particleType[n]) == 211  ): Type = 5
                                    if(math.fabs(tree.simHits_particleType[n]) == 2212 ): Type = 7
                                    self.sorted_hists1D['SimHitsParticleType'].Fill(Type)

                                for n in allRecHitsInChamber:
                                    self.sorted_hists1D['RecHitSimHitParticleType'].Fill(tree.recHits2D_simHit_particleTypeID[n])

                                HitsSelection = True

                                
                                if(opt.condition == 0 ): HitsSelection = (len(allSimHitsInChamber) > 2)
                                if(opt.condition == 1 ): HitsSelection = (len(allMuonSimHitsInChamber) == len(allSimHitsInChamber))

#                                print('Selection ', Selection, ' opt.condition ', opt.condition, '  simhits ', len(allSimHitsInChamber),  ' muon sim hits ', len(allMuonSimHitsInChamber))
                                # Start the segment efficiency block                                     
                                if(  HitsSelection  ):  # all SimHits
#                                if( len(allMuonSimHitsInChamber) == len(allSimHitsInChamber) ):
#                                    print('passed ? ')

                                    self.sorted_hists1D['NSegmentsSelectedChamber'].Fill(len(allSegmentsInChamber))
                                    if(len(allSegmentsInChamber) == 0):
                                        self.sorted_hists1D['ZeroSegmentsAllSimHits'].Fill(len(allSimHitsInChamber))
                                        self.sorted_hists1D['ZeroSegmentsMuonSimHits'].Fill(len(allMuonSimHitsInChamber))
                                        self.sorted_hists1D['ZeroSegmentsRecHits'].Fill(len(allRecHitsInChamber))

                                    SimSegment = allMuonSimHitsInChamber
                                    MatchedSegmentAndPulls = self.FindSegmentMatchedToSim(tree, good_chambers, SimSegment)
                                    MatchedSegmentIndex = MatchedSegmentAndPulls[0]
                                    if  MatchedSegmentIndex!=-1:
                                        self.sorted_hists1D['SegmentMatchingPullX'].Fill(MatchedSegmentAndPulls[1])
                                        self.sorted_hists1D['SegmentMatchingPullY'].Fill(MatchedSegmentAndPulls[2])
                                        self.sorted_hists1D['SegmentMatchingdX'].Fill(MatchedSegmentAndPulls[3])
                                        self.sorted_hists1D['SegmentMatchingdY'].Fill(MatchedSegmentAndPulls[4])
#                                        print ("pulls X/Y  ", MatchedSegmentAndPulls[1], MatchedSegmentAndPulls[2])
#                                    print('Matched Segment Index  ', MatchedSegmentIndex)
                                    SimAndRecoMatched   = self.SimRecoSegmentMatching(tree, good_chambers, SimSegment, recoMuIndex)
                                    self.sorted_hists1D['AllSegmentsInMuonsChamber'].Fill(len(allSegmentsInChamber))
#                                    print(' SimAndRecoMatched  ', SimAndRecoMatched , '  event  ', int(tree.Event))

                                    if(not SimAndRecoMatched): 
                                        Duplicatates = self.DublicateLayersInRecoSegment(tree, good_chambers, SimSegment, recoMuIndex)
#                                        print("  Duplication??  ",  Duplicatates)
                                        self.sorted_hists1D['DuplicatedLayersInSegment'].Fill(int(Duplicatates))


                                    central_sim_hit = -1
                                    for sh in allMuonSimHitsInChamber:
                                        if tree.simHits_ID_layer[sh] == 3:
                                            central_sim_hit = sh


#                                    if(self.Chamber_station(good_chambers) !=1 and self.Chamber_ring(good_chambers) !=1 ):
                                    if( True ):

#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'].Fill(GMuLV.Pt())
#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'].Fill(math.fabs(GMuLV.Eta()))
#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_den'].Fill(GMuLV.Phi())

                                        self.eff_denum_hists1D['AnySegmentEfficiency_MuonPt_den'].Fill(GMuLV.Pt())
                                        self.eff_denum_hists1D['AnySegmentEfficiency_MuonEta_den'].Fill(math.fabs(GMuLV.Eta()))

                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1):

                                            self.eff_denum_hists1D['SegmentEfficiency_LocalX_den'].Fill(tree.simHits_localX[central_sim_hit])
                                            self.eff_denum_hists1D['SegmentEfficiency_LocalY_den'].Fill(tree.simHits_localY[central_sim_hit])

                                            self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_den'].Fill(tree.simHits_localX[central_sim_hit])
                                            self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_den'].Fill(tree.simHits_localY[central_sim_hit])

                                        if( len(allSegmentsInChamber) != 0):
                                            self.sorted_hists1D['AnySegmentEfficiency_MuonPt'].Fill(GMuLV.Pt())
                                            self.sorted_hists1D['AnySegmentEfficiency_MuonEta'].Fill(math.fabs(GMuLV.Eta()))


                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1 and MatchedSegmentIndex !=-1):
                                            self.sorted_hists1D['MatchedSegmentEfficiency_LocalX'].Fill(tree.simHits_localX[central_sim_hit])
                                            self.sorted_hists1D['MatchedSegmentEfficiency_LocalY'].Fill(tree.simHits_localY[central_sim_hit])



                                        SegmentIsRecoed = self.MuonHasRecoSegmentInTheChamber(tree, good_chambers, recoMuIndex,  allMuonSimHitsInChamber )
                                        if(SegmentIsRecoed!=-1):
#                                            self.sorted_hists1D['SegmentEfficiency_MuonPt'].Fill(GMuLV.Pt())
#                                            self.sorted_hists1D['SegmentEfficiency_MuonEta'].Fill(math.fabs(GMuLV.Eta()))
#                                            self.sorted_hists1D['SegmentEfficiency_MuonPhi'].Fill(GMuLV.Phi())
                                            ###  Hits Pull

                                            rechits_of_segment = self.allRechits_of_segment(tree, SegmentIsRecoed)

                                            RecHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;  3 - localErrXX; 4 - localErrYY
                                            SimHitMatrix=[] # 0 - layer; 1 - local X; 2 - local Y;
                                            for rc in rechits_of_segment:
                                                RecHitMatrix.append([ tree.recHits2D_ID_layer[rc], tree.recHits2D_localX[rc], tree.recHits2D_localY[rc], 
                                                                      tree.recHits2D_localXXerr[rc], tree.recHits2D_localYYerr[rc] ])
                                            for sh in SimSegment:
                                                SimHitMatrix.append([ tree.simHits_ID_layer[sh], tree.simHits_localX[sh], tree.simHits_localY[sh]])

                                            RecHitMatrix.sort(key=lambda element : element[0])
                                            SimHitMatrix.sort(key=lambda element : element[0])


                                            if( len(RecHitMatrix) == len(SimHitMatrix) ):
                                                for i in range(len(RecHitMatrix)):
                                                    self.sorted_hists1D['SimRecHits_PullX_allLayers'].Fill( (SimHitMatrix[i][1] - RecHitMatrix[i][1])/sqrt(RecHitMatrix[i][3]) )
                                                    self.sorted_hists1D['SimRecHits_PullY_allLayers'].Fill( (SimHitMatrix[i][2] - RecHitMatrix[i][2])/sqrt(RecHitMatrix[i][4]) )



                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1 and SimAndRecoMatched):
                                            self.sorted_hists1D['SegmentEfficiency_LocalX'].Fill(tree.simHits_localX[central_sim_hit])
                                            self.sorted_hists1D['SegmentEfficiency_LocalY'].Fill(tree.simHits_localY[central_sim_hit])





                                            ############################# Comment out ME11                                        
#                                    if(self.Chamber_station(good_chambers)==1 and self.Chamber_ring(good_chambers)==1):

#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonPt_ME11_den'].Fill(GMuLV.Pt())
#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonEta_ME11_den'].Fill(math.fabs(GMuLV.Eta()))
#                                        self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_ME11_den'].Fill(GMuLV.Phi())

#                                        self.eff_denum_hists1D['AnySegmentEfficiency_MuonPt_ME11_den'].Fill(GMuLV.Pt())
#                                        self.eff_denum_hists1D['AnySegmentEfficiency_MuonEta_ME11_den'].Fill(math.fabs(GMuLV.Eta()))


#                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1):
#                                            self.eff_denum_hists1D['SegmentEfficiency_LocalX_ME11_den'].Fill(tree.simHits_localX[central_sim_hit])
#                                            self.eff_denum_hists1D['SegmentEfficiency_LocalY_ME11_den'].Fill(tree.simHits_localY[central_sim_hit])

#                                            self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_ME11_den'].Fill(tree.simHits_localX[central_sim_hit])
#                                            self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_ME11_den'].Fill(tree.simHits_localY[central_sim_hit])

#                                        if(len(allSegmentsInChamber) != 0):
#                                            self.sorted_hists1D['AnySegmentEfficiency_MuonPt_ME11'].Fill(GMuLV.Pt())
#                                            self.sorted_hists1D['AnySegmentEfficiency_MuonEta_ME11'].Fill(math.fabs(GMuLV.Eta()))


#                                        SegmentIsRecoed = self.MuonHasRecoSegmentInTheChamber(tree, good_chambers, recoMuIndex,  allMuonSimHitsInChamber )

#                                        if(SegmentIsRecoed!=-1):
#                                            self.sorted_hists1D['SegmentEfficiency_MuonPt_ME11'].Fill(GMuLV.Pt())
#                                            self.sorted_hists1D['SegmentEfficiency_MuonEta_ME11'].Fill(math.fabs(GMuLV.Eta()))
#                                            self.sorted_hists1D['SegmentEfficiency_MuonPhi_ME11'].Fill(GMuLV.Phi())


#                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1 and SimAndRecoMatched):
#                                            self.sorted_hists1D['SegmentEfficiency_LocalX_ME11'].Fill(tree.simHits_localX[central_sim_hit])
#                                            self.sorted_hists1D['SegmentEfficiency_LocalY_ME11'].Fill(tree.simHits_localY[central_sim_hit])

#                                        if( len(allMuonSimHitsInChamber) == 6 and central_sim_hit != -1 and MatchedSegmentIndex != -1):
#                                            self.sorted_hists1D['MatchedSegmentEfficiency_LocalX_ME11'].Fill(tree.simHits_localX[central_sim_hit])
#                                            self.sorted_hists1D['MatchedSegmentEfficiency_LocalY_ME11'].Fill(tree.simHits_localY[central_sim_hit])
                                        ############################# Comment out ME11                                        



                                # End   the segment efficiency block                                     



#                                if(len(allMuonSimHitsInChamber) == 6  and len(allRecHitsInChamber) > 3 and len(allRecHitsInChamber) <=10 and self.Chamber_station(good_chambers)!=1 and self.Chamber_ring(good_chambers)!=1):
                                if(True):

#                                if(allSimHitsInChamber == allMuonSimHitsInChamber and len(allMuonSimHitsInChamber) == 6   
#                                   and len(allRecHitsInChamber) == 6  and self.Chamber_station(good_chambers)!=1 and self.Chamber_ring(good_chambers)!=1):

#                                if(self.Chamber_station(good_chambers)!=1):
                                
                                    CleanSimChambers.append(good_chambers)
                                    for sh in allSimHitsInChamber:
#                                        print( self.ChamberID(tree.simHits_ID_endcap[sh],tree.simHits_ID_station[sh],tree.simHits_ID_ring[sh], tree.simHits_ID_chamber[sh]), 
#                                        ' layer  ', tree.simHits_ID_layer[sh], ' x-y  ', tree.simHits_localX[sh], ' - ', tree.simHits_localY[sh])
                                        self.sorted_hists1D["SimHitsLocalX_Debug"].Fill(tree.simHits_localX[sh] )
                                        self.sorted_hists1D["SimHitsLocalY_Debug"].Fill(tree.simHits_localY[sh] )
#                                        print('Sh ', sh  , '  Layer  ', tree.simHits_ID_layer[sh] ,"SimHit THeta ", tree.simHits_theta[sh], '  SimHit Phi   ', tree.simHits_phi[sh] )
#                                    print("all rechits :   ", AllRecHitOfTheMuon)
                                    ChambersWithRecoMuon = []
#                                    for rh in AllRecHitOfTheMuon:
                                    for rh in  allRecHitsInChamber:
                                        rhchamber = self.ChamberID(tree.recHits2D_ID_endcap[rh],tree.recHits2D_ID_station[rh],tree.recHits2D_ID_ring[rh], tree.recHits2D_ID_chamber[rh])
                                        ChambersWithRecoMuon.append(rhchamber)

                                        self.sorted_hists1D['RecHitsLocalX_nonSegment'].Fill(tree.recHits2D_localX[rh] )
                                        self.sorted_hists1D['RecHitsLocalY_nonSegment'].Fill(tree.recHits2D_localY[rh] )
                                        self.sorted_hists1D['RecHitsPerLayer_nonSEgment'].Fill(tree.recHits2D_ID_layer[rh])


                            DifferenceMuonSimRecHits = len(AllSimHitOfTheMuon) - len(AllRecHitOfTheMuon)
                            AllSegmentsOfSelectedMuon =  self.allSegments_belonging_toMuon(tree, recoMuIndex)
                            HitsSelection = True

                            if(opt.condition == 0 ): HitsSelection = (len(allSimHitsInChamber) > 2)
                            if(opt.condition == 1 ): HitsSelection = (len(allMuonSimHitsInChamber) == len(allSimHitsInChamber))
                            if ( HitsSelection ):
                             for chamber in CleanSimChambers:  # Loop over chambers where AllSimHits == AllMuonSimHIts (there are no other SimHits than produced by muon)
 #                               NSegments = self.allSegments_InChamber(tree, chamber)
                                NRecHits  = self.all_rechits_in_a_chamber(tree, chamber)
#                                self.sorted_hists1D['NSegmentsSelectedChamber'].Fill(len(NSegments))
                                if(self.Chamber_station(chamber)==1 and self.Chamber_ring(chamber)==1):
                                    self.sorted_hists1D['NSegmentsSelectedChamber_ME11'].Fill(len(allSegmentsInChamber))
                                self.sorted_hists1D['NRecHitsCleanChamber'].Fill(len(NRecHits))
#                                print('  How many segmentss  ', NSegments, )

                                for s in  allSegmentsInChamber:
                                    NRecHitsOfSegment = self.allRechits_of_segment(tree,s)
#                                    if len(NRecHitsOfSegment)!=6: continue
                                    if(tree.cscSegments_nDOF[s]!=0):
                                        self.sorted_hists1D['RecoSegmentChi2ndof'].Fill(tree.cscSegments_chi2[s]/tree.cscSegments_nDOF[s])
                                    self.sorted_hists1D['RecoSegmentNRH'].Fill(tree.cscSegments_nRecHits[s] )
                                    self.sorted_hists1D['RecoSegmentLocalTheta'].Fill(tree.cscSegments_localTheta[s] )
                                    self.sorted_hists1D['RecoSegmentLocalPhi'].Fill(tree.cscSegments_localPhi[s] )
                                    self.sorted_hists1D['RecoSegmentLocalX'].Fill(tree.cscSegments_localX[s] )
                                    self.sorted_hists1D['RecoSegmentLocalY'].Fill(tree.cscSegments_localY[s] )
                                    if(self.Chamber_station(chamber)==1 and self.Chamber_ring(chamber)==1):
                                        self.sorted_hists1D['RecoSegmentNRH_ME11'].Fill(tree.cscSegments_nRecHits[s] )
                                        self.sorted_hists1D['RecoSegmentLocalTheta_ME11'].Fill(tree.cscSegments_localTheta[s] )
                                        self.sorted_hists1D['RecoSegmentLocalPhi_ME11'].Fill(tree.cscSegments_localPhi[s] )
                                        self.sorted_hists1D['RecoSegmentLocalX_ME11'].Fill(tree.cscSegments_localX[s] )
                                        self.sorted_hists1D['RecoSegmentLocalY_ME11'].Fill(tree.cscSegments_localY[s] )

                                    for rh in NRecHitsOfSegment:

                                        self.sorted_hists1D['RecHitsLocalX'].Fill(tree.recHits2D_localX[rh] )
                                        self.sorted_hists1D['RecHitsLocalY'].Fill(tree.recHits2D_localY[rh] )
                                        self.sorted_hists1D['RHSegementDeltaLocalX'].Fill(tree.recHits2D_localX[rh] - tree.cscSegments_localX[s] )
                                        self.sorted_hists1D['RHSegementDeltaLocalY'].Fill(tree.recHits2D_localY[rh] - tree.cscSegments_localY[s] )
                                        self.sorted_hists1D['RecHitsPerLayer'].Fill(tree.recHits2D_ID_layer[rh] )
                                        if(self.Chamber_station(chamber)==1 and self.Chamber_ring(chamber)==1):
                                            self.sorted_hists1D['RecHitsLocalX_ME11'].Fill(tree.recHits2D_localX[rh] )
                                            self.sorted_hists1D['RecHitsLocalY_ME11'].Fill(tree.recHits2D_localY[rh] )
                                            self.sorted_hists1D['RHSegementDeltaLocalX_ME11'].Fill(tree.recHits2D_localX[rh] - tree.cscSegments_localX[s] )
                                            self.sorted_hists1D['RHSegementDeltaLocalY_ME11'].Fill(tree.recHits2D_localY[rh] - tree.cscSegments_localY[s] )
                                            self.sorted_hists1D['RecHitsPerLayer_ME11'].Fill(tree.recHits2D_ID_layer[rh] )

                                        central_sim_hit = -1
                                        allMuonSimHitsInChamber = self.all_muon_simhits_in_a_chamber(tree, chamber, genMuIndex )
                                        for sh in self.MuonSimSegment(tree, allMuonSimHitsInChamber, s):
                                            if tree.simHits_ID_layer[sh] == 3:
                                                central_sim_hit = sh
                                                if(central_sim_hit!=-1):

                                                    self.sorted_hists1D['DeltaThetaRecoSimSegment'].Fill(tree.cscSegments_localTheta[s] - tree.simHits_theta[central_sim_hit])
                                                    self.sorted_hists1D['DeltaPhiRecoSimSegment'].Fill(tree.cscSegments_localPhi[s]     - tree.simHits_phi[central_sim_hit])
                                                    self.sorted_hists1D['DeltaXRecoSimSegment'].Fill(tree.cscSegments_localX[s]         - tree.simHits_localX[central_sim_hit])
                                                    self.sorted_hists1D['DeltaYRecoSimSegment'].Fill(tree.cscSegments_localY[s]         - tree.simHits_localY[central_sim_hit])
                                                    if(self.Chamber_station(chamber) == 1 and self.Chamber_ring(chamber) == 1):
                                                        self.sorted_hists1D['DeltaThetaRecoSimSegment_ME11'].Fill(tree.cscSegments_localTheta[s] - tree.simHits_theta[central_sim_hit])
                                                        self.sorted_hists1D['DeltaPhiRecoSimSegment_ME11'].Fill(tree.cscSegments_localPhi[s]     - tree.simHits_phi[central_sim_hit])
                                                        self.sorted_hists1D['DeltaXRecoSimSegment_ME11'].Fill(tree.cscSegments_localX[s]         - tree.simHits_localX[central_sim_hit])
                                                        self.sorted_hists1D['DeltaYRecoSimSegment_ME11'].Fill(tree.cscSegments_localY[s]         - tree.simHits_localY[central_sim_hit])





#                            print(" Diiference SimHits - RecHIts (I expect always positive  )", DifferenceMuonSimRecHits)
#                            self.sorted_hists1D['SimRecHitsDifference'].Fill(DifferenceMuonSimRecHits)

#                            print("========================================================================= ")
########################################  to be rremoved




#Chambers_crossedByMuon
#    def allSegments_InChamber(self,tree,chamber):


##########################################################

#                            print("  Compare indexes   ",genMuIndex, tree.gen_muons_genindex[pair[]])


#                            self.sorted_hists1D["nMuonsSegments_sorted"].Fill(len(AllSegmentsOfSelectedMuon))

#                            print(' Event Info==>  Event', int(tree.Event), ' mupT ', self.recMuonLV(tree,recoMuIndex).Pt()  , ' all Segs:  ', self.allSegments_belonging_toMuon(tree, recoMuIndex)#,  
#                                  '  all chambers  ', ChambersCrossedByMuon, ' Segs in 1st chamber', self.allSegments_InChamber(tree, ChambersCrossedByMuon[0]) )
#                            print("chambers:  ", self.Chambers_crossedByMuon(tree, recoMuIndex))
#                            for chamber in ChambersCrossedByMuon:
#                                allSegmentsInAGivenChamber = self.allSegments_InChamber(tree, chamber)
#                                self.sorted_hists1D["nSegmentsInMuonCrossedChamber"].Fill(len(allSegmentsInAGivenChamber))
#                                self.sorted_hists1D["allSegments_inChamber_NOT_belonging_toMuon"].Fill(len(self.allSegments_inChamber_NOT_belonging_toMuon(tree,chamber, recoMuIndex)))


 #                               print("segments  in chamber ", self.allSegments_InChamber(tree, chamber))
 #                               for seg in self.allSegments_InChamber(tree, chamber):
 #                                   print("this segment is from a muon ", self.segment_is_from_muon(tree,seg) )

#                            AllSegmentsOfSelectedMuon =  self.allSegments_belonging_toMuon(tree, recoMuIndex) 
#                            print('----------')
#                            for s in AllSegmentsOfSelectedMuon:
#                                self.sorted_hists1D["nRecHitsPerMuonSegments_sorted"].Fill(len(self.allRechits_of_segment(tree,s)))

#                            if len(AllSegmentsOfSelectedMuon) ==1:
#                                self.sorted_hists1D["MuonSegmentLocalX_sorted"].Fill(tree.cscSegments_localX[s])
#                                self.sorted_hists1D["MuonSegmentLocalY_sorted"].Fill(tree.cscSegments_localY[s])
#                                print("this segment is from a muon ", self.segment_is_from_muon(tree,s), '  reco muon is: ',recoMuIndex )

                #2DSimHits
                if opt.isMC:

                    selectedGenMuons=[]
#                    print(" \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ")
 #                   print(" \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ")
                    for im in range(0, tree.gen_muons_nMuons):
                        muon = self.genMuonLV(tree,im)
#                        muon.Print()
                        if muon.Pt()> 3 and math.fabs(muon.Eta()) > 1.1 and math.fabs(muon.Eta()) < 2.4:
                            selectedGenMuons.append(im)
                        recoMuIndex = self.recoMuonMatchedIndex(tree,im) 
                        if recoMuIndex!= -1: recoMuon = self.recMuonLV(tree,recoMuIndex)


                    GRMuonsMap = self.GenCSCRecoMuonsMap(tree)

                    AllSimHitOfTheMuon = []
                    AllRecHitOfTheMuon = []

                    for pair in GRMuonsMap:
                        recoMuIndex = pair[1]
                        genMuIndex  = pair[0]

#                        print("recoMu index  ", recoMuIndex,genMuIndex)
                        AllSimHitOfTheMuon = self.allSimHits_belonging_toGenMuon(tree, pair[0])
                        AllRecHitOfTheMuon = self.allRecHits_belonging_toMuon(tree, pair[1])

                    selected_hits=[] 
                    for n in AllSimHitOfTheMuon:
#                    for n in range(0,tree.simHits_nSimHits):
                        sEndcap = tree.simHits_ID_endcap[n]
                        if sEndcap == 2: sEndcap = '-'
                        else: sEndcap = '+'
                        sStation = str(tree.simHits_ID_station[n])
                        sChamber = str(tree.simHits_ID_chamber[n])
                        sLayer   = str(tree.simHits_ID_layer[n])
                        sRing    = str(tree.simHits_ID_ring[n])
                        chamberID = tree.simHits_ID_endcap[n]*10000 + tree.simHits_ID_station[n]*1000  + tree.simHits_ID_ring[n]*100  + tree.simHits_ID_chamber[n]

                        x  = tree.simHits_localX[n]
                        y  = tree.simHits_localY[n]
                        gx = tree.simHits_globalX[n]
                        gy = tree.simHits_globalY[n]
                        
                        string = 'ME'+sEndcap+sStation+'_l'+sLayer+'_simHits2D'
                        self.hists2D[string].Fill(gx,gy)
                        string = 'ME'+sEndcap+sStation+'_simHits2D'
                        self.hists2D[string].Fill(gx,gy)

                        isMuonHit=True
                        for m in selectedGenMuons:
                            if self.simHitBelongToGenMuon(tree, n, m) and self.recoMuonMatchedIndex(tree, m): 
                                isMuonHit = True
#                        print(" #hit   isMuonHit  ", n, isMuonHit)
#                        if abs(tree.simHits_particleType[n]) == 13:
#                        print(">>>>>>>>>", isMuonHit, tree.simHits_particleType[n])
                        if abs(tree.simHits_particleType[n]) == 13:# and isMuonHit:   # make efficiency plots 
#                            print("<<<<<<<<")
                            shChamberSerial = tree.simHits_ID_chamberSerial[n]
                            shLayer         = tree.simHits_ID_layer[n]
                            shChamber       = tree.simHits_ID_chamber[n]
                            shRing          = tree.simHits_ID_ring[n]
                            shStation       = tree.simHits_ID_station[n]
                            shEndcap        = tree.simHits_ID_endcap[n]

                              
                            self.simHitsOverallEffDen += 1
                            self.simHitsEffDen[shChamberSerial] += 1
                            self.simHitsLayerEffDen[shChamberSerial][shLayer-1] += 1
                            self.simHitsChamberEffDen[shEndcap-1][shStation-1][shRing-1][shChamber-1][shLayer-1] += 1

                            self.simHits_muonMatched.append(n)
                            #SimHit Reco Efficiency
#
                            for m in AllRecHitOfTheMuon:
#                            for m in range(0,tree.recHits2D_nRecHits2D):
#                                print(">>>>>>>>>>>>>>>> ", isMuonHit, tree.recHits2D_simHit_particleTypeID[m])

 #                               if abs(tree.recHits2D_simHit_particleTypeID[m]) == 13:
#                                    self.sorted_hists1D['recHits_simHits_particleType'].Fill( tree.recHits2D_simHit_particleTypeID[m] )
                                    if tree.recHits2D_ID_chamberSerial[m] != shChamberSerial: continue
                                    if tree.recHits2D_ID_layer[m] != shLayer: continue
                                    xLow  = tree.recHits2D_localX[m] - 2*sqrt(tree.recHits2D_localXXerr[m])
                                    xHigh = tree.recHits2D_localX[m] + 2*sqrt(tree.recHits2D_localXXerr[m])
                                    yLow  = tree.recHits2D_localY[m] - 2*sqrt(tree.recHits2D_localYYerr[m])
                                    yHigh = tree.recHits2D_localY[m] + 2*sqrt(tree.recHits2D_localYYerr[m])

#                                    if (x < xLow or x > xHigh) and (y < yLow or y > yHigh): continue

                                    self.simHitsOverallEffNum += 1
                                    self.simHitsEffNum[shChamberSerial] += 1
                                    self.simHitsLayerEffNum[shChamberSerial][shLayer-1] += 1
                                    self.simHitsChamberEffNum[shEndcap-1][shStation-1][shRing-1][shChamber-1][shLayer-1] += 1

                                    self.recHits_muonMatched.append(m)
                                    break

                    self.hists1D['DeltaSimRecHits'].Fill( len(self.simHits_muonMatched) - len(self.recHits_muonMatched) )



                        
            if opt.isDigi and (opt.isLocalReco or opt.isFullReco):
                #ACLT/CLTC
                alctCounter = [0] * 600
                clctCounter = [0] * 600
                lctCounter  = [0] * 600
                for i in range(tree.alct_nAlcts):
                    alctCounter[tree.alct_ID_chamberSerial[i]] +=1
                for j in range(tree.clct_nClcts):
                    clctCounter[tree.clct_ID_chamberSerial[j]] +=1
                for jj in range(tree.correlatedLct_nLcts):
                    lctCounter[tree.correlatedLct_ID_chamberSerial[jj]] +=1
                
                for k in range(len(alctCounter)):
                    if alctCounter[k] == 2 and clctCounter[k] == 2:
                        self.hists1D['FourLctChambers_nSegments_Norm'].Fill(CSC_SegmentCounter[k])
                        self.hists1D['FourLctChambers_nCorrelLcts_Norm'].Fill(lctCounter[k])


            for ec in range(0,2):
                for st in range(0,4):
                    for rg in range(0,4):
                        if st+1 > 1 and rg+1 > 2: continue
                        for ch in range(0,36):
                            if st+1 > 1 and rg+1 == 1 and ch+1 > 18: continue
                            for lr in range(0,6):
#                                print '  EC  ', ec,'  st:  ', st ,' rg:  ', rg, ' ch:  ', ch,'  layer:  ',lr, '   nRecHits:  ',self.nRecHitsPerLayer[ec][st][rg][ch][lr] 
                                string = 'nrecHitsPerLayer_allChambers'
                                self.hists1D[string].Fill(self.nRecHitsPerLayer[ec][st][rg][ch][lr])








    def defineHistos(self):

        EC = ['+','-']
        ST = [1,2,3,4]
        RG = [1,2,3,4]
        LR = [1,2,3,4,5,6]


        #CSC Segments
        self.hists1D['OneSegmentChambers_nRecHitLayers_Norm'] = ROOT.TH1F("1SegmentChambers_nLayers","; N Layers; Fraction of Events", 9,-0.5,8.5) 
        self.hists1D['OneSegmentChambers_missingLayer_Norm'] = ROOT.TH1F("1SegmentChambers_missingLayer","; Missing Layer(s); Fraction of Events", 9,-0.5,8.5) 

        #LCTs
        self.hists1D['FourLctChambers_nSegments_Norm'] = ROOT.TH1F("4LctChambers_nSegments","; N Segments; Fractions of Events", 8,-0.5,7.5) 
        self.hists1D['FourLctChambers_nCorrelLcts_Norm'] = ROOT.TH1F("4LctChambers_nCorrelLcts","; N Correlated LCTs; Fractions of Events", 8,-0.5,7.5)

        #SimHits
        self.hists1D['simHitsRecoEfficiency']    = ROOT.TH1F("simHitsRecoEfficiency", ";    Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l1'] = ROOT.TH1F("simHitsRecoEfficiency_l1", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l2'] = ROOT.TH1F("simHitsRecoEfficiency_l2", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l3'] = ROOT.TH1F("simHitsRecoEfficiency_l3", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l4'] = ROOT.TH1F("simHitsRecoEfficiency_l4", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l5'] = ROOT.TH1F("simHitsRecoEfficiency_l5", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)
        self.hists1D['simHitsRecoEfficiency_l6'] = ROOT.TH1F("simHitsRecoEfficiency_l6", "; Chamber Serial; RECO Efficiency for Muons", 700, 0, 700)

        #Segments
        self.hists1D['segmentsPerSaMuon_Norm'] = ROOT.TH1F("segmentsPerSaMuon", "; Segments Per Muon; Fraction of SAMuons", 10, -0.5, 9.5)
        
        #Average recHits2D
        self.hists1D['avgRecHits2D'] = ROOT.TH1F("avgRecHits2D", "; Station; Average Rec Hits Per Chamber Per Event", 23,0,23)
        self.hists1D['avgRecHits2D'].SetStats(0)
        self.hists1D['avgRecHits2D'].GetYaxis().SetTitleOffset(1.45)
        for i in range(1,21):
            self.hists1D['avgRecHits2D'].GetXaxis().SetBinLabel(i,self.stationRings[i-1])
        self.hists1D['avgRecHits2D'].GetXaxis().LabelsOption("v")

        self.hists1D['recHitsPerSegment_saMuon_Norm'] = ROOT.TH1F("recHitsPerSegment_saMuon", "; RecHits Per Segment; Fraction of SAMuons", 8,-0.5,7.5)

        self.hists2D['recHitsVSp']        = ROOT.TH2F("recHitsVSp","; P (GeV); N RecHits",1000, 0, 800, 100, 0, 60)
        self.hists2D['recHitsVSpT']       = ROOT.TH2F("recHitsVSpT","; pT (GeV); N RecHits",1000, 0, 800, 100, 0, 60)
        self.hists2D['recHitsVSEta']      = ROOT.TH2F("recHitsVSEta","; eta; N RecHits",1000, -2.5, 2.5, 100, 0, 60)
        self.hists2D['recHitsPerSegVSp']  = ROOT.TH2F("recHitsPerSegVSp","; P (GeV); N RecHits/Segment", 1000, 0, 800, 8, 0, 8)
        self.hists2D['recHitsPerSegVSpT'] = ROOT.TH2F("recHitsPerSegVSpT","; pT (GeV); N RecHits/Segment", 1000, 0, 800, 8, 0, 8)



        #Segment Layers
        self.hists1D['recHitsPerSegment_Norm'] = ROOT.TH1F("recHitsPerSegment", "; N RecHits; Fraction of Segments", 6, 1.5, 7.5)





        #SimHit Efficiencies
        for i in range(len(EC)):
            for j in range(len(ST)):
                string = 'ME'+str(EC[i])+str(ST[j])
                string1 = string+'_recHits2D'
                self.hists2D[string1] = ROOT.TH2F(string1,"; X; Y", 1600, -800, 800, 1600, -800, 800)
                string2 = string+'_simHits2D'
                self.hists2D[string2] = ROOT.TH2F(string2,"; X; Y", 1600, -800, 800, 1600, -800, 800)
                for k in range(len(RG)):
                    if ST[j] > 1 and RG[k] > 2: continue
                    string3 = string+'-'+str(RG[k])+'_simHitEfficiency'
                    self.hists1D[string3] = ROOT.TH1F(string3,"; Chamber; RECO Efficiency for Muons",40,0,40)
                    string4 = string+'-'+str(RG[k])+'_recHitsPerSegment'
                    self.hists1D[string4+'_Norm'] = ROOT.TH1F(string4+"_recHitsPerSegment", "; N RecHits; Fraction of Segments", 6, 1.5, 7.5)

                for m in range(len(LR)):
                    string = 'ME'+str(EC[i])+str(ST[j])+'_l'+str(LR[m])
                    string1 = string+'_recHits2D'
                    self.hists2D[string1] = ROOT.TH2F(string1,";  X; Y", 1600, -800, 800, 1600, -800, 800)
                    string2 = string+'_simHits2D'
                    self.hists2D[string2] = ROOT.TH2F(string2,";  X; Y", 1600, -800, 800, 1600, -800, 800)
                    for k in range(len(RG)):
                        if ST[j] > 1 and RG[k] > 2: continue
                        string = 'ME'+str(EC[i])+str(ST[j])+'-'+str(RG[k])+'_l'+str(LR[m])
                        string3 = string+'_simHitEfficiency'
                        self.hists1D[string3] = ROOT.TH1F(string3,"; Chamber; RECO Efficiency for Muons",40,0,40)
        # Per Event
        self.hists1D['DeltaSimRecHits']              = ROOT.TH1F("DeltaSimRecHits","; N(sHits) - N(rHits) (gen muon matched)",10, -2.5, 7.5)
        self.hists1D['nrecHitsPerLayer_allChambers'] = ROOT.TH1F("nrecHitsPerLayer_allChambers", "; N RecHits per Layer", 11, -0.5, 10.5)



#        self.sorted_hists1D['nSegments_sorted'] = ROOT.TH1F("nSegments_sorted", "; N Segments (all CSC's) )", 35, -0.5, 34.5)
#        self.sorted_hists1D['nMuonsSegments_sorted'] = ROOT.TH1F("nMuonsSegments_sorted", "; N segments of selected #mu ", 7, -0.5, 6.5)
#        self.sorted_hists1D['nRecHitsPerMuonSegments_sorted'] = ROOT.TH1F("nRecHitsPerMuonSegments_sorted", "; N rechits per #mu segment ", 11, -0.5, 10.5)
#        self.sorted_hists1D['recHits_simHits_particleType'] = ROOT.TH1F("recHits_simHits_particleType", "; simHit type MATCHED to muon RecHit ", 15, -1.5, 13.5)
#        self.sorted_hists1D["allSegments_inChamber_NOT_belonging_toMuon"] = ROOT.TH1F("allSegments_inChamber_NOT_belonging_toMuon", "; N segments in chamber NOT from #mu ", 4, -0.5, 3.5)

        self.sorted_hists1D['nChambers_crossedByGenMuon'] = ROOT.TH1F("nChambers_crossedByGenMuon", "; N chambers crossed by gen #mu (simhits)", 11, -0.5, 10.5)
        self.sorted_hists1D['nChambers_crossedByRecMuon'] = ROOT.TH1F("nChambers_crossedByRecMuon", "; N chambers crossed by gen #mu (segment record)", 11, -0.5, 10.5)

#        self.sorted_hists1D['nSegmentsInMuonCrossedChamber'] = ROOT.TH1F("nSegmentsInMuonCrossedChamber", "; N segments in a chamber with muon ", 5, -0.5, 4.5) 
#        self.sorted_hists1D['nSegmentsTotal'] = ROOT.TH1F("nSegmentsTotal", "; N segments total  ", 35, -0.5, 34.5)


#        self.sorted_hists1D['MuonSegmentLocalX_sorted'] = ROOT.TH1F("MuonSegmentLocalX_sorted", "; muons segment locX ", 50, -150, 150) 
#        self.sorted_hists1D['MuonSegmentLocalY_sorted'] = ROOT.TH1F("MuonSegmentLocalY_sorted", "; muons segment locY ", 50, -150, 150) 


#        self.sorted_hists1D['SimRecHitsDifference']  = ROOT.TH1F("SimRecHitsDifference","; NSimHits - NRecHits", 14,-5.5, 8.5) 
        self.sorted_hists1D['NSegmentsSelectedChamber'] = ROOT.TH1F("NSegmentsSelectedChamber","; N Segments in selected chamber", 10, -0.5,9.5)
        self.sorted_hists1D['NSegmentsSelectedChamber_ME11'] = ROOT.TH1F("NSegmentsSelectedChamber_ME11","; N Segments in clean chamber (ME11)", 10, -0.5,9.5)
        self.sorted_hists1D['NRecHitsCleanChamber']  = ROOT.TH1F("NRecHitsCleanChamber","; N RecHits in clean chamber (AllSimhit = MuonSimhits)",10, -0.5,9.5 )
        self.sorted_hists1D["SimHitsLocalX_Debug"]   = ROOT.TH1F("SimHitsLocalX_Debug","; SimHitsLocalX, cm (debug)",50,-100,100)
        self.sorted_hists1D["SimHitsLocalY_Debug"]   = ROOT.TH1F("SimHitsLocalY_Debug","; SimHitsLocalY, cm (debug)",50,-200,200)
        self.sorted_hists1D["RecMuPt_Debug"]         = ROOT.TH1F("RecMuPt_Debug","; RecMuon PT, GeV (debug)",50,25,70)



        self.sorted_hists1D['DeltaThetaRecoSimSegment']  = ROOT.TH1F("DeltaThetaRecoSimSegment","; #Delta#theta (recoseg-simhit), rad", 60,-0.5, 0.5)
        self.sorted_hists1D['DeltaPhiRecoSimSegment']    = ROOT.TH1F("DeltaPhiRecoSimSegment","; #Delta#phi (recoseg-simhit), rad", 60,-0.1, 0.1)
        self.sorted_hists1D['DeltaXRecoSimSegment']      = ROOT.TH1F("DeltaXRecoSimSegment","; Local #Delta X (recosegment - simsegment), cm",60,-0.5,0.5)
        self.sorted_hists1D['DeltaYRecoSimSegment']      = ROOT.TH1F("DeltaYRecoSimSegment","; Local #Delta Y (recosegment - simsegment), cm",60,-0.5,0.5)


        self.sorted_hists1D['DeltaThetaRecoSimSegment_ME11']  = ROOT.TH1F("DeltaThetaRecoSimSegment_ME11","; #Delta#theta (recoseg-simhit), rad (ME11)", 60,-0.5, 0.5)
        self.sorted_hists1D['DeltaPhiRecoSimSegment_ME11']    = ROOT.TH1F("DeltaPhiRecoSimSegment_ME11","; #Delta#phi (recoseg-simhit), rad (ME11)", 60,-0.5, 0.5)
        self.sorted_hists1D['DeltaXRecoSimSegment_ME11']      = ROOT.TH1F("DeltaXRecoSimSegment_ME11","; Local #Delta X (recosegment - simsegment) (ME11), cm",60,-50,50)
        self.sorted_hists1D['DeltaYRecoSimSegment_ME11']      = ROOT.TH1F("DeltaYRecoSimSegment_ME11","; Local #Delta Y (recosegment - simsegment) (ME11), cm",60,-50,50)


#        self.sorted_hists1D['SegmentEfficiency_LocalPhi']   = ROOT.TH1F("SegmentEfficiency_LocalPhi","; Reco segment local #phi, rad ", 40, 1.2, 1.8)
#        self.sorted_hists1D['SegmentEfficiency_LocalPhi']   = ROOT.TH1F("SegmentEfficiency_LocalPhi","; Reco segment local #phi, rad ", 40, 1.2, 1.8)


        self.sorted_hists1D['RecoSegmentLocalTheta'] = ROOT.TH1F("RecoSegmentLocalTheta","; Reco segment local #theta, rad", 60,0, 0.5)
        self.sorted_hists1D['RecoSegmentLocalPhi']   = ROOT.TH1F("RecoSegmentLocalPhi","; Reco segment local #phi, rad ", 60,1, 2)
        self.sorted_hists1D['RecoSegmentLocalX']     = ROOT.TH1F("RecoSegmentLocalX","; Reco segment local X, cm", 50,-100, 100)
        self.sorted_hists1D['RecoSegmentLocalY']     = ROOT.TH1F("RecoSegmentLocalY","; Reco segment local Y, cm", 50,-200, 200)
        self.sorted_hists1D['RecoSegmentNRH']            = ROOT.TH1F('RecoSegmentNRH',"; N rechits (selected segment)", 10, -0.5, 9.5);

        self.sorted_hists1D['RecoSegmentLocalTheta_ME11'] = ROOT.TH1F("RecoSegmentLocalTheta_ME11","; Reco segment local #theta, rad (ME11)", 60,-3, 3)
        self.sorted_hists1D['RecoSegmentLocalPhi_ME11']   = ROOT.TH1F("RecoSegmentLocalPhi_ME11","; Reco segment local #phi, rad (ME11)", 60,1, 2)
        self.sorted_hists1D['RecoSegmentLocalX_ME11']     = ROOT.TH1F("RecoSegmentLocalX_ME11","; Reco segment local X, cm (ME11)", 50,-100, 100)
        self.sorted_hists1D['RecoSegmentLocalY_ME11']     = ROOT.TH1F("RecoSegmentLocalY_ME11","; Reco segment local Y, cm (ME11)" , 50,-200, 200)
        self.sorted_hists1D['RecoSegmentNRH_ME11']            = ROOT.TH1F('RecoSegmentNRH_ME11',"; N rechits (selected segment) (ME11)", 10, -0.5, 9.5);

        self.sorted_hists1D['RecHitsLocalX'] = ROOT.TH1F("RecHitsLocalX","; RecHit local X, cm", 50,-100, 100)
        self.sorted_hists1D['RecHitsLocalY'] = ROOT.TH1F("RecHitsLocalY","; RecHit local Y, cm", 50,-200, 200)

        self.sorted_hists1D['RecHitsLocalX_ME11'] = ROOT.TH1F("RecHitsLocalX_ME11","; RecHit local X, cm (ME11)", 50,-100, 100)
        self.sorted_hists1D['RecHitsLocalY_ME11'] = ROOT.TH1F("RecHitsLocalY_ME11","; RecHit local Y, cm (ME11)", 50,-200, 200)

        self.sorted_hists1D['RecHitsLocalX_nonSegment'] = ROOT.TH1F("RecHitsLocalX_nonSegment","; RecHit local X,(Not from segment record), cm", 50,-100, 100)
        self.sorted_hists1D['RecHitsLocalY_nonSegment'] = ROOT.TH1F("RecHitsLocalY_nonSegment","; RecHit local Y,(Not from segment record), cm", 50,-200, 200)
        self.sorted_hists1D['RecHitsPerLayer_nonSEgment'] = ROOT.TH1F("RecHitsPerLayer_nonSEgment","; RecHit per layer (Not from segment record) ", 8,-0.5,7.5)

        self.sorted_hists1D['RHSegementDeltaLocalX']     = ROOT.TH1F("RHSegementDeltaLocalX","; #Delta Local X(RH - Seg) cm", 50,-1, 1)
        self.sorted_hists1D['RHSegementDeltaLocalY']     = ROOT.TH1F("RHSegementDeltaLocalY","; #Delta Local Y(RH - Seg) cm", 50,-1, 1)
        self.sorted_hists1D['RHSegementDeltaLocalX_ME11']     = ROOT.TH1F("RHSegementDeltaLocalX_ME11","; #Delta Local X(RH - Seg) cm (ME11)", 50,-1, 1)
        self.sorted_hists1D['RHSegementDeltaLocalY_ME11']     = ROOT.TH1F("RHSegementDeltaLocalY_ME11","; #Delta Local Y(RH - Seg) cm (ME11)", 50,-1, 1)

        self.sorted_hists1D['RecHitsPerLayer']                = ROOT.TH1F("RecHitsPerLayer","; RecHit per layer (per selected segment) ", 8,-0.5,7.5)
        self.sorted_hists1D['RecHitsPerLayer_ME11']           = ROOT.TH1F("RecHitsPerLayer_ME11","; RecHit per layer (per selected segment) (ME11)", 8,-0.5,7.5)

        self.sorted_hists1D['RecoSegmentChi2ndof']       = ROOT.TH1F('RecoSegmentChi2ndof',"; segment #chi^2/ndof", 50, 0, 5);


        self.sorted_hists1D['allSimHitsInChamber']       = ROOT.TH1F('allSimHitsInChamber',"; N SimHits in chamber", 20, 0.5, 20.5);
        self.sorted_hists1D['allSimHitsInStation_1']        = ROOT.TH1F('allSimHitsInStation_1',"; N SimHits in station 1", 20, 0.5, 20.5);
        self.sorted_hists1D['allSimHitsInStation_ME11'] = ROOT.TH1F('allSimHitsInStation_ME11',"; N SimHits in station ME11", 20, 0.5, 20.5);
        self.sorted_hists1D['allSimHitsInStation_ME12'] = ROOT.TH1F('allSimHitsInStation_ME12',"; N SimHits in station ME12", 20, 0.5, 20.5);
        self.sorted_hists1D['allSimHitsInStation_2']        = ROOT.TH1F('allSimHitsInStation_2',"; N SimHits in station 2", 20, 0.5, 20.5);


        self.sorted_hists1D['allMuonSimHitsInChamber']   = ROOT.TH1F('allMuonSimHitsInChamber',"; N #mu SimHits in chamber", 20, 0.5, 20.5);
        self.sorted_hists1D['allRecHitsInChamber']       = ROOT.TH1F('allRecHitsInChamber',"; N RecHits in chamber", 20, 0.5, 20.5);
        self.sorted_hists1D['AllSegmentsInMuonsChamber'] = ROOT.TH1F('AllSegmentsInMuonsChamber',"; N Segments in selected chambers",10, -0.5, 9.5)


        self.sorted_hists2D['SimHitsVsMuonSimHits']    = ROOT.TH2F("SimHitsVsMuonSimHits","; N SimHits; N Muon SimHits", 20, 0.5, 20.5, 20, 0, 20.5)
#        self.sorted_hists2D['SimHitsVsRecHits']        = ROOT.TH2F("SimHitsVsRecHits","; N SimHits; N RecHits", 20, 0.5, 20.5, 20, 0, 20.5)

        self.sorted_hists1D['SimHitsParticleType']     = ROOT.TH1F("SimHitsParticleType", "; SimHit type ", 17, -1.5, 15.5) 
        self.sorted_hists1D['RecHitSimHitParticleType']= ROOT.TH1F("RecHitSimHitParticleType", "; SimHit type matched  to the RecHit ", 17, -1.5, 15.5)

        self.sorted_hists1D['DuplicatedLayersInSegment'] = ROOT.TH1F("DuplicatedLayersInSegment", "; Not matched (rec hits duplication in layers) ", 2, -0.5, 1.5)

        # Efficiency
        # Muon Reco
        self.eff_denum_hists1D['MuonReconstruction_MuonPt_den']= ROOT.TH1F("MuonReconstruction_MuonPt_den","; pT (gen #mu), GeV ",30,25,70)
        self.sorted_hists1D['MuonReconstruction_MuonPt']       = ROOT.TH1F("MuonReconstruction_MuonPt","; pT (gen #mu), GeV ",30,25,70)
        self.sorted_efficiency['MuonRecEfficiency_MuonPt']     = ROOT.TEfficiency("MuonRecEfficiency_MuonPt","; pT (gen #mu), GeV ; #Epsilon ",30,25,70)



        self.eff_denum_hists1D['MuonReconstruction_MuonEta_den'] = ROOT.TH1F("MuonReconstruction_MuonEta_den","; |#eta| (gen #mu)",30,1,2.5)
        self.sorted_hists1D['MuonReconstruction_MuonEta']        = ROOT.TH1F("MuonReconstruction_MuonEta","; |#eta| (gen #mu)",30,1,2.5)
        self.sorted_efficiency['MuonRecEfficiency_MuonEta']      = ROOT.TEfficiency("MuonRecEfficiency_MuonEta","; |#eta| (gen #mu)",30,1,2.5)

#        self.sorted_efficiency['']        = ROOT.TEfficiency("","; 

        self.sorted_hists1D['MuonReconstruction_PtResolution']   = ROOT.TH1F("MuonReconstruction_PtResolution","; #Delta pT  (gen - rec), Gev",30,-5,5)

        # ME11
#        self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'] = ROOT.TH1F("SegmentEfficiency_MuonPt_den","; pT (gen #mu), GeV ",30,25,70)
#        self.sorted_hists1D['SegmentEfficiency_MuonPt']        = ROOT.TH1F("SegmentEfficiency_MuonPt", "; pT (gen #mu), GeV ",30,25,70)
#        self.sorted_efficiency['SegmentEfficiency_MuonPt']     = ROOT.TEfficiency("SegmentEfficiency_MuonPt","; pT (gen #mu), GeV ",30,25,70)

        self.eff_denum_hists1D['AnySegmentEfficiency_MuonPt_den'] = ROOT.TH1F("AnySegmentEfficiency_MuonPt_den","; pT (gen #mu) ",30,25,70)
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt']        = ROOT.TH1F("AnySegmentEfficiency_MuonPt", "; pT (gen #mu), GeV ",30,25,70)
        self.sorted_efficiency['AnySegmentEfficiency_MuonPt']     = ROOT.TEfficiency("AnySegmentEfficiency_MuonPt","; pT (gen #mu), GeV ",30,25,70)

#        self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_den'] = ROOT.TH1F("SegmentEfficiency_MuonPhi_den","; #phi (gen #mu) ",30,-3.15,3.15)
#        self.sorted_hists1D['SegmentEfficiency_MuonPhi']        = ROOT.TH1F("SegmentEfficiency_MuonPhi", "; #phi (gen #mu) ",30,-3.15,3.15)
#        self.sorted_efficiency['SegmentEfficiency_MuonPhi']      = ROOT.TEfficiency("SegmentEfficiency_MuonPhi",";  #phi (gen #mu) ",30,-3.15,3.15)


#        self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'] = ROOT.TH1F("SegmentEfficiency_MuonEta_den","; |#eta| (gen #mu)",30,1.0,2.5)
#        self.sorted_hists1D['SegmentEfficiency_MuonEta']        = ROOT.TH1F("SegmentEfficiency_MuonEta", "; |#eta| (gen #mu) ",30,1.0,2.5)
#        self.sorted_efficiency['SegmentEfficiency_MuonEta']        = ROOT.TEfficiency("SegmentEfficiency_MuonEta",";  |#eta| (gen #mu) ",30,1.0,2.5)

        self.eff_denum_hists1D['AnySegmentEfficiency_MuonEta_den'] = ROOT.TH1F("AnySegmentEfficiency_MuonEta_den","; |#eta| (gen #mu)",30,1.0,2.5)
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta']        = ROOT.TH1F("AnySegmentEfficiency_MuonEta", "; |#eta| (gen #mu) ",30,1.0,2.5)
        self.sorted_efficiency['AnySegmentEfficiency_MuonEta']        = ROOT.TEfficiency("AnySegmentEfficiency_MuonEta",";  |#eta| (gen #mu) ",30,1.0,2.5)

        self.eff_denum_hists1D['SegmentEfficiency_LocalX_den']  = ROOT.TH1F('SegmentEfficiency_LocalX_den',"; segment local X, cm", 50,-100, 100)
        self.sorted_hists1D['SegmentEfficiency_LocalX']  = ROOT.TH1F('SegmentEfficiency_LocalX',"; segment local X, cm", 50,-100, 100)
        self.sorted_efficiency['SegmentEfficiency_LocalX']        = ROOT.TEfficiency("SegmentEfficiency_LocalX","; segment local X, cm", 50,-100, 100)
       
        self.eff_denum_hists1D['SegmentEfficiency_LocalY_den']  = ROOT.TH1F('SegmentEfficiency_LocalY_den',"; segment local Y, cm", 50,-200, 200)
        self.sorted_hists1D['SegmentEfficiency_LocalY']  = ROOT.TH1F('SegmentEfficiency_LocalY',"; segment local Y, cm", 50,-200, 200)
        self.sorted_efficiency['SegmentEfficiency_LocalY']        = ROOT.TEfficiency("SegmentEfficiency_LocalY","; segment local Y, cm", 50,-200, 200)

        self.sorted_hists1D['ZeroSegmentsAllSimHits']   = ROOT.TH1F('ZeroSegmentsAllSimHits',"; N SimHits (0 segment bin) ", 15, 0.5, 14.5)
        self.sorted_hists1D['ZeroSegmentsMuonSimHits']  = ROOT.TH1F('ZeroSegmentsMuonSimHits',"; N MuonSimHits (0 segment bin) ", 15, 0.5, 14.5) 
        self.sorted_hists1D['ZeroSegmentsRecHits']      = ROOT.TH1F('ZeroSegmentsRecHits',"; N RecHits (0 segment bin)", 15, 0.5, 14.5)



        self.sorted_hists1D['SegmentMatchingPullX'] = ROOT.TH1F('SegmentMatchingPullX',"; Segment pull X (mc - rec)/#sigma", 50,-10, 10)
        self.sorted_hists1D['SegmentMatchingPullY'] = ROOT.TH1F('SegmentMatchingPullY',"; Segment pull Y (mc - rec)/#sigma", 50,-10, 10)

        self.sorted_hists1D['SegmentMatchingdX'] = ROOT.TH1F('SegmentMatchingdX',"; Segment #Delta X (mc - rec)", 50,-0.5, 0.5)
        self.sorted_hists1D['SegmentMatchingdY'] = ROOT.TH1F('SegmentMatchingdY',"; Segment #Delta Y (mc - rec)", 50,-2, 2)



        self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_den']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalX_den',"; segment local X, cm", 50,-100, 100)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalX',"; segment local X, cm", 50,-100, 100)
        self.sorted_efficiency['MatchedSegmentEfficiency_LocalX']        = ROOT.TEfficiency("MatchedSegmentEfficiency_LocalX","; segment local X, cm", 50,-100, 100)
       
        self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_den']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalY_den',"; segment local Y, cm", 50,-200, 200)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalY',"; segment local Y, cm", 50,-200, 200)
        self.sorted_efficiency['MatchedSegmentEfficiency_LocalY']        = ROOT.TEfficiency("MatchedSegmentEfficiency_LocalY","; segment local Y, cm", 50,-200, 200)




        # ME11
        self.eff_denum_hists1D['SegmentEfficiency_MuonPt_ME11_den']    = ROOT.TH1F("SegmentEfficiency_MuonPt_ME11_den","; pT (gen #mu), GeV ",30,25,70)
        self.sorted_hists1D['SegmentEfficiency_MuonPt_ME11']           = ROOT.TH1F("SegmentEfficiency_MuonPt_ME11", "; pT (gen #mu), GeV ",30,25,70)
        self.sorted_efficiency['SegmentEfficiency_MuonPt_ME11']        = ROOT.TEfficiency("SegmentEfficiency_MuonPt_ME11","; pT (gen #mu), GeV ",30,25,70)

        self.eff_denum_hists1D['AnySegmentEfficiency_MuonPt_ME11_den'] = ROOT.TH1F("AnySegmentEfficiency_MuonPt_ME11_den","; #phi (gen #mu) ",30,25,70)
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt_ME11']           = ROOT.TH1F("AnySegmentEfficiency_MuonPt_ME11", "; pT (gen #mu), GeV ",30,25,70)
        self.sorted_efficiency['AnySegmentEfficiency_MuonPt_ME11']        = ROOT.TEfficiency("AnySegmentEfficiency_MuonPt_ME11","; pT (gen #mu), GeV ",30,25,70)


        self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_ME11_den']    = ROOT.TH1F("SegmentEfficiency_MuonPhi_ME11_den","; #phi (gen #mu) ",30,-3.15,3.15)
        self.sorted_hists1D['SegmentEfficiency_MuonPhi_ME11']           = ROOT.TH1F("SegmentEfficiency_MuonPhi_ME11", "; #phi (gen #mu) ",30,-3.15,3.15)
        self.sorted_efficiency['SegmentEfficiency_MuonPhi_ME11']        = ROOT.TEfficiency("SegmentEfficiency_MuonPhi_ME11","; #phi (gen #mu) ",30,-3.15,3.15)


#        self.sorted_hists1D['AnySegmentEfficiency_MuonPhi_ME11']           = ROOT.TH1F("AnySegmentEfficiency_MuonPhi_ME11", "; #phi (gen #mu) ",30,-3.15,3.15)
#        self.sorted_efficiency['AnySegmentEfficiency_MuonPhi_ME11']        = ROOT.TEfficiency("AnySegmentEfficiency_MuonPhi_ME11","; #phi (gen #mu) ",30,-3.15,3.15)


        self.eff_denum_hists1D['SegmentEfficiency_MuonEta_ME11_den']    = ROOT.TH1F("SegmentEfficiency_MuonEta_ME11_den","; |#eta| (gen #mu)",30,1.0,2.5)
        self.sorted_hists1D['SegmentEfficiency_MuonEta_ME11']           = ROOT.TH1F("SegmentEfficiency_MuonEta_ME11", "; |#eta| (gen #mu) ",30,1.0,2.5)
        self.sorted_efficiency['SegmentEfficiency_MuonEta_ME11']        = ROOT.TEfficiency("SegmentEfficiency_MuonEta_ME11","; |#eta| (gen #mu) ",30,1.0,2.5)

        self.eff_denum_hists1D['AnySegmentEfficiency_MuonEta_ME11_den'] = ROOT.TH1F("AnySegmentEfficiency_MuonEta_ME11_den","; |#eta| (gen #mu)",30,1.0,2.5)
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta_ME11']           = ROOT.TH1F("AnySegmentEfficiency_MuonEta_ME11", "; |#eta| (gen #mu) ",30,1.0,2.5)
        self.sorted_efficiency['AnySegmentEfficiency_MuonEta_ME11']        = ROOT.TEfficiency("AnySegmentEfficiency_MuonEta_ME11","; |#eta| (gen #mu) ",30,1.0,2.5)


        self.eff_denum_hists1D['SegmentEfficiency_LocalX_ME11_den']  = ROOT.TH1F('SegmentEfficiency_LocalX_ME11_den',"; segment local X, cm", 50,-100, 100)
        self.sorted_hists1D['SegmentEfficiency_LocalX_ME11']  = ROOT.TH1F('SegmentEfficiency_LocalX_ME11',"; segment local X, cm", 50,-100, 100)
        self.sorted_efficiency['SegmentEfficiency_LocalX_ME11']        = ROOT.TEfficiency("SegmentEfficiency_LocalX_ME11","; segment local X, cm", 50,-100, 100)


        self.eff_denum_hists1D['SegmentEfficiency_LocalY_ME11_den']  = ROOT.TH1F('SegmentEfficiency_LocalY_ME11_den',"; segment local Y, cm", 50,-200, 200)
        self.sorted_hists1D['SegmentEfficiency_LocalY_ME11']  = ROOT.TH1F('SegmentEfficiency_LocalY_ME11',"; segment local Y, cm", 50,-200, 200)
        self.sorted_efficiency['SegmentEfficiency_LocalY_ME11']        = ROOT.TEfficiency("SegmentEfficiency_LocalY_ME11","; segment local Y, cm", 50,-200, 200)




        self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_ME11_den']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalX_ME11_den',"; segment local X, cm", 50,-100, 100)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX_ME11']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalX_ME11',"; segment local X, cm", 50,-100, 100)
        self.sorted_efficiency['MatchedSegmentEfficiency_LocalX_ME11']        = ROOT.TEfficiency("MatchedSegmentEfficiency_LocalX_ME11","; segment local X, cm", 50,-100, 100)


        self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_ME11_den']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalY_ME11_den',"; segment local Y, cm", 50,-200, 200)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY_ME11']  = ROOT.TH1F('MatchedSegmentEfficiency_LocalY_ME11',"; segment local Y, cm", 50,-200, 200)
        self.sorted_efficiency['MatchedSegmentEfficiency_LocalY_ME11']        = ROOT.TEfficiency("MatchedSegmentEfficiency_LocalY_ME11","; segment local Y, cm", 50,-200, 200)
 
        # pulls
        self.sorted_hists1D['SimRecHits_PullX_allLayers'] = ROOT.TH1F('SimRecHits_PullX_allLayers',"; pull X ", 50,-5, 5)
        self.sorted_hists1D['SimRecHits_PullY_allLayers'] = ROOT.TH1F('SimRecHits_PullY_allLayers',"; pull Y ", 50,-5, 5)





#        self.sorted_hists1D[''] = ROOT.TH1F("", "; ", 11, -0.5, 10.5) # 1D hist templtae



    def writeHistos(self, Histos1D, Histos2D):
        
        ROOT.gROOT.ProcessLine(".L tdrstyle.cc")
        setTDRStyle(False)
        c = ROOT.TCanvas("c","c",700,700)
        for key in Histos1D:
            c.cd()
            normalized = 'Norm' in key
            if normalized and Histos1D[key].Integral() > 0:
                Histos1D[key].Scale(1/Histos1D[key].Integral())
            Efficiency = 'Efficiency' in key
            if Efficiency:
                Histos1D[key].GetYaxis().SetRangeUser(0.5,1.05)
            Histos1D[key].Draw("HIST")
#            c.SaveAs(opt.outDir+'/'+str(Histos1D[key].GetName())+'.eps')
            c.SaveAs(opt.outDir+'/'+str(Histos1D[key].GetName())+'.png')
            c.Clear()

        c1 = ROOT.TCanvas("c1","c1",700,700)
        for key in Histos2D:
            c1.cd()
            Histos2D[key].Draw()
#            c1.SaveAs(opt.outDir+'/'+str(Histos2D[key].GetName())+'.eps')
            c1.SaveAs(opt.outDir+'/'+str(Histos2D[key].GetName())+'.png')
            c1.Clear()


    def writeHistosToRoot(self, Histos1D, Histos2D):
        
        ROOT.gROOT.ProcessLine(".L tdrstyle.cc")
        setTDRStyle(False)
        outFile = ROOT.TFile(opt.jobName+'.root',"RECREATE")
        
        for key in Histos1D:
            normalized = 'Norm' in key
            if normalized and Histos1D[key].Integral() > 0:
                Histos1D[key].Scale(1/Histos1D[key].Integral())
            outFile.cd()
            Histos1D[key].Write()
        for key in Histos2D:
            Histos2D[key].Write()

        outFile.Write()
        outFile.Close()


    def writeSortedHistosToRoot(self, Histos1D, Histos2D, Efficiency, prefix):
        
        ROOT.gROOT.ProcessLine(".L tdrstyle.cc")
        setTDRStyle(False)
        outFile = ROOT.TFile(opt.jobName+prefix+'.root',"RECREATE")
        
        for key in Histos1D:
            normalized = 'Norm' in key
            if normalized and Histos1D[key].Integral() > 0:
                Histos1D[key].Scale(1/Histos1D[key].Integral())
            outFile.cd()
            Histos1D[key].Write()
        for key in Histos2D:
            Histos2D[key].Write()

        for key in Efficiency:
            Efficiency[key].Write()

        outFile.Write()
        outFile.Close()




    def endjob(self,singleFile):

        #Fill Eff Hists
        for x in range(0,600):
            eff = 0
            err = 0
            if self.simHitsEffDen[x] > 0:
                eff = float(self.simHitsEffNum[x])/self.simHitsEffDen[x]
                err_nom   =float( pow( self.simHitsEffNum[x]*self.simHitsEffDen[x]*(self.simHitsEffNum[x] + self.simHitsEffDen[x]) , 0.5 ))
                err_den   =float( pow(self.simHitsEffDen[x],2))
                err       = err_nom/err_den
            if x == 599:
                eff = float(self.simHitsOverallEffNum)/self.simHitsOverallEffDen
                err_nom = float( pow( self.simHitsOverallEffNum*self.simHitsOverallEffDen*(self.simHitsOverallEffNum + self.simHitsOverallEffDen), 0.5)) 
                err_den = float( pow(self.simHitsOverallEffDen,2))
                err     = err_nom/err_den
            #print x,  self.simHitsEffDen[x], self.simHitsEffNum[x], eff, self.simHitsOverallEffDen, self.simHitsOverallEffDen
            self.hists1D['simHitsRecoEfficiency'].SetBinContent(x+1,eff)
            self.hists1D['simHitsRecoEfficiency'].SetBinError(x+1,err)
            for y in range(0,6):
                eff = 0
                err = 0

                if self.simHitsLayerEffDen[x][y] > 0:
                    eff = float(self.simHitsLayerEffNum[x][y])/self.simHitsLayerEffDen[x][y]
                    err_nom =  float( pow( self.simHitsLayerEffNum[x][y]*self.simHitsLayerEffDen[x][y]*(self.simHitsLayerEffNum[x][y] + self.simHitsLayerEffDen[x][y]), 0.5 ))
                    err_den =  float( pow(self.simHitsLayerEffDen[x][y],2))
                    err     =  err_nom/err_den

                self.hists1D['simHitsRecoEfficiency_l'+str(y+1)].SetBinContent(x+1,eff)
                self.hists1D['simHitsRecoEfficiency_l'+str(y+1)].SetBinError(x+1,err)


        # Muon Recons
        self.sorted_efficiency['MuonRecEfficiency_MuonPt'] = ROOT.TEfficiency(MuonReconstruction_MuonPt, MuonReconstruction_MuonPt_den)

        self.sorted_hists1D['MuonReconstruction_MuonPt'].Sumw2()
        self.sorted_hists1D['MuonReconstruction_MuonPt'].Divide(self.eff_denum_hists1D['MuonReconstruction_MuonPt_den'])

        self.sorted_efficiency['MuonRecEfficiency_MuonEta'] = ROOT.TEfficiency(MuonReconstruction_MuonEta, MuonReconstruction_MuonEta_den)
        self.sorted_hists1D['MuonReconstruction_MuonEta'].Sumw2()
        self.sorted_hists1D['MuonReconstruction_MuonEta'].Divide(self.eff_denum_hists1D['MuonReconstruction_MuonEta_den'])


#        self.sorted_efficiency[''] = ROOT.TEfficiency()
        # Find Segment Efficiency
#        self.sorted_efficiency['SegmentEfficiency_MuonPt'] = ROOT.TEfficiency(SegmentEfficiency_MuonPt,SegmentEfficiency_MuonPt_den)
#        self.sorted_hists1D['SegmentEfficiency_MuonPt'].Sumw2()
#        self.sorted_hists1D['SegmentEfficiency_MuonPt'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'])

        self.sorted_efficiency['AnySegmentEfficiency_MuonPt'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonPt,AnySegmentEfficiency_MuonPt_den)
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt'].Sumw2()
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt'].Divide(self.eff_denum_hists1D['AnySegmentEfficiency_MuonPt_den'])


#        self.sorted_efficiency['SegmentEfficiency_MuonPhi'] = ROOT.TEfficiency(SegmentEfficiency_MuonPhi,SegmentEfficiency_MuonPhi_den) 
#        self.sorted_hists1D['SegmentEfficiency_MuonPhi'].Sumw2()
#        self.sorted_hists1D['SegmentEfficiency_MuonPhi'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_den'])


#        self.sorted_efficiency['AnySegmentEfficiency_MuonPhi'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonPhi,SegmentEfficiency_MuonPhi_den) 
#        self.sorted_hists1D['AnySegmentEfficiency_MuonPhi'].Sumw2()
#        self.sorted_hists1D['AnySegmentEfficiency_MuonPhi'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_den'])

#        self.sorted_efficiency['SegmentEfficiency_MuonEta'] = ROOT.TEfficiency(SegmentEfficiency_MuonEta,SegmentEfficiency_MuonEta_den)
#        self.sorted_hists1D['SegmentEfficiency_MuonEta'].Sumw2()
#        self.sorted_hists1D['SegmentEfficiency_MuonEta'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'])

        self.sorted_efficiency['AnySegmentEfficiency_MuonEta'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonEta,AnySegmentEfficiency_MuonEta_den)
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta'].Sumw2()
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta'].Divide(self.eff_denum_hists1D['AnySegmentEfficiency_MuonEta_den'])


        self.sorted_efficiency['SegmentEfficiency_LocalX'] = ROOT.TEfficiency(SegmentEfficiency_LocalX,SegmentEfficiency_LocalX_den)
        self.sorted_hists1D['SegmentEfficiency_LocalX'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_LocalX'].Divide(self.eff_denum_hists1D['SegmentEfficiency_LocalX_den'])

        self.sorted_efficiency['SegmentEfficiency_LocalY'] = ROOT.TEfficiency(SegmentEfficiency_LocalY,SegmentEfficiency_LocalY_den)
        self.sorted_hists1D['SegmentEfficiency_LocalY'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_LocalY'].Divide(self.eff_denum_hists1D['SegmentEfficiency_LocalY_den'])



        self.sorted_efficiency['MatchedSegmentEfficiency_LocalX'] = ROOT.TEfficiency(MatchedSegmentEfficiency_LocalX,MatchedSegmentEfficiency_LocalX_den)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX'].Sumw2()
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX'].Divide(self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_den'])

        self.sorted_efficiency['MatchedSegmentEfficiency_LocalY'] = ROOT.TEfficiency(MatchedSegmentEfficiency_LocalY,MatchedSegmentEfficiency_LocalY_den)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY'].Sumw2()
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY'].Divide(self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_den'])







        self.sorted_efficiency['SegmentEfficiency_MuonPt_ME11'] = ROOT.TEfficiency(SegmentEfficiency_MuonPt_ME11,SegmentEfficiency_MuonPt_ME11_den)
        self.sorted_hists1D['SegmentEfficiency_MuonPt_ME11'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_MuonPt_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPt_ME11_den'])

        self.sorted_efficiency['AnySegmentEfficiency_MuonPt_ME11'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonPt_ME11,AnySegmentEfficiency_MuonPt_ME11_den)
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt_ME11'].Sumw2()
        self.sorted_hists1D['AnySegmentEfficiency_MuonPt_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPt_ME11_den'])


        self.sorted_efficiency['SegmentEfficiency_MuonPhi_ME11'] = ROOT.TEfficiency(SegmentEfficiency_MuonPhi_ME11,SegmentEfficiency_MuonPhi_ME11_den)
        self.sorted_hists1D['SegmentEfficiency_MuonPhi_ME11'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_MuonPhi_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_ME11_den'])

#        self.sorted_efficiency['AnySegmentEfficiency_MuonPhi_ME11'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonPhi_ME11,SegmentEfficiency_MuonPhi_ME11_den)
#        self.sorted_hists1D['AnySegmentEfficiency_MuonPhi_ME11'].Sumw2()
#        self.sorted_hists1D['AnySegmentEfficiency_MuonPhi_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPhi_ME11_den'])


        self.sorted_efficiency['SegmentEfficiency_MuonEta_ME11'] = ROOT.TEfficiency(SegmentEfficiency_MuonEta_ME11,SegmentEfficiency_MuonEta_ME11_den)
        self.sorted_hists1D['SegmentEfficiency_MuonEta_ME11'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_MuonEta_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonEta_ME11_den'])


        self.sorted_efficiency['AnySegmentEfficiency_MuonEta_ME11'] = ROOT.TEfficiency(AnySegmentEfficiency_MuonEta_ME11,AnySegmentEfficiency_MuonEta_ME11_den)
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta_ME11'].Sumw2()
        self.sorted_hists1D['AnySegmentEfficiency_MuonEta_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonEta_ME11_den'])

        self.sorted_efficiency['SegmentEfficiency_LocalX_ME11'] = ROOT.TEfficiency(SegmentEfficiency_LocalX_ME11,SegmentEfficiency_LocalX_ME11_den)
        self.sorted_hists1D['SegmentEfficiency_LocalX_ME11'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_LocalX_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_LocalX_ME11_den'])


        self.sorted_efficiency['SegmentEfficiency_LocalY_ME11'] = ROOT.TEfficiency(SegmentEfficiency_LocalY_ME11,SegmentEfficiency_LocalY_ME11_den)
        self.sorted_hists1D['SegmentEfficiency_LocalY_ME11'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_LocalY_ME11'].Divide(self.eff_denum_hists1D['SegmentEfficiency_LocalY_ME11_den'])



        self.sorted_efficiency['MatchedSegmentEfficiency_LocalX_ME11'] = ROOT.TEfficiency(MatchedSegmentEfficiency_LocalX_ME11,MatchedSegmentEfficiency_LocalX_ME11_den)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX_ME11'].Sumw2()
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalX_ME11'].Divide(self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalX_ME11_den'])


        self.sorted_efficiency['MatchedSegmentEfficiency_LocalY_ME11'] = ROOT.TEfficiency(MatchedSegmentEfficiency_LocalY_ME11,MatchedSegmentEfficiency_LocalY_ME11_den)
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY_ME11'].Sumw2()
        self.sorted_hists1D['MatchedSegmentEfficiency_LocalY_ME11'].Divide(self.eff_denum_hists1D['MatchedSegmentEfficiency_LocalY_ME11_den'])




        #Average recHits2D
        myFile = open(opt.outDir+'/AverageRecHits2D.txt', 'w')
        counter = 0
        for x in self.stationRings:
            counter+=1
            self.nRecHitsPerStation[x] = self.nRecHitsPerStation[x]/self.nChambers[x]/self.totalEvents
            self.hists1D['avgRecHits2D'].SetBinContent(counter,self.nRecHitsPerStation[x])
            string = x+'   '+str(self.nRecHitsPerStation[x])+'\n'
            myFile.write(string)
        myFile.close()



        myEffFile = open(opt.outDir+'/SimHitEfficiencies.txt', 'w')
        
        for ec in range(0,2):
            EC = '+'
            if ec == 1:
                EC = '-'
            for st in range(0,4):
                for rg in range(0,4):
                    if st+1 > 1 and rg+1 > 2: continue
                    string = 'ME'+EC+str(st+1)+'/'+str(rg+1)+'\n'
                    myEffFile.write(string)
                    myEffFile.write('--------------------\n')

                    for ch in range(0,36):
                        if st+1 > 1 and rg+1 == 1 and ch+1 > 18: continue
                        num = 0
                        den = 0
                        effAr = [0] * 6
                        for lr in range(0,6):

                            eff = 0
                            err = 0
                            if self.simHitsChamberEffDen[ec][st][rg][ch][lr] > 0:
                                eff = float(self.simHitsChamberEffNum[ec][st][rg][ch][lr])/self.simHitsChamberEffDen[ec][st][rg][ch][lr]
                                err_nom = float( pow( self.simHitsChamberEffNum[ec][st][rg][ch][lr]*self.simHitsChamberEffDen[ec][st][rg][ch][lr]*(self.simHitsChamberEffNum[ec][st][rg][ch][lr]+ self.simHitsChamberEffDen[ec][st][rg][ch][lr]),0.5))
                                err_den = float( pow(self.simHitsChamberEffDen[ec][st][rg][ch][lr],2))
                                err = err_nom/err_den
                                effAr[lr] = eff;
                                num += self.simHitsChamberEffNum[ec][st][rg][ch][lr]
                                den += self.simHitsChamberEffDen[ec][st][rg][ch][lr]
                            string = 'ME'+EC+str(st+1)+'-'+str(rg+1)+'_l'+str(lr+1)+'_simHitEfficiency'
                            self.hists1D[string].SetBinContent(ch+1,eff)
                            self.hists1D[string].SetBinError(ch+1,err)
 

                        if den > 0:
                            eff = float(num)/den
                            err_nom = float( pow( num*den*(num+den),0.5))
                            err_den = float( pow(den,2))
                            err     = err_nom/err_den
                        else: 
                            eff = 0
                            err = 0
                        string = 'ME'+EC+str(st+1)+'-'+str(rg+1)+'_simHitEfficiency'
                        self.hists1D[string].SetBinContent(ch+1,eff)
                        self.hists1D[string].SetBinError(ch+1,err)
                        #string = '  Chamber '+str(ch+1)+': '+str(effAr[0])+'  '+str(effAr[1])+'  '+str(effAr[2])+'  '+str(effAr[3])+'  '+str(effAr[4])+'  '+str(effAr[5])+'     '+str(eff)+'\n'
                        string = '  Chamber {0}: {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}   {6:.3f}\n'.format(ch+1,effAr[0],effAr[1],effAr[2],effAr[3],effAr[4],effAr[5],eff)
                        myEffFile.write(string)
                    myEffFile.write('\n')
                myEffFile.write('\n')

                    
        myEffFile.close()
        print('Total number of events processed:  ', self.totalEvents)
        if self.totalEvents > 0:
            if singleFile:
                
                self.writeHistos(self.hists1D,self.hists2D)
                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D,self.sorted_hists2D,self.sorted_efficiency,"sorted")
            else:
                self.writeHistos(self.hists1D,self.hists2D)
                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D,self.sorted_hists2D,self.sorted_efficiency,"sorted")
        




#Main  
if __name__ == "__main__":


    global opt, args
    parseOptions()

    myClass = Analysis()
    singleFile = False

    if opt.file.endswith(".root"):
        singleFile = True
    elif opt.file.endswith(".txt"):
        singleFile = False
    else:
        raise RuntimeError, "opt.file: file name does not end with .root or .txt!"

    print "Begin Analysis"

    # Loop for parallel or single file 
    if singleFile:
        myClass.doAnalysis(opt.file)
    else:
        lines = open(opt.file,"r")
        for line in lines:
            f = line.split()
            if not f[0].endswith(".root"): continue
            if len(f) < 1: continue
            print "Opening file",f[0]
            myClass.doAnalysis(f[0])
            

    myClass.endjob(singleFile)
