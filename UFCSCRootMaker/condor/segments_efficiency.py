#!/usr/bin/env python


import sys, os, pwd
import optparse, shlex, re
import math
from ROOT import *
import ROOT
from array import array
from numpy import sqrt 


import tools as tools
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
    global opt, args, debug, Chambers
    (opt, args) = parser.parse_args()
    Chambers = [11, 12, 13 , 21, 22, 31, 32, 41 ,42] # Station + Ring
    debug = False


class Analysis():

    def __init__(self):

        self.hists1D = {}
        self.hists2D = {}

        self.sorted_hists1D    = {}
        self.sorted_hists2D    = {}
        self.sorted_efficiency = {}
        self.eff_denum_hists1D = {}


        self.totalEvents = 0
        self.defineHistos()

        self.simHits_muonMatched = []
        self.recHits_muonMatched = []



                      
    def doAnalysis(self,file):
        global opt, args
  
        tfile = ROOT.TFile(file,"READ")
        print("   ==============!!!!!!!!!!!!!!!!!!!!!+===============   ")
        if not tfile:
            raise RunTimeError("No input file specified or root file could not be found!")

        print("Opened file ", file)
        
        if opt.isMC:
            tree = tfile.Get("cscRootMaker/Events")
        else:
            tree = tfile.Get("cscRootMaker/Events")

        if not tree:
            raise RunTimeError("Tree not found!")

        SegmentFarFromSimHits = open("SegmentFarFromSimHits.txt","w")
        EventsAndChambersWithZeroRuSegments = open("EventsAndChambersWithZeroRuSegmentsLotsOfRecHits.txt","w")
        EventsAndChambersWithTwoSegments = open("EventsAndChambersWithTwoSegments.txt","w")
        EventsAndChambersWithFourSegments = open("EventsAndChambersWithFourSegments.txt","w")

        #Analysis Loop
        for i in range( tree.GetEntries() ):
#            print('===============================    Event loop    ========================================= ')
            tree.GetEntry(i)

            if i%100 == 0:
                 print("Event ",i)
            if self.totalEvents > opt.maxEvents:
                break
            self.totalEvents+=1
            recMuon_segments_rechits = []
            if opt.isLocalReco or opt.isFullReco:

                self.simHits_muonMatched[:]=[]
                self.recHits_muonMatched[:]=[]

                MuonSegmentsRechitsList = []

                if opt.isMC:

                    MuonsFromZ = tools.findMuonsFromZ(tree)
#                    GRMuonsMap = tools.GenCSCRecoMuonsMap(tree)

                    for mu in MuonsFromZ:                        
                    
                            genMuIndex  = mu
                            GMuLV = tools.genMuonLV(tree, genMuIndex);
                            recoMuIndex = tools.recoMuonMatchedIndex(tree,mu)
                            
                            if( recoMuIndex!=-1 ):
                                RMuLV = tools.recMuonLV(tree, recoMuIndex);

                            if recoMuIndex!=-1:
                                ChambersCrossedByMuon    = tools.Chambers_crossedByMuon(tree, recoMuIndex)
                                AllRecHitOfTheMuon = tools.allRecHits_belonging_toMuon(tree, recoMuIndex)
                                self.sorted_hists1D["nChambers_crossedByRecMuon"].Fill(len(ChambersCrossedByMuon) )

                            ChambersCrossedByGenMuon = tools.Chambers_crossedByGenMuon(tree, genMuIndex)
                            AllSimHitOfTheMuon       = tools.allSimHits_belonging_toGenMuon(tree, genMuIndex)
                            self.sorted_hists1D["nChambers_crossedByGenMuon"].Fill(len(ChambersCrossedByGenMuon) )
                            
                            CleanSimChambers = []
#                            print('ChambersCrossedByGenMuon   ',ChambersCrossedByGenMuon)
                            for chambers_with_gen_muon in ChambersCrossedByGenMuon:
                                if(debug): print('>>>>>>>>>>>>>>>>>>>>>>>>>   loop chambers with muons  <<<<<<<<<<<<<<<<<<<<<<<<< ', chambers_with_gen_muon)
                                allSimHitsInChamber     = tools.all_simhits_in_a_chamber(tree, chambers_with_gen_muon)
                                allMuonSimHitsInChamber = tools.all_muon_simhits_in_a_chamber(tree, chambers_with_gen_muon, genMuIndex )
                                allRecHitsInChamber     = tools.all_rechits_in_a_chamber(tree, chambers_with_gen_muon)
                                allSegmentsInChamber    = tools.allSegments_InChamber(tree, chambers_with_gen_muon)
                                Chamber_station         = tools.Chamber_station(chambers_with_gen_muon)
                                Chamber_ring            = tools.Chamber_ring(chambers_with_gen_muon)

                                ThisChamberStationRing  = int(Chamber_station*10  + Chamber_ring)
                                if(ThisChamberStationRing == 14): continue # Skip Unexisting chamber, dont know what it is
                                ChamberTypePrefix       = 'ME_'+str(ThisChamberStationRing) + '_'
                                HitsSelectionPrefix     = ''


                                
                                if((len(allSimHitsInChamber) >= 3 and len(allMuonSimHitsInChamber) >= 3)): HitsSelectionPrefix = 'Noise_'
                                if((len(allSimHitsInChamber) == len(allMuonSimHitsInChamber) and len(allMuonSimHitsInChamber) >= 3)) : HitsSelectionPrefix = 'Clean_'
                                if(len(allMuonSimHitsInChamber) < 3 ):continue   # Skip if 2 mu simHits in here, who cares
                                if(len(allRecHitsInChamber)     < 3 ):continue   # Skip if less than 3 rechits



                                DifferenceMuonSimRecHits = len(AllSimHitOfTheMuon) - len(AllRecHitOfTheMuon)

                                SkipEvent = False # Here I check that muSimHIts are not in HV spacer
                                for simHit in allMuonSimHitsInChamber:
                                    isNotInHVSpacer = tools.is_y_in_not_dead_zone(tree.simHits_localY[simHit], ChamberTypePrefix[:-1] )
                                    if isNotInHVSpacer == False:
                                        SkipEvent = True
                                        break
                                if SkipEvent == True: continue


                                
                                if(ThisChamberStationRing in Chambers):

                                    ThirdLayerMuonSimHit = -1
                                    for isim in allMuonSimHitsInChamber:
                                        if tree.simHits_ID_layer[isim]  == 3: ThirdLayerMuonSimHit = isim
                                        
                                    MuonSimSegment_localX = tools.SimSegment_localPosition(tree, allMuonSimHitsInChamber).X()
                                    MuonSimSegment_localY = tools.SimSegment_localPosition(tree, allMuonSimHitsInChamber).Y()


                                    
#                                    if(Thir dLayerMuonSimHit !=-1):
#                                        MuonSimSegment_localX = tree.simHits_localX[ThirdLayerMuonSimHit]
#                                        MuonSimSegment_localY = tree.simHits_localY[ThirdLayerMuonSimHit]
#                                    else:
#                                        MuonSimSegment_localX  = ( tree.simHits_localX[allMuonSimHitsInChamber[0]] + tree.simHits_localX[allMuonSimHitsInChamber[-1]] )*0.5
#                                        MuonSimSegment_localY  = ( tree.simHits_localY[allMuonSimHitsInChamber[0]] + tree.simHits_localY[allMuonSimHitsInChamber[-1]] )*0.5



#                                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
 #                                       WireHist  = tools.fill_wire_matrix(tree,allRecHitsInChamber,chambers_with_gen_muon)
 #                                       StripHist = tools.fill_strip_matrix(tree,allRecHitsInChamber,chambers_with_gen_muon)
 #                                       print('Event:  ', int(tree.Event), '  chamber  ', chambers_with_gen_muon)
 #                                       tools.write_th2f(WireHist)
 #                                       tools.write_th2f(StripHist)
 #                                       print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
#                                   if(len(allSegmentsInChamber) == 1):
                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_MuonPt_den'].Fill(GMuLV.Pt())
                                    self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_MuonPt_ToBeRemoved'].Fill(GMuLV.Pt())
                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_MuonEta_den'].Fill(math.fabs(GMuLV.Eta()))
                                    self.sorted_hists1D[ChamberTypePrefix    + HitsSelectionPrefix + "SelectedSegments_Norm"].Fill(  len(allSegmentsInChamber)  )
                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_LocalX_den'].Fill(MuonSimSegment_localX)
                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_LocalY_den'].Fill(MuonSimSegment_localY)
                                    LayerRecHits = tools.RecHitsPerLayer(tree, chambers_with_gen_muon)
                                    for lr in range(0,6):
                                        self.sorted_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'nRecHitsPerLayer_Norm'].Fill(LayerRecHits[lr])
                                        self.sorted_hists2D[ChamberTypePrefix + HitsSelectionPrefix +'nRecHitsPerLayerVsSegments'].Fill(LayerRecHits[lr],len(allSegmentsInChamber))
                                                    

#                                Hist.Draw()
                                    
 #                                   if(len(allSegmentsInChamber) > 1):
#                                        print(' How many segments:  ', len(allSegmentsInChamber))
#                                        for seg in allSegmentsInChamber:
#                                            print('seg # :', seg, ' X / Y: ', tree.cscSegments_localX[seg], '  /  ', tree.cscSegments_localY[seg] )
                                    ClosestSegment = tools.Segment_closest_to_simhit(tree, allMuonSimHitsInChamber, allSegmentsInChamber)
                                    toFill = ClosestSegment
                                    if(ClosestSegment!=-1):toFill=1
                                    self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'ClosestSegment'].Fill(toFill)
                                    
                                    if(ClosestSegment == -1):
                                        print('  SimSegment Local X / Y ', MuonSimSegment_localX, ' / ',MuonSimSegment_localY, '  and N segments  ', len(allSegmentsInChamber))
                                        for segment in allSegmentsInChamber:
                                            print(' X/ Y',  tree.cscSegments_localX[segment], '/ ',tree.cscSegments_localY[segment])
                                            
                                    if( len(allSegmentsInChamber) ==0 ):
                                        print(' when there is no segment:   N Rec Hits: ',len(allRecHitsInChamber), ' mu sim hits  ' ,
                                              len(allMuonSimHitsInChamber), '  all sim hits  ', len(allSimHitsInChamber), '  closest segment ',ClosestSegment )
                                        
                                        for simhit in allSimHitsInChamber:
                                            x = tree.simHits_localX[simhit]
                                            y = tree.simHits_localY[simhit]
                                            if ( math.fabs(tree.simHits_particleType[simhit]) == 13 ):
                                                self.sorted_hists2D[ChamberTypePrefix + 'MuSimHitsLostSegment'].Fill(x, y)
                                                print('  Mu Sim Hits in the lost segment case    ', x,'  \   ', y)
                                        if(len(allRecHitsInChamber) > 200):EventsAndChambersWithZeroRuSegments.write('{}  {}  {}  {}   {}   \n '.format(tree.Event,
                                                                                                                     int(tools.Chamber_endcap(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_station(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_ring(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_chamber(chambers_with_gen_muon))))


                                    if( len(allSegmentsInChamber) ==2 ):
                     #                   print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                     #                   WireHist  = tools.fill_wire_matrix(tree,allRecHitsInChamber,chambers_with_gen_muon)
                     #                   StripHist = tools.fill_strip_matrix(tree,allRecHitsInChamber,chambers_with_gen_muon)
                     #                   print('Event:  ', int(tree.Event), '  chamber  ', chambers_with_gen_muon)
                     #                   tools.write_th2f(WireHist)
                     #                   tools.write_th2f(StripHist)

                                        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                                        EventsAndChambersWithTwoSegments.write('{}  {}  {}  {}   {}   \n '.format(tree.Event,
                                                                                                                     int(tools.Chamber_endcap(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_station(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_ring(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_chamber(chambers_with_gen_muon))))

                                    if( len(allSegmentsInChamber) ==4 ):
                                        EventsAndChambersWithFourSegments.write('{}  {}  {}  {}   {}   \n '.format(tree.Event,
                                                                                                                     int(tools.Chamber_endcap(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_station(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_ring(chambers_with_gen_muon)),
                                                                                                                     int(tools.Chamber_chamber(chambers_with_gen_muon))))

                                    MatchedSegmentWithinResolution = tools.FoundMatchedSegment(tree, allMuonSimHitsInChamber, chambers_with_gen_muon)  # to be worked on
                                    
#                                    print(' pass  ', tools.SegmentWithinResolution(tree, ClosestSegment,  MuonSimSegment_localX, MuonSimSegment_localY, ChamberTypePrefix[:-1] ), '  and is mathced  ', MatchedSegmentWithinResolution)
                                    SegmentISWithinResolution = tools.SegmentWithinResolution(tree, ClosestSegment,  MuonSimSegment_localX, MuonSimSegment_localY, ChamberTypePrefix[:-1] )
#                                    print('MatchedSegmentWithinResolution   ', MatchedSegmentWithinResolution, ' NSegments  ', len(allSegmentsInChamber))
#                                    if MatchedSegmentWithinResolution != -1:

                                    if SegmentISWithinResolution == True:

                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_MuonPt'].Fill(GMuLV.Pt())
                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_MuonEta'].Fill(math.fabs(GMuLV.Eta()))

                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_LocalX'].Fill(MuonSimSegment_localX)
                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_LocalY'].Fill(MuonSimSegment_localY)
                                        
                                        if(ThirdLayerMuonSimHit!=-1):
                                            self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'DeltaThetaSegmentSimHits'].Fill(tree.cscSegments_localTheta[ClosestSegment] - tree.simHits_theta[ThirdLayerMuonSimHit])
                                            self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'DeltaPhiSegmentSimHits'].Fill( tree.cscSegments_localPhi[ClosestSegment] - tree.simHits_phi[ThirdLayerMuonSimHit])



                                    #### Resolution

                                    if(ClosestSegment!=-1):
                                        self.sorted_hists1D[ChamberTypePrefix + HitsSelectionPrefix +"SegmentXResolution"].Fill( tree.cscSegments_localX[ClosestSegment] - MuonSimSegment_localX )
                                        self.sorted_hists1D[ChamberTypePrefix + HitsSelectionPrefix +"SegmentYResolution"].Fill( tree.cscSegments_localY[ClosestSegment] - MuonSimSegment_localY )

                                        
                                        Xpull = (tree.cscSegments_localX[ClosestSegment] - MuonSimSegment_localX) / sqrt(tree.cscSegments_localXerr[ClosestSegment])
                                        Ypull = (tree.cscSegments_localY[ClosestSegment] - MuonSimSegment_localY) / sqrt(tree.cscSegments_localYerr[ClosestSegment])
                                        self.sorted_hists1D[ChamberTypePrefix + HitsSelectionPrefix +"SegmentXResolutionPull"].Fill( Xpull)
                                        self.sorted_hists1D[ChamberTypePrefix + HitsSelectionPrefix +"SegmentYResolutionPull"].Fill( Ypull)
                                        self.sorted_hists2D[ChamberTypePrefix + HitsSelectionPrefix+'ResolutionXY'].Fill(tree.cscSegments_localX[ClosestSegment] - MuonSimSegment_localX ,
                                                                                                                         tree.cscSegments_localY[ClosestSegment] - MuonSimSegment_localY )
                                        self.sorted_hists2D[ChamberTypePrefix + HitsSelectionPrefix+'ResolutionXYPull'].Fill(Xpull,Ypull)
                                        
                                        if(math.fabs ( tree.cscSegments_localX[ClosestSegment] - MuonSimSegment_localX  ) > 1 and math.fabs ( tree.cscSegments_localY[ClosestSegment] - MuonSimSegment_localY  ) > 1 ):
                                            SegmentFarFromSimHits.write('{}  {}  {}  {}   {}   \n '.format(tree.Event,
                                                                                                       int(tools.Chamber_endcap(chambers_with_gen_muon)),
                                                                                                       int(tools.Chamber_station(chambers_with_gen_muon)),
                                                                                                       int(tools.Chamber_ring(chambers_with_gen_muon)),
                                                                                                       int(tools.Chamber_chamber(chambers_with_gen_muon))))


                                        
#
#                                    for i in SegmentThirdLayerSimHit:
#                                        print('  local resol ---> ')
#                                        if tree.simHits_localX[i[1]]  > 0:
#                                            self.sorted_hists1D["SegmentXResolutionPos"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )
#                                            self.sorted_hists1D["SegmentXResolutionPosPull"].Fill( (tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])/sqrt(tree.cscSegments_localXerr[i[0]]) )
#                                        if tree.simHits_localX[i[1]]  < 0:
#                                            self.sorted_hists1D["SegmentXResolutionNeg"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )
#                                            self.sorted_hists1D["SegmentXResolutionNegPull"].Fill( (tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])/sqrt(tree.cscSegments_localXerr[i[0]]) )
#                                        self.sorted_hists1D["SegmentYResolution"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )

#                                        if tree.simHits_localY[i[1]] < -27.5:
#                                           self.sorted_hists1D["SegmentYResolutionBot"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
#                                           self.sorted_hists1D["SegmentYResolutionBotPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )
#                                        if tree.simHits_localY[i[1]] > -27.5 and tree.simHits_localY[i[1]] < 35:
#                                            self.sorted_hists1D["SegmentYResolutionMid"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
#                                            self.sorted_hists1D["SegmentYResolutionMidPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )
#                                        if tree.simHits_localY[i[1]] > 35:
#                                            self.sorted_hists1D["SegmentYResolutionUp"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
#                                            self.sorted_hists1D["SegmentYResolutionUpPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )

#                                        self.sorted_hists1D["SegmentXResolutionPull"].Fill( (tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])/sqrt(tree.cscSegments_localXerr[i[0]]) )
#                                        self.sorted_hists1D["SegmentYResolutionPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]]) )

                                    


    def defineHistos(self):

        EC = ['+','-']
        ST = [1,2,3,4]
        RG = [1,2,3,4]
        LR = [1,2,3,4,5,6]


        #CSC Segments

        self.sorted_hists1D['nChambers_crossedByGenMuon'] = ROOT.TH1F("nChambers_crossedByGenMuon", "; N chambers crossed by gen #mu (simhits)", 11, -0.5, 10.5)
        self.sorted_hists1D['nChambers_crossedByRecMuon'] = ROOT.TH1F("nChambers_crossedByRecMuon", "; N chambers crossed by rec #mu (segment record)", 11, -0.5, 10.5)

        for ring in Chambers:
            ch = 'ME_'+str(int(ring))+'_'
            Range  =  100
            if ring == 11: Range = 80
            if ( ring == 42 or ring == 22 or ring == 32) : Range = 170
            self.sorted_hists2D[ch + 'MuSimHitsLostSegment'] = ROOT.TH2F(ch + 'MuSimHitsLostSegment', "; X, cm; Y cm ", 800, -100, 100, 800 , -Range, Range)
            for sl in range(0,2):
                Selection = 'Noise_'
                if sl == 1:
                    Selection = 'Clean_'
                string = ch + Selection

                    
                ## Efficiency
                self.sorted_hists1D[string+ "SelectedSegments_Norm"]                = ROOT.TH1F(string+'SelectedSegments_Norm', "; N Segments ", 15, -0.5, 14.5)
                self.sorted_hists1D[string+ "ClosestSegment"]                  = ROOT.TH1F(string+'ClosestSegment', "; N Segments ", 3, -1.5, 1.5)
                self.eff_denum_hists1D[string+'SegmentEfficiency_MuonPt_den']  = ROOT.TH1F(string+"SegmentEfficiency_MuonPt_den","; pT (gen #mu) ",30,25,70)
                self.sorted_hists1D[string+'SegmentEfficiency_MuonPt']         = ROOT.TH1F(string+"SegmentEfficiency_MuonPt", "; pT (gen #mu), GeV ",30,25,70)
                self.sorted_hists1D[string+'SegmentEfficiency_MuonPt_ToBeRemoved']         = ROOT.TH1F(string+"SegmentEfficiency_MuonPt_ToBeRemoved", "; pT (gen #mu), GeV ",30,25,70)

                self.sorted_efficiency[string+'SegmentEfficiency_MuonPt']      = ROOT.TEfficiency(string+"SegmentEfficiency_MuonPt","; pT (gen #mu), GeV ",30,25,70)

                self.eff_denum_hists1D[string+'SegmentEfficiency_MuonEta_den'] = ROOT.TH1F(string+"SegmentEfficiency_MuonEta_den","; |#eta| (gen #mu)",30,1.0,2.5)
                self.sorted_hists1D[string+'SegmentEfficiency_MuonEta']        = ROOT.TH1F(string+"SegmentEfficiency_MuonEta", "; |#eta| (gen #mu) ",30,1.0,2.5)
                self.sorted_efficiency[string+'SegmentEfficiency_MuonEta']     = ROOT.TEfficiency(string+"SegmentEfficiency_MuonEta",";  |#eta| (gen #mu) ",30,1.0,2.5)


                self.eff_denum_hists1D[string+'SegmentEfficiency_LocalX_den']  = ROOT.TH1F(string+"SegmentEfficiency_LocalX_den","; Sim muon local Y, cm  ",50,-100,100)
                self.sorted_hists1D[string+'SegmentEfficiency_LocalX']         = ROOT.TH1F(string+"SegmentEfficiency_LocalX","; Sim muon local Y, cm  ",50,-100,100)
                self.sorted_efficiency[string+'SegmentEfficiency_LocalX']      = ROOT.TEfficiency(string+"SegmentEfficiency_LocalX","; Sim muon local X, cm  ",50,-100,100)

                self.eff_denum_hists1D[string+'SegmentEfficiency_LocalY_den']  = ROOT.TH1F(string+"SegmentEfficiency_LocalY_den","; Sim muon local Y, cm  ",50,-100,100)
                self.sorted_hists1D[string+'SegmentEfficiency_LocalY']         = ROOT.TH1F(string+"SegmentEfficiency_LocalY","; Sim muon local Y, cm  ",50,-100,100)
                self.sorted_efficiency[string+'SegmentEfficiency_LocalY']      = ROOT.TEfficiency(string+"SegmentEfficiency_LocalY","; Sim muon local Y, cm  ",50,-100,100)


                # SimHit Resolution 
                
                self.sorted_hists1D[string+'DeltaThetaSegmentSimHits']  = ROOT.TH1F(string+"DeltaThetaSegmentSimHits","; Local #Delta#theta (segment - simhit), rad", 60, -0.5, 0.5)
                self.sorted_hists1D[string+'DeltaPhiSegmentSimHits']    = ROOT.TH1F(string+"DeltaPhiSegmentSimHits","; Local #Delta#phi (segment - simhit), rad", 60, -0.1, 0.1)

                self.sorted_hists1D[string+'SegmentXResolution'] = ROOT.TH1F(string+"SegmentXResolution", "; reco segment resolution X, cm ", 50, -1, 1)
                self.sorted_hists1D[string+'SegmentYResolution'] = ROOT.TH1F(string+"SegmentYResolution", "; reco segment resolution Y, cm ", 50, -5, 5)

                self.sorted_hists1D[string+'SegmentXResolutionPull'] = ROOT.TH1F(string+"SegmentXResolutionPull", "; reco segment resolution #DeltaX/#sigma", 50, -10, 10)
                self.sorted_hists1D[string+'SegmentYResolutionPull'] = ROOT.TH1F(string+"SegmentYResolutionPull", "; reco segment resolution #DeltaY/#sigma", 50, -10, 10)

                ######### TH2F resolution plots
                self.sorted_hists2D[string+'ResolutionXY']               = ROOT.TH2F(string+'ResolutionXY',         "; #DeltaX, cm; #DeltaY cm ", 50, -2, 2, 50 , -2, 2)
                self.sorted_hists2D[string+'ResolutionXYPull']           = ROOT.TH2F(string+'ResolutionXYPull',     "; #DeltaX/#sigma; #DeltaY/#sigma ", 50, -10, 10, 50 , -10, 10)



                ######## ReHitsPerLayer
                self.sorted_hists1D[string + 'nRecHitsPerLayer_Norm']         =  ROOT.TH1F(string+"nRecHitsPerLayer_Norm", "; N rechits per layer ",20,-0.5,19.5)
                self.sorted_hists2D[string + 'nRecHitsPerLayerVsSegments']    = ROOT.TH2F(string+'nRecHitsPerLayerVsSegments',"; N recHits PerLayer; N segments ", 20, -0.5, 19.5, 20 ,-0.5, 19.5)

                
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


        for ring in Chambers:
            ch = 'ME_'+str(int(ring))+'_'
            for sl in range(0,2):
                Selection = 'Clean_'
                if sl == 1:
                    Selection = 'Noise_'
                string = ch + Selection

                self.sorted_efficiency[string+'SegmentEfficiency_MuonPt']  = ROOT.TEfficiency(self.sorted_hists1D[string+'SegmentEfficiency_MuonPt'],
                                                                                              self.eff_denum_hists1D[string+'SegmentEfficiency_MuonPt_den'])
                self.sorted_efficiency[string+'SegmentEfficiency_MuonEta'] = ROOT.TEfficiency(self.sorted_hists1D[string+'SegmentEfficiency_MuonEta'],
                                                                                              self.eff_denum_hists1D[string+'SegmentEfficiency_MuonEta_den'])
                self.sorted_efficiency[string+'SegmentEfficiency_LocalX']  = ROOT.TEfficiency(self.sorted_hists1D[string+'SegmentEfficiency_LocalX'],
                                                                                              self.eff_denum_hists1D[string+'SegmentEfficiency_LocalX_den'])
                self.sorted_efficiency[string+'SegmentEfficiency_LocalY']  = ROOT.TEfficiency(self.sorted_hists1D[string+'SegmentEfficiency_LocalY'] ,
                                                                                              self.eff_denum_hists1D[string+'SegmentEfficiency_LocalY_den'] )



        print('Total number of events processed:  ', self.totalEvents)
        if self.totalEvents > 0:
            if singleFile:
                
                self.writeHistos(self.hists1D,self.hists2D)
#                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D, self.sorted_hists2D, self.sorted_efficiency,"sorted")
            else:
                self.writeHistos(self.hists1D, self.hists2D)
#                self.writeHistosToRoot(self.hists1D,self.hists2D)
                self.writeSortedHistosToRoot(self.sorted_hists1D, self.sorted_hists2D, self.sorted_efficiency,"sorted")
        




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
        raise RuntimeError("opt.file: file name does not end with .root or .txt!")

    print("Begin Analysis")



    # Loop for parallel or single file 
    if singleFile:
        myClass.doAnalysis(opt.file)
    else:
        lines = open(opt.file,"r")
        for line in lines:
            f = line.split()
            if not f[0].endswith(".root"): continue
            if len(f) < 1: continue
            print("Opening file",f[0])
            myClass.doAnalysis(f[0])
            

    myClass.endjob(singleFile)
   
