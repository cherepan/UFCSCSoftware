#!/usr/bin/env python3


import sys
import subprocess
import os

def show_help():
    print("Usage: {} [-f root_file] [-p python_script] [-j job_name] [-c config] [-h]".format(sys.argv[0]))
    print("")
    print("Options:")
    print("  -f root_file       Specify a root file to process.")
    print("  -p python_script   Specify a Python script to execute.")
    print("  -j job_name        Specify a job name.")
    print("  -c config          Specify a configuration.")
    print("  -h                 Show this help message.")
    sys.exit(0)

def execute_python_script(python_script, root_file, job_name, config):
    if not root_file or not job_name or not config:
        print("Error: Root file, job name, and config must be specified.")
        show_help()

    print("Executing Python script: {} with root file: {}, job name: {}, and config: {}".format(python_script, root_file, job_name, config))
    subprocess.call(["python3", "-i", python_script, "-m", "1", "-f", root_file, "-j", job_name, "-c", config, "-r", "0", "-k", "1", " 2>&1 | tee ", job_name])

def main():
    # Initialize variables
    root_file = ""
    python_script = "eff_csc.py"  # Default script
    job_name = ""
    config = ""

    # Parse command line options
    args = sys.argv[1:]
    while args:
        opt = args.pop(0)
        if opt == "-f":
            root_file = args.pop(0)
        elif opt == "-p":
            python_script = args.pop(0)
        elif opt == "-j":
            job_name = args.pop(0)
        elif opt == "-c":
            config = args.pop(0)
        elif opt == "-h":
            show_help()
        else:
            print("Invalid option: {}".format(opt))
            show_help()

    # Check if required options are provided
    if not root_file or not job_name or not config:
        print("Error: Root file, job name, and config must be specified.")
        show_help()

    print('Starting Job')
    subprocess.call(["ls", "-lt", "/afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_13_3_0/src/UFCSCSoftware/UFCSCRootMaker/condor"])
    os.environ["workdir"] = "/afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_13_3_0/src/UFCSCSoftware/UFCSCRootMaker/condor"
    os.environ["X509_USER_PROXY"] = "/afs/cern.ch/work/c/cherepan/T3M/Tools/ControlScripts/proxy/x509up_u54841"
    os.chdir("/afs/cern.ch/work/c/cherepan/CSC/LocalReco/CMSSW_13_3_0/src/UFCSCSoftware/UFCSCRootMaker/condor")

    # Execute the Python script with the provided options
    execute_python_script(python_script, root_file, job_name, config)

    os.environ["HOME"] = "/afs/cern.ch/user/c/cherepan"
    print('Completed Job')

if __name__ == "__main__":
    main()
