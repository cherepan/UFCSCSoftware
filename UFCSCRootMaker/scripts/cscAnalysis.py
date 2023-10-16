

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
        
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    


class Analysis():

    def __init__(self):

        self.hists1D = {}
        self.hists2D = {}

        self.sorted_hists1D = {}
        self.sorted_hists2D = {}

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

    def genMuonLV(self, tree, index):
        if index > tree.gen_muons_nMuons or index == -1:
            print("============= >  genMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        genMuon = TLorentzVector(tree.gen_muons_px[index],
                                 tree.gen_muons_py[index],
                                 tree.gen_muons_pz[index],
                                 tree.gen_muons_energy[index])
        return genMuon


    def recMuonLV(self, tree, index):
        if index > tree.muons_nMuons or index == -1:
            print("============= >recMuonLV:  Requested index is out if range or equal to -1, return 0,0,0,0;")
            return TLorentzVector(0,0,0,0)
        recMuon = TLorentzVector(tree.muons_px[index],
                                 tree.muons_py[index],
                                 tree.muons_pz[index],
                                 tree.muons_energy[index])
        return recMuon



    def recoMuonMatchedIndex(self, tree, index_genMuon):
        list_dR_muon=[]
        genMuon = self.genMuonLV(tree, index_genMuon)

        for n in range(tree.muons_nMuons):
            recMatchedMuon = TLorentzVector(tree.muons_px[n], tree.muons_py[n], tree.muons_pz[n],tree.muons_energy[n])
            list_dR_muon.append([recMatchedMuon.DeltaR(genMuon),n, abs(recMatchedMuon.Pt() - genMuon.Pt())])
        list_dR_muon.sort(key=lambda element : element[0])    
        if len(list_dR_muon)!=0 and  list_dR_muon[0][2] < 2 :return  list_dR_muon[0][1]
        return -1
        


    def linked_gen_mu_index(self, tree, i):
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




    def ChamberID(self, endcap, station, ring, chamber):
        return endcap*10000 + 1000*station + 100*ring + chamber


    def AllGenRecoMuonsMap(self, tree):
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

                 if (muonsegmentChamberID == segmentChamberID and  
                     segmenLocalX == muon_segment_localX      and  
                     segmenLocalY == muon_segment_localY): muon_segments.append(s)
        return muon_segments
                     


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
                if self.ChamberID(tree.recHits2D_ID_endcap[i2DRecHit],
                                  tree.recHits2D_ID_station[i2DRecHit],
                                  tree.recHits2D_ID_ring[i2DRecHit],
                                  tree.recHits2D_ID_chamber[i2DRecHit]) == chamber_of_srechit:
                          
                          
                    if(layer_2DRecHit == segment_rechit_layer   and 
                       localX_2DRecHit == segment_rechit_localX and 
                       localY_2DRecHit == segment_rechit_localY):
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



    def link_rechits_to_segments(self, tree, list_of_segments):
        outlist = []
        for i in list_of_segments:
            outlist.append([i,self.allRechits_of_segment(tree, i)])
        return outlist    

                      
    def doAnalysis(self,file):
        global opt, args
  
        tfile = ROOT.TFile(file,"READ")
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

            if i%1000 == 0:
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
#                        for muon_segment in range(0, len(allSegments_belonging_toMuon(tree, n))):
#                            rechits_segments_list.append()
                            



#                if len(MuonSegmentsRechitsList)>1: 
#                    print(" len(MuonSegmentsRechitsList)",                     len(MuonSegmentsRechitsList))
#                    print(" MuonSegmentsRechitsList:         ",                MuonSegmentsRechitsList)
#                    print(" MuonSegmentsRechitsList:   [0][0]   ",             MuonSegmentsRechitsList[0][0])
#                    print(" MuonSegmentsRechitsList:   [1][0]   ",             MuonSegmentsRechitsList[1][0])
#                    print(" MuonSegmentsRechitsList:   [0][0]   ",          MuonSegmentsRechitsList[0][0])
#                    print(" MuonSegmentsRechitsList:   [0][1]   ",          MuonSegmentsRechitsList[0][1])
#                    print(" MuonSegmentsRechitsList:   [0][1][0]   ",       MuonSegmentsRechitsList[0][1][0])
#                    print(" MuonSegmentsRechitsList:   [0][1][1]   ",       MuonSegmentsRechitsList[0][1][1])
#                    print(" MuonSegmentsRechitsList:   [0][1][2]   ",       MuonSegmentsRechitsList[0][1][2])
#                    print("====================")         
#                    print(" MuonSegmentsRechitsList:   [0][1][0][0]   ",    MuonSegmentsRechitsList[0][1][0][0])
#                    print(" MuonSegmentsRechitsList:   [0][1][1][0]   ",    MuonSegmentsRechitsList[0][1][1][0])
#                    print(" MuonSegmentsRechitsList:   [0][1][2][0]   ",    MuonSegmentsRechitsList[0][1][2][0])
#                                                          
#                    print(" MuonSegmentsRechitsList:   [0][1][0][1][3]   ", MuonSegmentsRechitsList[0][1][0][1][3])
#                    print(" MuonSegmentsRechitsList:   [0][1][1][1][3]   ", MuonSegmentsRechitsList[0][1][1][1][3])
#                    print(" MuonSegmentsRechitsList:   [0][1][2][1][3]   ", MuonSegmentsRechitsList[0][1][2][1][3])
#                    print(" MuonSegmentsRechitsList:  size of ( [1] )   ", len(MuonSegmentsRechitsList[1]) )

#                if len(list_test)!=0: print("lllllllllllllll:   ", list_test[1])
                #CSCSegments
                CSC_SegmentCounter = [0] * 600
                CSC_SegmentMap = [''] * 600
                for n in range(tree.cscSegments_nSegments):
#                    print(" print out rechits of the segment  ", n,                    self.allRechits_of_segment(tree, n))
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
                    print("__________________________________________________________________________________")
                    selectedGenMuons=[]
                    for im in range(0, tree.gen_muons_nMuons):
                        muon = self.genMuonLV(tree,im)
                        if muon.Pt()> 3 and math.fabs(muon.Eta()) > 1.1 and math.fabs(muon.Eta()) < 2.4:
                            selectedGenMuons.append(im)


                        recoMuIndex = self.recoMuonMatchedIndex(tree,im) 
                        if recoMuIndex!= -1: recoMuon = self.recMuonLV(tree,recoMuIndex)
  #                  print(" print reco gen map   ",self.SelectedGenRecoMuonsMap(tree,selectedGenMuons))
                    self.sorted_hists1D["GenRecoMatchingSize"].Fill(len(self.SelectedGenRecoMuonsMap(tree,selectedGenMuons)))

                    ### debug HERE
                    print(" gen reco muons map  ", self.SelectedGenRecoMuonsMap(tree,selectedGenMuons))

                    for n in range(tree.muons_nMuons):
                        if math.fabs(self.recMuonLV(tree,n).Eta() > 1.1):
                            print(" muon   n, ++++++++++++ nSegments, standalon/Global  ",n, len ( self.allSegments_belonging_toMuon(tree, n)), tree.muons_isStandAloneMuon[n], tree.muons_isGlobalMuon[n])
                            self.recMuonLV(tree,n).Print()
                            if tree.muons_isStandAloneMuon[n] and len(self.allSegments_belonging_toMuon(tree, n) ) > 0:


                                print(" Muon n   ", n, "  has   ", self.allSegments_belonging_toMuon(tree,n)," segments  ")
                                for k in self.allSegments_belonging_toMuon(tree,n):
                                    print("  Segment  #   ", k  , "  has    ", self.allRechits_of_segment(tree,k), "  rechits " ) #







                    for l in self.SelectedGenRecoMuonsMap(tree,selectedGenMuons):
                        if l[1]!=-1:
                            print("=======================================   matched   gen and reco indices    ", l[0],l[1]) 

                            self.genMuonLV(tree,l[0]).Print()
                            self.recMuonLV(tree,l[1]).Print()

                            self.sorted_hists1D["dRMatching"].Fill(self.recMuonLV(tree,l[1]).DeltaR(self.genMuonLV(tree,l[0])))

#                            print("------------------- muon index  ", l[1])
#                            print("print all segments that do belong to muon:  ", self.allSegments_belonging_toMuon(tree, l[1]))
#                            print("print all segments that do NOT belong to muon:  ", self.allSegments_NOT_belonging_toMuon(tree, l[1]))
                    #print("============================== hits loop ============================= ")
                    selected_hits=[] 
                    for n in range(0,tree.simHits_nSimHits):
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

                        isMuonHit=False
                        for m in selectedGenMuons:
                            if self.simHitBelongToGenMuon(tree, n, m) and self.recoMuonMatchedIndex(tree, m): 
                                isMuonHit = True
#                        print(" #hit   isMuonHit  ", n, isMuonHit)
#                        if abs(tree.simHits_particleType[n]) == 13:
                        if abs(tree.simHits_particleType[n]) == 13 and isMuonHit:   # make efficiency plots 

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
                            for m in range(0,tree.recHits2D_nRecHits2D):
                                if abs(tree.recHits2D_simHit_particleTypeID[m]) == 13:
                                    if tree.recHits2D_ID_chamberSerial[m] != shChamberSerial: continue
                                    if tree.recHits2D_ID_layer[m] != shLayer: continue
                                    xLow  = tree.recHits2D_localX[m] - 2*sqrt(tree.recHits2D_localXXerr[m])
                                    xHigh = tree.recHits2D_localX[m] + 2*sqrt(tree.recHits2D_localXXerr[m])
                                    yLow  = tree.recHits2D_localY[m] - 2*sqrt(tree.recHits2D_localYYerr[m])
                                    yHigh = tree.recHits2D_localY[m] + 2*sqrt(tree.recHits2D_localYYerr[m])

                                    if (x < xLow or x > xHigh) and (y < yLow or y > yHigh): continue
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

        self.hists2D['recHitsVSp'] = ROOT.TH2F("recHitsVSp","; P (GeV); N RecHits",1000, 0, 800, 100, 0, 60)
        self.hists2D['recHitsVSpT'] = ROOT.TH2F("recHitsVSpT","; pT (GeV); N RecHits",1000, 0, 800, 100, 0, 60)
        self.hists2D['recHitsVSEta'] = ROOT.TH2F("recHitsVSEta","; eta; N RecHits",1000, -2.5, 2.5, 100, 0, 60)
        self.hists2D['recHitsPerSegVSp'] = ROOT.TH2F("recHitsPerSegVSp","; P (GeV); N RecHits/Segment", 1000, 0, 800, 8, 0, 8)
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
        self.sorted_hists1D['GenRecoMatchingSize'] = ROOT.TH1F("GenRecoMatchingSize", "; n matched muons  ", 4, -0.5, 3.5) # 1D hist templtae
        self.sorted_hists1D['dRMatching'] = ROOT.TH1F("dRMatching", ";dR(gen-reco) ", 50, -0.001, 0.05) # 1D hist templtae
#        self.hists1D[''] = ROOT.TH1F("", "; ", 11, -0.5, 10.5) # 1D hist templtae



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


    def writeSortedHistosToRoot(self, Histos1D, Histos2D, prefix):
        
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
        
        if self.totalEvents > 0:
            if singleFile:
                
                self.writeHistos(self.hists1D,self.hists2D)
                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D,self.sorted_hists2D,"sorted")
            else:
                self.writeHistos(self.hists1D,self.hists2D)
                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D,self.sorted_hists2D,"sorted")
        




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
