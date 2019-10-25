import ROOT
import lib.plotter
import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--t1', dest='tag1', type=str, help='for each plot')
    parser.add_argument('--t2', dest='tag2', type=str, help='for each plot')
    parser.add_argument('--plotfile1', dest='plotfile1', type=str, help='plotfile1')
    parser.add_argument('--plotfile2', dest='plotfile2', type=str, help='plotfile2')
    parser.add_argument('--plotdir', dest='plotdir', type=str, help='plotdir')

    args = parser.parse_args()
    return args

args=ParseOption()
plotfile1 = args.plotfile1
plotfile2 = args.plotfile2
tag1 = args.tag1
tag2 = args.tag2
plotdir = args.plotdir

histnames = ["nSegPerChamebr","nRHPerSeg","chi2PerDOF"]
xmins = [0,0,0]
xmaxs = [10,7,100]
ymins = [0.1,0.1,0.1]
#ymaxs = [10000,10000,10000,10000]
ymaxs = [5000,5000,6000]
xtitles = ["nSegPerChamber","nRHPerSeg","chi2/DOF"]

for i in range(len(histnames)):

    plotter = lib.plotter.Plotter()

    histname = histnames[i]

#    plotter.GetHistFromRoot("tmpRootPlots/CSCresults_RU.root",histname,'RU')
#    plotter.GetHistFromRoot("tmpRootPlots/CSCresults_UF_ST.root",histname,'UF')
    plotter.GetHistFromRoot(plotfile1,histname,tag1)
    plotter.GetHistFromRoot(plotfile2,histname,tag2)

    drawOps = ["HIST","HIST"]
    colors = [1,2]
    styles = [1,1]
    sizes = [2,2]

    tmpHists = [histname+'_RU',histname+'_UF']

    plotter.AddPlot(tmpHists,drawOps, colors, styles, sizes)

    comments = ["RU algo","UF algo"]

    canvasCord = [xmins[i],xmaxs[i],ymins[i],ymaxs[i]]  
    legendCord = [0.7,0.75,0.9,0.9]
    titles = [xtitles[i],'']

#    savename = "/home/mhl/public_html/2017/20171203_cscSeg/ME11/" + histname
#    savename = "/home/mhl/public_html/2017/20171203_cscSeg/nonME11/" + histname
    savename = plotdir + histname

    if i == 2:
       plotter.Plot(tmpHists,canvasCord,legendCord,titles,comments,drawOps,savename,True) # log
    else:
       plotter.Plot(tmpHists,canvasCord,legendCord,titles,comments,drawOps,savename)

