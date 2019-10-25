##
# these two trees must have same num of entries and structure
##
import ROOT
from tdrStyle import *
setTDRStyle()
import argparse
import logging


def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--input1', dest='input1', type=str, help='input1')
    parser.add_argument('--input2', dest='input2', type=str, help='input2')
#    parser.add_argument('--doME11', dest='doME11', type=bool, help='doME11')
    parser.add_argument('--doME11', dest='doME11', action='store_true', default=False)
    parser.add_argument('--plotdir', dest='plotdir', type=str, help='plotdir')

    args = parser.parse_args()
    return args

#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file,'w')        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def SaveSegIndexs(t, doME11):

    tSegs = []

    for i in range(t.cscSegments_nSegments):
        e = (t.cscSegments_ID_endcap)[i]
        s = (t.cscSegments_ID_station)[i]
        r = (t.cscSegments_ID_ring)[i]     
        c = (t.cscSegments_ID_chamber)[i]

        isME11 = False
        if (s == 1 and (r==1 or r==4)): isME11 = True

        #do ME11
        if (doME11 and (not isME11)): continue
        # do nonME11
        if ((not doME11) and isME11): continue

        index = 10000*e + 1000*s + 100*r + c
        
        if len(tSegs) == 0:
           tmpSegs = [i]
           tSegs.append([index,tmpSegs])

        else:
           thisIndexUsed = False
           for j in range(len(tSegs)): 
               if tSegs[j][0] == index: 
                  tSegs[j][1].append(i)
                  thisIndexUsed = True
                  break

           if not thisIndexUsed:
              tmpSegs = [i]
              tSegs.append([index,tmpSegs])

    return tSegs


def CompareLocalXY(t1,t2,t1Segs,t2Segs,h2,hx,hy):

    segMissed_UF = True
    segMissed_RU = True

# UF algo finds 0 seg
    for i in range(len(t1Segs)):
        segIndex1 = t1Segs[i][0]
        segs1 = t1Segs[i][1]
        for j in range(len(t2Segs)):
            segIndex2 = t2Segs[j][0]
            if t1.Event==t2.Event and (segIndex1 == segIndex2): 
               segMissed_UF = False
               break
        if segMissed_UF :
           e = (t1.cscSegments_ID_endcap)[segs1[0]]
           s = (t1.cscSegments_ID_station)[segs1[0]]
           r = (t1.cscSegments_ID_ring)[segs1[0]]
           c = (t1.cscSegments_ID_chamber)[segs1[0]]
           if s==1 and r==4: r=1
           compareNSeg.Fill(len(segs1),0)
           log1 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)]) 
           logger_1.info(log1)
#           print t1.Event,e,s,r,c,len(segs1)
        segMissed_UF = True

# RU algo finds 0 seg
    for i in range(len(t2Segs)):
        segIndex2 = t2Segs[i][0]
        segs2 = t2Segs[i][1]
        for j in range(len(t1Segs)):
            segIndex1 = t1Segs[j][0]
            if t1.Event==t2.Event and (segIndex1 == segIndex2):
               segMissed_RU = False
               break
        if segMissed_RU:
           e = (t2.cscSegments_ID_endcap)[segs2[0]]
           s = (t2.cscSegments_ID_station)[segs2[0]]
           r = (t2.cscSegments_ID_ring)[segs2[0]]
           c = (t2.cscSegments_ID_chamber)[segs2[0]]
           if s==1 and r==4: r=1
#           print t2.Event,e,s,r,c,len(segs2)
           compareNSeg.Fill(0,len(segs2))
           log2 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
           logger_2.info(log2)
        segMissed_RU = True

# normal loop
    for j in range(len(t1Segs)):
        segIndex1 = t1Segs[j][0]
        segs1 = t1Segs[j][1]

        for k in range(len(t2Segs)):
            segIndex2 = t2Segs[k][0]
            segs2 = t2Segs[k][1]

            if t1.Event==t2.Event and (segIndex1 == segIndex2) :
               compareNSeg.Fill(len(segs1),len(segs2))
#               if t1.Event == t2.Event and (segIndex1 == segIndex2) and len(segs1) == 4 and len(segs2) == 4:
               e = (t2.cscSegments_ID_endcap)[segs2[0]]
               s = (t2.cscSegments_ID_station)[segs2[0]]
               r = (t2.cscSegments_ID_ring)[segs2[0]]
               c = (t2.cscSegments_ID_chamber)[segs2[0]]
               if r == 4: r =1
#               print t1.Event,e,s,r,c

               if len(segs1) == 2 and len(segs2) == 1:
                  log3 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
                  logger_3.info(log3)
               if len(segs1) == 1 and len(segs2) == 2:
                  log4 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
                  logger_4.info(log4)
               if len(segs1) == 4 and len(segs2) == 4:
                  log5 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
                  logger_5.info(log5)

               if t1.Event == t2.Event and (segIndex2 == segIndex1) and len(segs1) == 1 and len(segs2) == 1:
                  x1 = (t1.cscSegments_localX)[segs1[0]]
                  y1 = (t1.cscSegments_localY)[segs1[0]]
                  x2 = (t2.cscSegments_localX)[segs2[0]]
                  y2 = (t2.cscSegments_localY)[segs2[0]]
                  nRH1 = (t1.cscSegments_nRecHits)[segs1[0]]
                  nRH2 = (t2.cscSegments_nRecHits)[segs2[0]]

                  compareNRH.Fill(nRH1,nRH2)

                  if nRH1 == 6 and nRH2 == 6:
                     h2.Fill(x1-x2,y1-y2)
                     hx.Fill(x1-x2)
                     hy.Fill(y1-y2)

                  if nRH1 == 6 and nRH2 == 5:
                     log6 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
                     logger_6.info(log6)
                  if nRH1 == 5 and nRH2 == 6:
                     log7 = ' '.join([str(t1.Event),str(e),str(s),str(r),str(c)])
                     logger_7.info(log7)

#               if abs(y1-y2) > 8: 
#                  print t1.Event,e,s,r,c
#                  print t1.Run,":",t1.Event,x1-x2,y1-y2, segIndex2
#                  print "RU:",x1,y1,(t1.cscSegments_nRecHits)[segs1[0]]
#                  print "UF:",x2,y2,(t2.cscSegments_nRecHits)[segs2[0]]



def DrawHistOnCanvas(hist,option,savename,isLogy=False,isLogx=False):

#    ROOT . gStyle . SetOptStat(1)

    c1 = ROOT.TCanvas("c1","",800,800)
    c1.SetRightMargin(0.15)
#    hist.SetStats(1)
    if isLogy: c1.SetLogy()
    if isLogx: c1.SetLogx()

    print hist.GetName() + " integral: ", hist.Integral()

    hist.SetMarkerSize(2)
    hist.Draw(option)
    c1.SaveAs(savename+".png")
    c1.SaveAs(savename+".pdf")



args=ParseOption()

doME11 = args.doME11
input1 = args.input1
input2 = args.input2
plotdir = args.plotdir

#logger
ME11_tag = 'nonME11'
if doME11: ME11_tag = 'ME11' 

logger_1 = setup_logger('seg_uf_0_ru_1', 'logs/seg_uf_0_ru_1_' + ME11_tag + '.txt')
logger_2 = setup_logger('seg_uf_1_ru_0', 'logs/seg_uf_1_ru_0_' + ME11_tag + '.txt')
logger_3 = setup_logger('seg_uf_1_ru_2', 'logs/seg_uf_1_ru_2_' + ME11_tag + '.txt')
logger_4 = setup_logger('seg_uf_2_ru_1', 'logs/seg_uf_2_ru_1_' + ME11_tag + '.txt')
logger_5 = setup_logger('seg_uf_4_ru_4', 'logs/seg_uf_4_ru_4_' + ME11_tag + '.txt')

logger_6 = setup_logger('rh_uf_5_ru_6', 'logs/rh_uf_5_ru_6_' + ME11_tag + '.txt')
logger_7 = setup_logger('rh_uf_6_ru_5', 'logs/rh_uf_6_ru_5_' + ME11_tag + '.txt')

# define hist
compareLocalXY = ROOT.TH2F("compareLocalXY","",200,-100,100,200,-100,100)
compareLocalX = ROOT.TH1F("compareLocalX","", 100,-1,1)
compareLocalY = ROOT.TH1F("compareLocalY","", 100,-5,5)
compareNSeg = ROOT.TH2F("compareNSeg","",10,0,10,10,0,10)
compareNRH = ROOT.TH2F("compareNRH","",4,3,7,4,3,7)
# could specify chamber type
#filename1 = "DUMMYFILENAME_RU.root"
#filename2 = "DUMMYFILENAME_UF.root"
#filename2 = "DUMMYFILENAME_UF_ST.root"
filename1 = input1
filename2 = input2

treename = "cscRootMaker/Events"

f1_ = ROOT.TFile(filename1)
t1_ = f1_.Get(treename)

f2_ = ROOT.TFile(filename2)
t2_ = f2_.Get(treename)

for i in range(t1_.GetEntries()):

#    if i > 10: break

    t1_.GetEntry(i)
    t2_.GetEntry(i)

    # save segment index first (E_S_R_CH, [i,j,k])
    t1Segs_ = SaveSegIndexs(t1_, doME11)
    t2Segs_ = SaveSegIndexs(t2_, doME11)               

#    if t1_.Event == 438765835:
#     print t1Segs_
#     print t2Segs_

    CompareLocalXY(t1_,t2_,t1Segs_,t2Segs_,compareLocalXY,compareLocalX,compareLocalY)

compareLocalY.GetXaxis().SetTitle("#delta(localY) (cm)")
compareLocalX.GetXaxis().SetTitle("#delta(localX) (cm)")
compareLocalXY.GetXaxis().SetTitle("#delta(localX) (cm)")
compareLocalXY.GetYaxis().SetTitle("#delta(localY) (cm)")
compareNSeg.GetXaxis().SetTitle("nSeg(RU)")
compareNSeg.GetYaxis().SetTitle("nSeg(UF)")
compareNRH.GetXaxis().SetTitle("nRH per segment (RU)")
compareNRH.GetYaxis().SetTitle("nRH per segment (UF)")
compareNRH.GetYaxis().SetNdivisions(105)
compareNRH.GetXaxis().SetNdivisions(105)
compareNSeg.GetXaxis().SetNdivisions(110)
compareNSeg.GetYaxis().SetNdivisions(110)

#savedir = "~/public_html/2017/20171203_cscSeg/ME11/"
#savedir = "~/public_html/2017/20171203_cscSeg/nonME11/"
savedir = plotdir

DrawHistOnCanvas(compareLocalX,"HIST",savedir+compareLocalX.GetName(),True)
DrawHistOnCanvas(compareLocalY,"HIST",savedir+compareLocalY.GetName(),True)
DrawHistOnCanvas(compareLocalXY,"COLZ",savedir+compareLocalXY.GetName())
DrawHistOnCanvas(compareNSeg,"text COLZ",savedir+compareNSeg.GetName())
DrawHistOnCanvas(compareNRH,"text COLZ",savedir+compareNRH.GetName())

