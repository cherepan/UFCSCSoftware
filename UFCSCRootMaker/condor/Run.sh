#! /bin/bash
echo 'Starting Job' 
ls -lt /afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor
export workdir="/afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor"
export X509_USER_PROXY="/afs/cern.ch/work/c/cherepan/T3M/Tools/ControlScripts/proxy/x509up_u54841"
cd /afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_12_4_4/src/UFCSCSoftware/UFCSCRootMaker/condor
source deb.test
export HOME="/afs/cern.ch/user/c/cherepan"         
echo 'Completed Job' 

