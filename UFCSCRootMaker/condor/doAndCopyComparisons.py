#! /bin/env python

import subprocess
import os
import shutil
from datetime import datetime
import argparse

def run_comparison(file1, file2, output_pdf):
    command = ['./compare.py', file1, file2, '-f', output_pdf]
    subprocess.call(command)

def copy_to_eos_directory(source_dir, destination_dir, keyword):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        if keyword in filename and filename.endswith('.pdf'):
            shutil.copy(os.path.join(source_dir, filename), destination_dir)
            print "Copied {} to {}".format(filename, destination_dir)

def main(file1, file2, output_tag):
    # Run the comparison script
    output_pdf = '{}.pdf'.format(output_tag)
    run_comparison(file1, file2, output_pdf)

    # Determine EOS directory path with date stamp and output tag
    eos_dir = "/eos/user/c/cherepan/www/CSC/{}_{}".format(output_tag, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    # Copy PDF files containing OutputTag to EOS directory
    source_dir = os.getcwd()  # Assuming PDFs are generated in the current working directory
    copy_to_eos_directory(source_dir, eos_dir, output_tag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare .root files and copy resulting PDFs to EOS directory.')
    parser.add_argument('file1', type=str, help='First .root file')
    parser.add_argument('file2', type=str, help='Second .root file')
    parser.add_argument('output_tag', type=str, help='Output tag for PDF filename')
    args = parser.parse_args()

    main(args.file1, args.file2, args.output_tag)
