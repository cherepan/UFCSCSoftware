#! /bin/bash
echo 'Starting Job' 
ls -lt /afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor
export workdir="/afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor"
export X509_USER_PROXY="/afs/cern.ch/work/c/cherepan/T3M/Tools/ControlScripts/proxy/x509up_u54841"
cd /afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor

#python -i missing_layers.py  -m 1 -f ../ZMM_RU_10_05.root  -j Efficiency_MissingLayers_AllSimHits_RU_ME21 -c 0  -r 0 -k 1  2>&1 | tee LogRU_All
python -i eff_csc.py  -m 1 -f ../ZMM_RU_10_05.root  -j Efficiency_AllSimHits_RU_ME21 -c 0  -r 0 -k 1 2>&1 | tee LogRU_All


export HOME="/afs/cern.ch/user/c/cherepan"         
echo 'Completed Job' 

