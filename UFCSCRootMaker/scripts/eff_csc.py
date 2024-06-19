#!/usr/bin/env python


import sys, os, pwd, commands
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
    global opt, args, debug
    (opt, args) = parser.parse_args()
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

                            for chambers_with_gen_muon in ChambersCrossedByGenMuon:
                                if(debug):print('>>>>>>>>>>>>>>>>>>>>>>>>>   loop chambers with muons  <<<<<<<<<<<<<<<<<<<<<<<<< ')
                                allSimHitsInChamber     = tools.all_simhits_in_a_chamber(tree, chambers_with_gen_muon)
                                allMuonSimHitsInChamber = tools.all_muon_simhits_in_a_chamber(tree, chambers_with_gen_muon, genMuIndex )
                                allRecHitsInChamber     = tools.all_rechits_in_a_chamber(tree, chambers_with_gen_muon)
                                allSegmentsInChamber    = tools.allSegments_InChamber(tree, chambers_with_gen_muon)
                                Chamber_station         = tools.Chamber_station(chambers_with_gen_muon)
                                Chamber_ring            = tools.Chamber_ring(chambers_with_gen_muon)


                                if(opt.ME11 == 0 and ( Chamber_station ==1 and Chamber_ring == 1) ): continue  # non ME11
                                if(opt.ME21 == 1 and ( Chamber_station !=2 or Chamber_ring  != 1) ): continue  # selecti either ME21 or all except ME11


                                DifferenceMuonSimRecHits = len(AllSimHitOfTheMuon) - len(AllRecHitOfTheMuon)
#                                AllSegmentsOfSelectedMuon =  tools.allSegments_belonging_toMuon(tree, recoMuIndex)


                                HitsSelection = True
                                if(opt.condition == 0 ): HitsSelection = (len(allSimHitsInChamber) >= 3 and len(allMuonSimHitsInChamber) >= 3 ) # at least tree muon simhits
                                if(opt.condition == 1 ): HitsSelection = (len(allSimHitsInChamber)  ==  len(allMuonSimHitsInChamber)  and  len(allMuonSimHitsInChamber) >= 3)


                                if ( HitsSelection ):  # here clean or noise


                                    self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'].Fill(GMuLV.Pt())
                                    self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'].Fill(math.fabs(GMuLV.Eta()))


                                    self.sorted_hists1D["SelectedSegments"].Fill(  len(allSegmentsInChamber)  )

                                    SegmentThirdLayerSimHit = []
                                    for isegment in allSegmentsInChamber:

                                        AllRecHitsOfSegment = tools.allRechits_of_segment(tree, isegment)
                                        if(debug):print("  segment local X/Y  ", tree.cscSegments_localX[isegment], " /  ", tree.cscSegments_localY[isegment])
                                        for irec in AllRecHitsOfSegment:
                                        
                                            ClosestSimHit =  tools.RecHit_closest_SimHit(tree, irec, allMuonSimHitsInChamber)
                                            if(tree.simHits_ID_layer[ClosestSimHit] == 3): 
                                                SegmentThirdLayerSimHit.append([isegment,ClosestSimHit])
                                                if(debug):print("rechit:  ",  irec, "  X/Y  ", tree.recHits2D_localX[irec], " / ", 
                                                                tree.recHits2D_localY[irec], ' layer:  ', tree.recHits2D_ID_layer[irec])
                                                if(debug):print("Closest Sim :  ",  "  X/Y  ", tree.simHits_localX[ClosestSimHit], " / ", 
                                                                tree.simHits_localY[ClosestSimHit], ' layer:  ', tree.simHits_ID_layer[ClosestSimHit])

                                                self.sorted_hists1D["RecHitResolutionX3rdLayer"].Fill( tree.recHits2D_localX[irec] - tree.simHits_localX[ClosestSimHit] )
                                                self.sorted_hists1D["RecHitResolutionY3rdLayer"].Fill( tree.recHits2D_localY[irec] - tree.simHits_localY[ClosestSimHit] )

                                                self.sorted_hists1D["RecHitSegmentX3rdLayer"].Fill( tree.recHits2D_localX[irec] - tree.cscSegments_localX[isegment] )
                                                self.sorted_hists1D["RecHitSegmentY3rdLayer"].Fill( tree.recHits2D_localY[irec] - tree.cscSegments_localY[isegment] )

                                    ThirdLayerMuonSimHit = -1
                                    if(debug):print(" All MuSimHits in chamber   ", len(allMuonSimHitsInChamber))
                                    for isim in allMuonSimHitsInChamber:
                                        if tree.simHits_ID_layer[isim]  == 3: ThirdLayerMuonSimHit = isim

                                    if ThirdLayerMuonSimHit !=-1:
                                        self.eff_denum_hists1D['SegmentEfficiency_LocalX_den'].Fill(tree.simHits_localX[ThirdLayerMuonSimHit])
                                        self.eff_denum_hists1D['SegmentEfficiency_LocalY_den'].Fill(tree.simHits_localY[ThirdLayerMuonSimHit])
#                                        print('simhit:   ', isim, "  layer  ", tree.simHits_ID_layer[isim]  ,' simhit local X/Y  ', tree.simHits_localX[isim], ' / ', tree.simHits_localY[isim])
#                                    if( not  ThirdLayer  ) : print("no sim hit in the third Layer !!!!!!!!!!!")
#                                    print("segment  third layer hit ", SegmentThirdLayerSimHit)



                                    MatchedSegmentWithinResolution = tools.FoundMatchedSegment(tree, allMuonSimHitsInChamber, chambers_with_gen_muon)
                                    if MatchedSegmentWithinResolution != -1:

                                        self.sorted_hists1D['SegmentEfficiency_MuonPt'].Fill(GMuLV.Pt())
                                        self.sorted_hists1D['SegmentEfficiency_MuonEta'].Fill(math.fabs(GMuLV.Eta()))

                                        self.sorted_hists1D['SegmentEfficiency_LocalX'].Fill(tree.simHits_localX[ThirdLayerMuonSimHit])
                                        self.sorted_hists1D['SegmentEfficiency_LocalY'].Fill(tree.simHits_localY[ThirdLayerMuonSimHit])


                                        self.sorted_hists1D['DeltaThetaSegmentSimHits'].Fill(tree.cscSegments_localTheta[MatchedSegmentWithinResolution] - tree.simHits_theta[ThirdLayerMuonSimHit])
                                        self.sorted_hists1D['DeltaPhiSegmentSimHits'].Fill(tree.cscSegments_localPhi[MatchedSegmentWithinResolution]     - tree.simHits_phi[ThirdLayerMuonSimHit])


                                        if(debug):print('------------------------------- ', ThirdLayerMuonSimHit)
                                        if(debug):print("matched segment  X/Y   ", tree.cscSegments_localX[MatchedSegmentWithinResolution],' / ', 
                                                        tree.cscSegments_localY[MatchedSegmentWithinResolution], ' 3rd layer sim Hit   ', 
                                                        tree.simHits_localX[ThirdLayerMuonSimHit], '  /  ', tree.simHits_localY[ThirdLayerMuonSimHit])
                                              


                                    for i in SegmentThirdLayerSimHit:

#                                        print("resolution X  ", tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])
#                                        print("resolution Y  ", tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])

                                        self.sorted_hists1D["SegmentXResolution"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )

                                        if tree.simHits_localX[i[1]]  > 0:
                                            self.sorted_hists1D["SegmentXResolutionPos"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )
                                        if tree.simHits_localX[i[1]]  < 0:
                                            self.sorted_hists1D["SegmentXResolutionNeg"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )

                                        self.sorted_hists1D["SegmentYResolution"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )

                                        if tree.simHits_localY[i[1]] < -30:
                                           self.sorted_hists1D["SegmentYResolutionBot"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
                                           self.sorted_hists1D["SegmentYResolutionBotPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )
                                        if tree.simHits_localY[i[1]] > -30 and tree.simHits_localY[i[1]] < 30:
                                            self.sorted_hists1D["SegmentYResolutionMid"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
                                            self.sorted_hists1D["SegmentYResolutionMidPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )
                                        if tree.simHits_localY[i[1]] > 30:
                                            self.sorted_hists1D["SegmentYResolutionUp"].Fill( tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]] )
                                            self.sorted_hists1D["SegmentYResolutionUpPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]])  )

                                        self.sorted_hists1D["SegmentXResolutionPull"].Fill( (tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])/sqrt(tree.cscSegments_localXerr[i[0]]) )
                                        self.sorted_hists1D["SegmentYResolutionPull"].Fill( (tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]]) )

                                    

                                    for simhit in allSimHitsInChamber:
                                        self.sorted_hists2D['XYSimHitsInChamber'].Fill(tree.simHits_localX[simhit],tree.simHits_localY[simhit])

                                    for rechit in allRecHitsInChamber:
                                        self.sorted_hists2D['XYRecHitsInChamber'].Fill(tree.recHits2D_localX[rechit], tree.recHits2D_localY[rechit])




    def defineHistos(self):

        EC = ['+','-']
        ST = [1,2,3,4]
        RG = [1,2,3,4]
        LR = [1,2,3,4,5,6]


        #CSC Segments

        self.sorted_hists1D['nChambers_crossedByGenMuon'] = ROOT.TH1F("nChambers_crossedByGenMuon", "; N chambers crossed by gen #mu (simhits)", 11, -0.5, 10.5)
        self.sorted_hists1D['nChambers_crossedByRecMuon'] = ROOT.TH1F("nChambers_crossedByRecMuon", "; N chambers crossed by rec #mu (segment record)", 11, -0.5, 10.5)
        self.sorted_hists1D['SegmentXResolution'] = ROOT.TH1F("SegmentXResolution", "; reco Segment resolution X, cm ", 50, -0.5, 0.5)
        self.sorted_hists1D['SegmentXResolutionPos'] = ROOT.TH1F("SegmentXResolutionPos", "; reco Segment resolution X, cm ", 50, -0.5, 0.5)
        self.sorted_hists1D['SegmentXResolutionNeg'] = ROOT.TH1F("SegmentXResolutionNeg", "; reco Segment resolution X, cm ", 50, -0.5, 0.5)
        self.sorted_hists1D['SegmentYResolution'] = ROOT.TH1F("SegmentYResolution", "; reco Segment resolution Y, cm ", 50, -1.5, 1.5)

        self.sorted_hists1D['SegmentYResolutionBot'] = ROOT.TH1F("SegmentYResolutionBot", "; reco Segment resolution Y, cm ", 50, -1.5, 1.5)
        self.sorted_hists1D['SegmentYResolutionMid'] = ROOT.TH1F("SegmentYResolutionMid", "; reco Segment resolution Y, cm ", 50, -1.5, 1.5)
        self.sorted_hists1D['SegmentYResolutionUp'] = ROOT.TH1F("SegmentYResolutionUp", "; reco Segment resolution Y, cm ", 50, -1.5, 1.5)

        self.sorted_hists1D['SegmentXResolutionPull'] = ROOT.TH1F("SegmentXResolutionPull", "; reco Segment resolution X, pull ", 50, -10.0, 10.0)
        self.sorted_hists1D['SegmentYResolutionPull'] = ROOT.TH1F("SegmentYResolutionPull", "; reco Segment resolution Y, pull ", 50, -10.0, 10.0)


        self.sorted_hists1D['SegmentYResolutionBotPull'] = ROOT.TH1F("SegmentYResolutionBotPull", "; reco Segment resolution Y, pull ", 50, -10.0, 10.0)
        self.sorted_hists1D['SegmentYResolutionMidPull'] = ROOT.TH1F("SegmentYResolutionMidPull", "; reco Segment resolution Y, pull ", 50, -10.0, 10.0)
        self.sorted_hists1D['SegmentYResolutionUpPull'] = ROOT.TH1F("SegmentYResolutionUpPull", "; reco Segment resolution Y, pull ", 50, -10.0, 10.0)


        self.sorted_hists2D['XYSimHitsInChamber'] = ROOT.TH2F('XYSimHitsInChamber', "; X, cm; Y cm ", 50, -100, 100, 50 , -100, 100) 
        self.sorted_hists2D['XYRecHitsInChamber'] = ROOT.TH2F('XYRecHitsInChamber', "; X, cm; Y cm ", 50, -100, 100, 50 , -100, 100) 


        self.sorted_hists1D['RecHitResolutionX3rdLayer'] = ROOT.TH1F('RecHitResolutionX3rdLayer', "; X RecHit resolution 3rd layer, cm ", 50, -1.5, 1.5)
        self.sorted_hists1D['RecHitResolutionY3rdLayer'] = ROOT.TH1F('RecHitResolutionY3rdLayer', "; Y RecHit resolution 3rd layer, cm ", 50, -1.5, 1.5)

        self.sorted_hists1D["RecHitSegmentX3rdLayer"] = ROOT.TH1F('RecHitSegmentX3rdLayer', "; RecHit 3rd layer X  - Segment local X, cm ", 50, -1.5, 1.5)
        self.sorted_hists1D["RecHitSegmentY3rdLayer"] = ROOT.TH1F('RecHitSegmentY3rdLayer', "; RecHit 3rd layer Y  - Segment local Y, cm ", 50, -1.5, 1.5)



        self.sorted_hists1D["SelectedSegments"] = ROOT.TH1F('SelectedSegments', "; N Segments ", 5, -0.5, 4.5)




        ## Efficiency 
        self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'] = ROOT.TH1F("SegmentEfficiency_MuonPt_den","; pT (gen #mu) ",30,25,70)
        self.sorted_hists1D['SegmentEfficiency_MuonPt']        = ROOT.TH1F("SegmentEfficiency_MuonPt", "; pT (gen #mu), GeV ",30,25,70)
        self.sorted_efficiency['SegmentEfficiency_MuonPt']     = ROOT.TEfficiency("SegmentEfficiency_MuonPt","; pT (gen #mu), GeV ",30,25,70)

        self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'] = ROOT.TH1F("SegmentEfficiency_MuonEta_den","; |#eta| (gen #mu)",30,1.0,2.5)
        self.sorted_hists1D['SegmentEfficiency_MuonEta']        = ROOT.TH1F("SegmentEfficiency_MuonEta", "; |#eta| (gen #mu) ",30,1.0,2.5)
        self.sorted_efficiency['SegmentEfficiency_MuonEta']     = ROOT.TEfficiency("SegmentEfficiency_MuonEta",";  |#eta| (gen #mu) ",30,1.0,2.5)


        self.eff_denum_hists1D['SegmentEfficiency_LocalX_den']  = ROOT.TH1F("SegmentEfficiency_LocalX_den","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)
        self.sorted_hists1D['SegmentEfficiency_LocalX']     = ROOT.TH1F("SegmentEfficiency_LocalX","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)
        self.sorted_efficiency['SegmentEfficiency_LocalX']  = ROOT.TEfficiency("SegmentEfficiency_LocalX","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)

        self.eff_denum_hists1D['SegmentEfficiency_LocalY_den']  = ROOT.TH1F("SegmentEfficiency_LocalY_den","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)
        self.sorted_hists1D['SegmentEfficiency_LocalY']     = ROOT.TH1F("SegmentEfficiency_LocalY","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)
        self.sorted_efficiency['SegmentEfficiency_LocalY']  = ROOT.TEfficiency("SegmentEfficiency_LocalY","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)








        # SimHit Resolution 

        self.sorted_hists1D['DeltaThetaSegmentSimHits']  = ROOT.TH1F("DeltaThetaSegmentSimHits","; Local #Delta#theta (segment - simhit), rad", 60, -0.5, 0.5)
        self.sorted_hists1D['DeltaPhiSegmentSimHits']    = ROOT.TH1F("DeltaPhiSegmentSimHits","; Local #Delta#phi (segment - simhit), rad", 60, -0.1, 0.1)




#        self.sorted_hists1D['']


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


        self.sorted_efficiency['SegmentEfficiency_MuonPt'] = ROOT.TEfficiency(SegmentEfficiency_MuonPt,SegmentEfficiency_MuonPt_den)
        self.sorted_hists1D['SegmentEfficiency_MuonPt'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_MuonPt'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonPt_den'])

        self.sorted_efficiency['SegmentEfficiency_MuonEta'] = ROOT.TEfficiency(SegmentEfficiency_MuonEta,SegmentEfficiency_MuonEta_den)
        self.sorted_hists1D['SegmentEfficiency_MuonEta'].Sumw2()
        self.sorted_hists1D['SegmentEfficiency_MuonEta'].Divide(self.eff_denum_hists1D['SegmentEfficiency_MuonEta_den'])


        self.sorted_efficiency['SegmentEfficiency_LocalX']  = ROOT.TEfficiency(SegmentEfficiency_LocalX,SegmentEfficiency_LocalX_den)
        self.sorted_efficiency['SegmentEfficiency_LocalY']  = ROOT.TEfficiency(SegmentEfficiency_LocalY,SegmentEfficiency_LocalY_den)




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
