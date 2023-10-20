import ROOT

f = ROOT.TFile.Open("root://cmsio2.rc.ufl.edu//store/user/t2/users/mhl/rootfiles_2017/SingleMuon_Run2017C-ZMu-12Sep2017-v1_3.root")
t = f.Get("cscRootMaker/Events")
print t.GetEntries()
