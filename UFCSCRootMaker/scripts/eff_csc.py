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
                                print(' loop chambers with muons  ')
                                allSimHitsInChamber     = tools.all_simhits_in_a_chamber(tree, chambers_with_gen_muon)
                                allMuonSimHitsInChamber = tools.all_muon_simhits_in_a_chamber(tree, chambers_with_gen_muon, genMuIndex )
                                allRecHitsInChamber     = tools.all_rechits_in_a_chamber(tree, chambers_with_gen_muon)
                                allSegmentsInChamber    = tools.allSegments_InChamber(tree, chambers_with_gen_muon)
                                Chamber_station         = tools.Chamber_station(chambers_with_gen_muon)
                                Chamber_ring            = tools.Chamber_ring(chambers_with_gen_muon)


                                if(opt.ME11 == 0 and ( Chamber_station ==1 and Chamber_ring == 1) ): continue  # non ME11
                                if(opt.ME21 == 1 and ( Chamber_station !=2 or Chamber_ring  != 1) ): continue  # selecti either ME21 or all except ME11


                            DifferenceMuonSimRecHits = len(AllSimHitOfTheMuon) - len(AllRecHitOfTheMuon)
                            AllSegmentsOfSelectedMuon =  tools.allSegments_belonging_toMuon(tree, recoMuIndex)


                            HitsSelection = True

                            
                            if(opt.condition == 0 ): HitsSelection = (len(allSimHitsInChamber) >= 3 and len(allMuonSimHitsInChamber) >= 3 ) # at least tree muon simhits
                            if(opt.condition == 1 ): HitsSelection = (len(allSimHitsInChamber)  ==  len(allMuonSimHitsInChamber)  and  len(allMuonSimHitsInChamber) >= 3)


                            if ( HitsSelection ):
                                print(" AllSegmentsOfSelectedMuon  ", len(AllSegmentsOfSelectedMuon))
                                for isegment in AllSegmentsOfSelectedMuon:
                                    print('all  recihits of reco segment: ', tools.allRechits_of_segment(tree,isegment), ' Segment Local X/Y  ', tree.cscSegments_localX[isegment], '/', tree.cscSegments_localY[isegment], ' rechit strip position  ')
                                    AllRecHitsOfSegment = tools.allRechits_of_segment(tree, isegment)
                                    for irec in AllRecHitsOfSegment:
                                        print(" recHit local X/Y  ", tree.recHits2D_localX[irec], '/', tree.recHits2D_localY[irec], '  closest simHit X/Y ', tree.recHits2D_simHit_localX[irec], 'Y', tree.recHits2D_simHit_localY[irec])
                                    
                                print(" All MuSimHits in chamber   ", len(allMuonSimHitsInChamber))
                                for isim in allMuonSimHitsInChamber:
                                    print(' simhit local X/Y  ', tree.simHits_localX[isim], ' / ', tree.simHits_localY[isim])
                                










    def defineHistos(self):

        EC = ['+','-']
        ST = [1,2,3,4]
        RG = [1,2,3,4]
        LR = [1,2,3,4,5,6]


        #CSC Segments

        self.sorted_hists1D['nChambers_crossedByGenMuon'] = ROOT.TH1F("nChambers_crossedByGenMuon", "; N chambers crossed by gen #mu (simhits)", 11, -0.5, 10.5)
        self.sorted_hists1D['nChambers_crossedByRecMuon'] = ROOT.TH1F("nChambers_crossedByRecMuon", "; N chambers crossed by rec #mu (segment record)", 11, -0.5, 10.5)



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
