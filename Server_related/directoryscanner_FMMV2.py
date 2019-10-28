#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@usage on silverback:

# =============================================================================
# FITTERS V2
# =============================================================================


    
#SELECTOME
python36 directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/analysis/FITTERS_V2/SELECTOME
    
#PETROV
python36 directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/PETROV/bestrecip_prank_alignments -o /home/aglucaci/TRIPLE_HITS/analysis/FITTERS_V2/PETROV -t True
    PETROV_TREEDIR = /home/aglucaci/TRIPLE_HITS/data/PETROV/bestrecip_prank_alignments/Trees/BioNJ/ForHyPhy

#IMMUNE
python36 directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/IMMUNE_GENES/compgen_alignments -o /home/aglucaci/TRIPLE_HITS/analysis/FITTERS_V2/IMMUNE -t True
    IMMUNE_TREEDIR = /home/aglucaci/TRIPLE_HITS/data/IMMUNE_GENES/compgen_alignments/Trees/BioNJ/ForHyPhy
    
#mtDNA
    python36 directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/updatedAnalysis_mtDNA_combined -o 
    
    python36 directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/updatedAnalysis_mtDNA_combined

#HIV LANL    
    
    
    Another script
    
python36 directoryscanner_refactor_withoutput_SRV_multiprocess.py -a /home/aglucaci/TRIPLE_HITS/data/HIV_LANL/Preprocessing/SEQUENCES -o /home/aglucaci/TRIPLE_HITS/analysis/FITTERS_V2/HIV_LANL -t /home/aglucaci/TRIPLE_HITS/data/HIV_LANL/Preprocessing/TREES


# =============================================================================
# END OF FITTERS V2
# =============================================================================
    
#PETROV
python36 directoryscanner_refactor_withoutput_ISLANDS.py -a /home/aglucaci/TRIPLE_HITS/data/PETROV/bestrecip_prank_alignments -o /home/aglucaci/TRIPLE_HITS/analysis/PETROV/bestrecip_prank_alignments_SRV_ISLANDS_FITTERS_JSON -t True
python36 directoryscanner_refactor_withoutput_ISLANDS.py -a /home/aglucaci/TRIPLE_HITS/data/IMMUNE_GENES/compgen_alignments -o 
#useful command for deleting empty json output files:
find . -size 0 -delete

"""

# =============================================================================
# Imports
# =============================================================================
import os, argparse, subprocess, re, sys
import argparse
import subprocess
import re
import sys
import time

# =============================================================================
# Declares
# =============================================================================
#Specifiy batch file
batch_file = "/home/aglucaci/hyphy-analyses/FitMultiModel/FitMultiModel.bf"

#HyPhy location
#HYPHY = "/home/aglucaci/hyphy-develop/HYPHYMP"
HYPHY = "/home/aglucaci/hyphy-develop-alt/HYPHYMP"

#HyPhy resource folder
LIBPATH = "/home/aglucaci/hyphy-develop-alt/res/"

#Optional Tree directory
#TREE_DIR="/home/aglucaci/TRIPLE_HITS/data/IMMUNE_GENES/compgen_alignments/Trees/BioNJ/ForHyPhy"
#OUTPUT_DIR="/home/aglucaci/TRIPLE_HITS/analysis/IMMUNE_GENE/compgen_alignments_SRV_FITTERS_JSON"


#if not os.path.exists(OUTPUT_DIR):
#    os.makedirs(OUTPUT_DIR)

numsimul_jobs = 500

# =============================================================================
# Helper function
# =============================================================================
def main(path):
    numbers = re.compile ("^\.[0-9]+$")
    count = 0
    for root, dirs, files in os.walk(path):
        for each_file in files:
            name, ext = os.path.splitext(each_file)
            if len(ext) > 0 and ext in ['.mt', '.nex', '.fa', '.phy'] or numbers.match (ext):
                existing = os.path.join(OUTPUT_DIR, name + ext + ".FITTER.json")
                if not os.path.isfile (existing):
                    file = os.path.join (root, name + ext)
                    gen_code = 'Universal' if ext != '.mt' else 'Vertebrate mtDNA'
                    if TREE_DIR != "":
                        TREE_FILE = os.path.join(TREE_DIR, file.split("/")[-1] + "-BioNJ_tree_hyphy.nwk")
                    print (file, gen_code)
                    input_string = ""
                    input_string += HYPHY
                    input_string += " LIBPATH="
                    input_string += LIBPATH + " "
                    input_string += batch_file
                    input_string += " --alignment " + file 
                    if TREE_DIR != "":
                        input_string += " --tree " + TREE_FILE
                    input_string += " --code " + gen_code
                    #input_string += " --output " + OUTPUT_DIR+name+ext+".FITTER.json"
                    input_string += " --output " + existing
                               
                    print(input_string)
                   
                    #["qsub", "-V", "-l", "nodes=1:ppn=24", "-l", "walltime=999:99:99"]                    
                    subprocess.run (["qsub","-q", "opteron", "-V", "-l", "walltime=12:00:00"], input = (input_string), universal_newlines = True)
                    #subprocess.run (["qsub","-q", "epyc", "-V", "-l", "walltime=12:00:00"], input = (input_string), universal_newlines = True) 
                    count += 1
                    #if count == numsimul_jobs: sys.exit(1)
                    if count == numsimul_jobs: break
                else:
                    print ("CACHED %s" % existing)
                     
# =============================================================================
# Main subroutine
# =============================================================================
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='scan the directory of NGS files and process them'
    )
    parser.add_argument(
        '-a', '--alignments',
        type=str,
        help='the directory that contains sequence alignments',
        required=True,
    )
    parser.add_argument('-o', '--output_dir',
                        type=str,
                        help='the output directory',
                        required=False,)    
    parser.add_argument('-t', '--tree_dir',
                        type=str,
                        help='the tree directory',
                        required=False,)

    args = parser.parse_args()

    path = args.alignments    

    OUTPUT_DIR = args.output_dir
	
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)    

    TREE_DIR = ""

    if args.tree_dir == "True":
        TREE_DIR = path + "/Trees/BioNJ/ForHyPhy"

    file_count = 0
    for root, dirs, files in os.walk(path):
        for file in files: file_count += 1
    
    num_of_runs = int(file_count/numsimul_jobs) + 1
    #print(file_count, num_of_runs)
        
    import datetime
    x = 0
    while x < num_of_runs + 1:
        main(path)
        print("Sleeping: ", str(datetime.datetime.now())) 
        time.sleep(3600)
        x += 1
        
    
    

# =============================================================================
# END OF FILE
# =============================================================================
