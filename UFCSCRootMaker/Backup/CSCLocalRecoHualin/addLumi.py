#from ROOT import *
import ROOT
from array import array
import subprocess
import argparse
import sys


def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--inputname', dest='inputname', type=str, help='inputname')
    parser.add_argument('--era', dest='era', type=str, help='era')

    args = parser.parse_args()
    return args

args=ParseOption()
filename = args.inputname
era = args.era

print "root://cmsio2.rc.ufl.edu//store/user/t2/users/mhl/rootfiles_2017/" + filename
#sys.exit()

f = ROOT.TFile.Open("root://cmsio2.rc.ufl.edu//store/user/t2/users/mhl/rootfiles_2017/" + filename,"update")

t = f.Get("cscRootMaker/Events")

instLumi = array('d', [0])
bLumi = t.Branch("instLumi",instLumi,"instLumi/D")

for i in range(t.GetEntries()):

    t.GetEntry(i)

    run = t.Run
    ls = t.LumiSect

    command = " grep \"" + str(run) + ":\" sortLumi/test_ls_sort_" + era + ".csv | grep \"," + str(ls) + ":\" | awk -F \",\" '{print $6}' "
    
    tmpLumi = (subprocess.Popen(command,stdout=subprocess.PIPE,shell=True) ).communicate()[0]

#    print run, ls, tmpLumi
    instLumi[0] = float(tmpLumi)/24.0

    bLumi.Fill()

t.Write()
