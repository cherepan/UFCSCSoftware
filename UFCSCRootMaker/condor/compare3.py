#!/usr/bin/env python3

import sys
import numpy as np
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

from DisplayManager import DisplayManager

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

colours = [2, 1, 3, 6, 8]
styles = [1, 1, 3, 4, 5]
width = [2, 2, 3, 3, 2]

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetLineStyle(styles[i])
    h.SetLineWidth(2)
    h.SetStats(False)


def applyEfficiencyStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetLineStyle(styles[i])
    h.SetLineWidth(2)


def get1DHistsNames(f):
    names1D = []
    for key in f.GetListOfKeys():
        h = f.Get(key.GetName())
        if isinstance(h, ROOT.TH1F):
            names1D.append(key.GetName())
    if len(names1D) != 0:
        return names1D
    else:
        print('Failed to find 1D histograms in file, returning None', f)
    return None


def getTEfficiencyNames(f):
    names1D = []
    for key in f.GetListOfKeys():
        h = f.Get(key.GetName())
        print("  h test  ", h)
        if isinstance(h, ROOT.TEfficiency):
            names1D.append(key.GetName())
    if len(names1D) != 0:
        return names1D
    else:
        print('Failed to find TEfficiency in file, returning empty list', f)
    return names1D


def find1DHists(f):
    oneDimHists = []
    for key in f.GetListOfKeys():
        h = f.Get(key.GetName())
        if isinstance(h, ROOT.TH1F):
            oneDimHists.append(h)
    if len(oneDimHists) != 0:
        return oneDimHists
    else:
        print('Failed to find 1D histograms in file, returning None', f)
    return None


def findTEfficiencyHists(f):
    oneDimHists = []
    for key in f.GetListOfKeys():
        h = f.Get(key.GetName())
        if isinstance(h, ROOT.TEfficiency):
            print('>>>>>>>>>>>>>>>', h.GetPassedHistogram().GetXaxis().GetTitle())
            oneDimHists.append(h)
    if len(oneDimHists) != 0:
        return oneDimHists
    else:
        print('Failed to find TEfficiency in file, returning empty', f)
    return oneDimHists


def comparisonPlots(hists, names_to_plot, titles, pname, ratio=True):
    display = DisplayManager(pname, ratio)

    for i_hist_name in names_to_plot:
        histstocompare = []
        for i, hlist in enumerate(hists):
            for j, h in enumerate(hlist):
                if h.GetName() == i_hist_name:
                    h_name = h.GetName() + str(j)
                    h.Sumw2()
                    applyHistStyle(h, i)
                    histstocompare.append(h)
        display.Draw(histstocompare, titles)


def comparisonEfficiencyPlots(hists, names_to_plot, titles, pname, ratio=False):
    display = DisplayManager(pname, ratio)
    print('____________________________________________________________________________________________')

    for i_hist_name in names_to_plot:
        histstocompare = []
        for i, hlist in enumerate(hists):
            for j, h in enumerate(hlist):
                if h.GetName() == i_hist_name:
                    h_name = h.GetName() + str(j)
                    applyEfficiencyStyle(h, i)
                    histstocompare.append(h)
        display.DrawEfficiency(histstocompare, titles)


if __name__ == '__main__':
    usage = '''
    > python compare.py file1.root file2.root
    '''

    parser = OptionParser(usage=usage)

    parser.add_option('-t', '--titles', type='string', dest='titles', default='UF, Default', help='Comma-separated list of titles for the N input files')
    parser.add_option('-r', '--no-ratio', dest='do_ratio', action='store_false', default=True, help='Do not show ratio plots')
    parser.add_option('-f', '--outfile', type='string', default='compare_UF_RecentLR.pdf', help='Output file name')

    (options, args) = parser.parse_args()

    if len(args) < 2:
        print('Provide at least 2 input root files')
        sys.exit(1)

    titles = options.titles.split(',')

    if len(titles) < len(args):
        print('Provide at least as many titles as input files')
        sys.exit(1)

    filesTocompare = [ROOT.TFile(arg) for arg in args]

    h_names = [set(get1DHistsNames(f)) for f in filesTocompare]
    hists = [find1DHists(f) for f in filesTocompare]
    h_names_common = set.intersection(*h_names)

    efficiency_names = [set(getTEfficiencyNames(f)) for f in filesTocompare]
    efficiency = [findTEfficiencyHists(f) for f in filesTocompare]
    efficiency_names_common = set.intersection(*efficiency_names)

    print('Making plots for all common branches')
    comparisonPlots(hists, h_names_common, titles, options.outfile, options.do_ratio)
    comparisonEfficiencyPlots(efficiency, efficiency_names_common, titles, "Efficiency_" + options.outfile, False)
