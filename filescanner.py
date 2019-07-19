#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modified version of directoryscanner.py

@usage: python filescanner.py -f <file.txt> -d <directory containing nexus files>
on silverback:  python36 filescanner.py -f ../analysis/SERINES/filenames_p0.005-TH-Threshold\(10x\).txt -d ../data/selectome_trip_ammended/

on epyc: python3.6 filescanner.py --files /home/aglucaci/TRIPLE_HITS/analysis/SERINES/filenames_p0.005-TH_Threshold_10x.out --directory /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended --output <output_dir>
a.g.l.

useful commands:
find . -size 0 -delete
"""

# =============================================================================
# Imports
# =============================================================================
import os, argparse, subprocess, re, sys

# =============================================================================
# Declares
# =============================================================================
HYPHY = "/home/aglucaci/hyphy/HYPHYMP"
#batch_file = "/home/aglucaci/hyphy/res/TemplateBatchFiles/SelectionAnalyses/FitMultiModel.bf"
batch_file = "/home/aglucaci/hyphy/res/TemplateBatchFiles/SelectionAnalyses/FitMultiMode_cpl.bf"
LIBPATH = "/home/aglucaci/hyphy/res/"

# =============================================================================
# Main subroutine.
# =============================================================================
if __name__ == '__main__':
    #print("() in main")
    parser = argparse.ArgumentParser(description='scan the textfile of NGS files and process them')
    parser.add_argument(
        '-f', '--files',
        type=str,
        help='the textfile that contains the name of alignments we want to target for analysis.',
        required=True,
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        help='the directory that contains sequence alignments',
        required=True,
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='the output directory for model fit files (*.FITTER.json)',
        required=False,
    )
    
    args = parser.parse_args()
    numbers = re.compile ("^\.[0-9]+$")
    cnt = 0
    nodes = ["6", "7"]
    #print([args.output], type(args.output))
    #process --files file.
    with open(args.files) as f:
        for n, line in enumerate(f):
            filename = os.path.join(args.directory, line.strip())  #add filename to directory path
            #print(n, args.directory+line.strip())
            existing = filename + ".FITTER.json"
            if not os.path.isfile(existing):
                gen_code = "Universal"
                #print(filename, gen_code)      
                #print("OUTPUT DIR:", args.output)
                subprocess.Popen(["bpsh", nodes[cnt % len(nodes)], "sh", "-c", " ".join([HYPHY, " LIBPATH=" + LIBPATH, batch_file, gen_code, "--alignment " + filename])], universal_newlines = True)
                print(HYPHY + " LIBPATH=" + LIBPATH + " " + batch_file +  ' "%s" %s' % (gen_code, filename))
                cnt += 1
                if cnt == 601: sys.exit(2)
            else:
                print ("CACHED %s" % existing)
                pass 
                
                
    sys.exit(1) #^ do once.
    
# =============================================================================
# end of file
# =============================================================================
