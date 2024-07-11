#! /bin/env python3


import ROOT
import argparse

def save_th2d_histograms_as_png(root_filename, output_directory):


    ROOT.gROOT.ProcessLine(".L tdrstyle.cc")
#    setTDRStyle(False)

    
    # Open the ROOT file
    
    root_file = ROOT.TFile(root_filename)
    
    # Get list of keys in the ROOT file
    keys = root_file.GetListOfKeys()
    
    # Loop over all keys in the ROOT file
    for key in keys:
        obj = key.ReadObj()
        
        # Check if the object is a TH2D histogram
        if isinstance(obj, ROOT.TH2F):
            # Determine point color and legend label based on histogram name
            if 'ElesimHits2D' in obj.GetName():
                point_color = ROOT.kRed
                legend_label = "{} - e simHits".format(obj.GetName()[:4])
            elif 'MusimHits2D' in obj.GetName():
                point_color = ROOT.kBlue
                legend_label = "{} - #mu simHits".format(obj.GetName()[:4])
            elif 'HadsimHits2D' in obj.GetName():
                point_color = ROOT.kBlack
                legend_label = "{} - #pi/p simHits".format(obj.GetName()[:4])
            elif 'recHits2D' in obj.GetName():
                point_color = ROOT.kBlack
                legend_label = "{} - recHits".format(obj.GetName()[:4])
            else:
                continue  # Skip histograms not containing 'Eles' or 'Mus'
            
            # Create canvas for plotting
            canvas = ROOT.TCanvas("canvas", "TH2D Plot", 800, 600)
            
            # Draw the histogram on the canvas with point color
            obj.SetMarkerColor(point_color)
            obj.Draw()
            
            # Add legend
            legend = ROOT.TLegend(0.1, 0.75, 0.3, 0.95)  # Left upper corner
            legend.SetBorderSize(0)
            legend.SetFillColor(0)
            legend.SetLineColor(0)
            legend.SetFillStyle(0)
            legend.SetTextSize(0.05)
            legend.SetTextColor(point_color)
            legend.SetTextFont(42)



            legend.AddEntry(obj, legend_label, "p")
            legend.Draw()
            
            # Generate output file name
            output_file = '{}/{}.png'.format(output_directory, obj.GetName())
            
            # Save canvas as PNG
            canvas.SaveAs(output_file)
    
    # Close the ROOT file
    root_file.Close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save TH2D histograms from a ROOT file as PNG files.')
    parser.add_argument('root_file', type=str, help='Path to the ROOT file')
    parser.add_argument('-o', '--output', type=str, default='output_plots', help='Output directory to save PNG files')
    
    args = parser.parse_args()
    
    save_th2d_histograms_as_png(args.root_file, args.output)
