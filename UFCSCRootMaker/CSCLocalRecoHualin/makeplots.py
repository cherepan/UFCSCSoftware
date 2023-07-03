import ROOT
import lib.plotter
import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--t1', dest='tag1', type=str, help='for each plot',default = 'UF')
    parser.add_argument('--t2', dest='tag2', type=str, help='for each plot',default = 're')
    parser.add_argument('--inputfile1', dest='inputfile1', type=str, help='inputfile1')
    parser.add_argument('--inputfile2', dest='inputfile2', type=str, help='inputfile2')
    parser.add_argument('--plotdir', dest='plotdir', type=str, help='plotdir')

    args = parser.parse_args()
    return args

args=ParseOption()
inputfile1 = args.inputfile1
inputfile2 = args.inputfile2
tag1 = args.tag1
tag2 = args.tag2
plotdir = args.plotdir


#histnames = ["nSegPerChamebr","nRHPerSeg","chi2PerDOF","nSegmentsPerChamber","nSegmentsPerMuonChamber"]
histnames = ["nChambers_crossedbyMuon","nSegmentsPerMuonChamber","TwoMuons_mass","TwoMuons_mass_wide","nSegmentsPerMuonChamber_notBelongingToMuon","nSegmentsPerChamber","nRHPerSeg","nRHPerNonMuonSegment","nMuon_perEvent"]
xmins = [0,0,60,60,-0.5,0,0,0,0]
xmaxs = [6,5,120,120,6,6,7,7,5]
ymins = [0,1,0,0,0,0,0,0,0]
#ymaxs = [10000,10000,10000,10000]

#ymaxs = [1000,5000,5000,300,5000,40000,1500,200,5000]

ymaxs = [100,500,500,30,500,4000,500,100,1000]

xtitles = ["# chambers crossed by Muon","# segments per chamber with muon","M, GeV","M, GeV","# non muon segments","# segments per chamber","# RH per muon segment","# RH per non muon segment","# muons per event"]

for i in range(len(histnames)):

    plotter = lib.plotter.Plotter()

    histname = histnames[i]

#    plotter.GetHistFromRoot("tmpRootPlots/CSCresults_RU.root",histname,'RU')
#    plotter.GetHistFromRoot("tmpRootPlots/CSCresults_UF_ST.root",histname,'UF')
    plotter.GetHistFromRoot(inputfile1, histname, tag1)
    plotter.GetHistFromRoot(inputfile2, histname, tag2)

    drawOps = ["HIST","HIST"]
    colors = [3,4]
    styles = [1,1]
    sizes = [2,2]

    tmpHists = [histname+'_RU',histname+'_UF']

    plotter.AddPlot(tmpHists, drawOps, colors, styles, sizes)

    comments = ["RU","UF "]

    canvasCord = [xmins[i],xmaxs[i],ymins[i],ymaxs[i]]  
    legendCord = [0.4,0.75,0.9,0.9]
    titles = [xtitles[i],'']

#    savename = "/home/mhl/public_html/2017/20171203_cscSeg/ME11/" + histname
#    savename = "/home/mhl/public_html/2017/20171203_cscSeg/nonME11/" + histname
    savename = plotdir + histname

    if i == 2:
       plotter.Plot(tmpHists,canvasCord,legendCord,titles,comments,drawOps,savename,True) # log
    else:
       plotter.Plot(tmpHists,canvasCord,legendCord,titles,comments,drawOps,savename)

