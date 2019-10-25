import ROOT
from tdrStyle import *
setTDRStyle()
import sys

class Plotter():

      def __init__(self):

          self.hist1D = ROOT.RooWorkspace("h1d")  # save all hists
          self.hist2D = []
#          self.c1 = ROOT.TCanvas("c1","",800,800)

      def GetHistFromRoot(self,filename,histname,tag):

          file_ = ROOT.TFile(filename)
          tmpHist = file_.Get(histname)
          getattr(self.hist1D, 'import')(tmpHist,histname+'_'+tag)


      def AddPlot(self, histnames, drawOps, colors, styles, sizes, do1D=True):    

          for i in range(len(histnames)):

              drawOp = drawOps[i]
              color = colors[i]
              style = styles[i]
              size = sizes[i]

              if "HIST" in drawOp:

                 self.hist1D.obj(histnames[i]).SetLineColor(color)
                 self.hist1D.obj(histnames[i]).SetLineStyle(style)
                 self.hist1D.obj(histnames[i]).SetLineWidth(size)

              if "p" in drawOp:
                 self.hist1D.obj(histnames[i]).SetMarkerColor(color)
                 self.hist1D.obj(histnames[i]).SetMarkerStyle(style)
                 self.hist1D.obj(histnames[i]).SetMarkerSize(size)
              

      def Plot(self,histnames,canvasCord,legendCord,titles,comments,drawOps,savename,isLog=False):

          c1 = ROOT.TCanvas("c1","",800,800)
          dummy = ROOT.TH1D("dummy","dummy",1,canvasCord[0],canvasCord[1])
          if isLog: c1.SetLogy()
          dummy.SetMinimum(canvasCord[2])
          dummy.SetMaximum(canvasCord[3])
          dummy.SetLineColor(0)
          dummy.SetMarkerColor(0)
          dummy.SetLineWidth(0)
          dummy.SetMarkerSize(0)
          dummy.GetYaxis().SetTitle(titles[1])
          dummy.GetYaxis().SetTitleOffset(1.3)
          dummy.GetXaxis().SetTitle(titles[0])
          dummy.Draw()

          legend = ROOT.TLegend(legendCord[0],legendCord[1],legendCord[2],legendCord[3])

          for i in range(len(histnames)):
              self.hist1D.obj(histnames[i]).Draw('same ' + drawOps[i])
              legend.AddEntry(self.hist1D.obj(histnames[i]),comments[i])#,drawOps[i])

          legend.SetTextSize(0.03)
          legend.SetLineWidth(1)
          legend.SetFillColor(0)
          legend.SetBorderSize(1)
          legend.Draw("same")

          c1.SaveAs(savename+".png")
          c1.SaveAs(savename+".pdf")

