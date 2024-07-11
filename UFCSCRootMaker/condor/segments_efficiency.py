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
                            print('ChambersCrossedByGenMuon   ',ChambersCrossedByGenMuon)
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

                                if((len(allSimHitsInChamber) >= 3 and len(allMuonSimHitsInChamber) >= 3 )): HitsSelectionPrefix = 'Noise_'
                                if((len(allSimHitsInChamber)  ==  len(allMuonSimHitsInChamber)  and  len(allMuonSimHitsInChamber) >= 3)) : HitsSelectionPrefix = 'Clean_'
                                if(len(allMuonSimHitsInChamber) < 3 ):continue   # Skip if 2 mu simHits in here, who cares



                                DifferenceMuonSimRecHits = len(AllSimHitOfTheMuon) - len(AllRecHitOfTheMuon)

                                SkipEvent = False # Here I check that muSimHIts are not in HV spacer
                                for simHit in allMuonSimHitsInChamber:
                                    isNotInHVSpacer = tools.is_y_in_not_dead_zone(tree.simHits_localY[simHit], ChamberTypePrefix[:-1] )
                                    if isNotInHVSpacer == False:
                                        SkipEvent = True
                                        break
                                if SkipEvent == True: continue


                                
                                if(ThisChamberStationRing in Chambers):

                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_MuonPt_den'].Fill(GMuLV.Pt())
                                    self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_MuonEta_den'].Fill(math.fabs(GMuLV.Eta()))
                                    self.sorted_hists1D[ChamberTypePrefix    + HitsSelectionPrefix + "SelectedSegments"].Fill(  len(allSegmentsInChamber)  )


                                    ThirdLayerMuonSimHit = -1
                                    for isim in allMuonSimHitsInChamber:
                                        if tree.simHits_ID_layer[isim]  == 3: ThirdLayerMuonSimHit = isim

                                        
                                    if ThirdLayerMuonSimHit !=-1:
                                        self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix + 'SegmentEfficiency_LocalX_den'].Fill(tree.simHits_localX[ThirdLayerMuonSimHit])
                                        self.eff_denum_hists1D[ChamberTypePrefix + HitsSelectionPrefix +'SegmentEfficiency_LocalY_den'].Fill(tree.simHits_localY[ThirdLayerMuonSimHit])




                                    MatchedSegmentWithinResolution = tools.FoundMatchedSegment(tree, allMuonSimHitsInChamber, chambers_with_gen_muon)  # to be worked on
#                                    print('MatchedSegmentWithinResolution   ', MatchedSegmentWithinResolution, ' NSegments  ', len(allSegmentsInChamber))
                                    if MatchedSegmentWithinResolution != -1:

                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix +  'SegmentEfficiency_MuonPt'].Fill(GMuLV.Pt())
                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_MuonEta'].Fill(math.fabs(GMuLV.Eta()))

                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_LocalX'].Fill(tree.simHits_localX[ThirdLayerMuonSimHit])
                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'SegmentEfficiency_LocalY'].Fill(tree.simHits_localY[ThirdLayerMuonSimHit])

                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'DeltaThetaSegmentSimHits'].Fill(tree.cscSegments_localTheta[MatchedSegmentWithinResolution] -
                                                                                                                                        tree.simHits_theta[ThirdLayerMuonSimHit])
                                        self.sorted_hists1D[ChamberTypePrefix +  HitsSelectionPrefix + 'DeltaPhiSegmentSimHits'].Fill(tree.cscSegments_localPhi[MatchedSegmentWithinResolution]     -
                                                                                                                                      tree.simHits_phi[ThirdLayerMuonSimHit])


#
#                                    for i in SegmentThirdLayerSimHit:


#                                        self.sorted_hists2D['SegmentXResolutionPullVsX'].Fill((tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]])/sqrt(tree.cscSegments_localXerr[i[0]]),tree.simHits_localX[i[1]])
#                                        self.sorted_hists2D['SegmentYResolutionPullVsY'].Fill((tree.cscSegments_localY[i[0]] - tree.simHits_localY[i[1]])/sqrt(tree.cscSegments_localYerr[i[0]]),tree.simHits_localY[i[1]])


                                        
#                                        self.sorted_hists1D["SegmentXResolution"].Fill( tree.cscSegments_localX[i[0]] - tree.simHits_localX[i[1]] )
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
            for sl in range(0,2):
                Selection = 'Noise_'
                if sl == 1:
                    Selection = 'Clean_'
                string = ch + Selection

                    
                ## Efficiency
                self.sorted_hists1D[string+ "SelectedSegments"]                = ROOT.TH1F(string+'SelectedSegments', "; N Segments ", 10, -0.5, 9.5)
                self.eff_denum_hists1D[string+'SegmentEfficiency_MuonPt_den']  = ROOT.TH1F(string+"SegmentEfficiency_MuonPt_den","; pT (gen #mu) ",30,25,70)
                self.sorted_hists1D[string+'SegmentEfficiency_MuonPt']         = ROOT.TH1F(string+"SegmentEfficiency_MuonPt", "; pT (gen #mu), GeV ",30,25,70)
                self.sorted_efficiency[string+'SegmentEfficiency_MuonPt']      = ROOT.TEfficiency(string+"SegmentEfficiency_MuonPt","; pT (gen #mu), GeV ",30,25,70)

                self.eff_denum_hists1D[string+'SegmentEfficiency_MuonEta_den'] = ROOT.TH1F(string+"SegmentEfficiency_MuonEta_den","; |#eta| (gen #mu)",30,1.0,2.5)
                self.sorted_hists1D[string+'SegmentEfficiency_MuonEta']        = ROOT.TH1F(string+"SegmentEfficiency_MuonEta", "; |#eta| (gen #mu) ",30,1.0,2.5)
                self.sorted_efficiency[string+'SegmentEfficiency_MuonEta']     = ROOT.TEfficiency(string+"SegmentEfficiency_MuonEta",";  |#eta| (gen #mu) ",30,1.0,2.5)


                self.eff_denum_hists1D[string+'SegmentEfficiency_LocalX_den']  = ROOT.TH1F(string+"SegmentEfficiency_LocalX_den","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)
                self.sorted_hists1D[string+'SegmentEfficiency_LocalX']         = ROOT.TH1F(string+"SegmentEfficiency_LocalX","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)
                self.sorted_efficiency[string+'SegmentEfficiency_LocalX']      = ROOT.TEfficiency(string+"SegmentEfficiency_LocalX","; Muon SimHit (3rd Layer) X, cm  ",50,-100,100)

                self.eff_denum_hists1D[string+'SegmentEfficiency_LocalY_den']  = ROOT.TH1F(string+"SegmentEfficiency_LocalY_den","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)
                self.sorted_hists1D[string+'SegmentEfficiency_LocalY']         = ROOT.TH1F(string+"SegmentEfficiency_LocalY","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)
                self.sorted_efficiency[string+'SegmentEfficiency_LocalY']      = ROOT.TEfficiency(string+"SegmentEfficiency_LocalY","; Muon SimHit (3rd Layer) Y, cm  ",50,-100,100)


                # SimHit Resolution 
                
                self.sorted_hists1D[string+'DeltaThetaSegmentSimHits']  = ROOT.TH1F(string+"DeltaThetaSegmentSimHits","; Local #Delta#theta (segment - simhit), rad", 60, -0.5, 0.5)
                self.sorted_hists1D[string+'DeltaPhiSegmentSimHits']    = ROOT.TH1F(string+"DeltaPhiSegmentSimHits","; Local #Delta#phi (segment - simhit), rad", 60, -0.1, 0.1)




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
