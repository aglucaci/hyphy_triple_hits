#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
@usage on silverback:
# =============================================================================
# FITTERS V0.2 - Fixed Bug  11/5/2019
# =============================================================================
    
#SELECTOME
python36 ../directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/analysis/SELECTOME_FITTERS
python36 ../directoryscanner_FMMV2.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/analysis/SELECTOME_FITTERS_ISLANDS -islands Yes    

#Uses 
  Python 3.7
  HyPhy 2.5.15
  HyPhy Standalone-analyses

Command:
-a is alignments
-o is output folder
-t is tree directory
-islands is Yes/No to use islands parameter

python directoryscanner_TH_REVISIONS.py -a {} -t {} -o {} -islands Yes

# MASKED SELECTOME
python directoryscanner_TH_REVISIONS_ExtendedAnalysis.py -a /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/selectome_v06_Euteleostomi-nt_masked_mod -t /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/selectome_v06_Euteleostomi-Trees_Newick -o /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis




# UNMASKED SELECTOME
python directoryscanner_TH_REVISIONS_ExtendedAnalysis_CheckForErrors.py -a /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -o /home/aglucaci/TRIPLE_HITS/TH_REVISIONS/analysis/UNMASKED_SELECTOME



    
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
import datetime

# =============================================================================
# Declares
# =============================================================================

BASEDIR = "/home/aglucaci/TRIPLE_HITS/TH_REVISIONS"


#Specifiy batch file
batch_file = BASEDIR + "/scripts/hyphy-analyses/FitMultiModel/FitMultiModel.bf"
ABSREL = BASEDIR + "/scripts/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/aBSREL.bf"
BUSTEDSMH = BASEDIR + "/scripts/hyphy-analyses/BUSTED-MH/BUSTED-MH.bf"
BUSTED = BASEDIR + "/scripts/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/BUSTED.bf"

#HyPhy location
#HYPHY = "/home/aglucaci/hyphy-develop/HYPHYMP"
HYPHY = BASEDIR + "/scripts/hyphy-develop/HYPHYMP"

#HyPhy resource folder
#LIBPATH = "/home/aglucaci/hyphy-develop/res/"
LIBPATH = BASEDIR + "/scripts/hyphy-develop/res"

STDIN = BASEDIR + "/scripts/STDIN"
STDIN_E = BASEDIR + "/scripts/STDIN_E"
numsimul_jobs = 50

HYPHY_ERRORS_FILELIST = []

# =============================================================================
# Helper function
# =============================================================================
def make_command(HYPHY, LIBPATH, batch_file, file, TREE_FILE, gen_code, existing):
    #Initialize the command 
    input_string = ""
    input_string += HYPHY
    input_string += " LIBPATH="
    input_string += LIBPATH + " "
    input_string += batch_file
    input_string += " --alignment " + file 
    if TREE_FILE != "NEXUS":
        input_string += " --tree " + TREE_FILE
    input_string += " --code " + gen_code
    #if islands == "Yes": input_string += " --triple-islands Yes "
    input_string += " --output " + existing

    return input_string
#end method


def main(path, islands, TREE_DIR):
    global OUTPUT_DIR, STDIN, STDIN_E, HYPHY_ERRORS_FILELIST
    numbers = re.compile ("^\.[0-9]+$")
    count = 0

    for root, dirs, files in os.walk(path):
        for n, each_file in enumerate(files):
            name, ext = os.path.splitext(each_file)
            if len(ext) > 0 and ext in ['.fas', '.nex'] or numbers.match (ext):
                file = os.path.join (root, name + ext)
                gen_code = 'Universal' if ext != '.mt' else 'Vertebrate mtDNA'

                #print (file, gen_code)
                 
                # Check for Hyphy Errors

                print(n, "# Checking for HyPhy Errors", [each_file])
                if str(each_file) in HYPHY_ERRORS_FILELIST: 
                    print("\t Found in Errors list")
                    continue
                    #sys.exit(2)
                else:
                    print("\t Passed")

                #continue
                #sys.exit(1)                               

                # end - check for hyphy errors


                if ext == '.nex': 
                    TREE_FILE = "NEXUS" 
                else:
                    #Set tree file.
                    TREE_FILE = ""
                    TREE_FILE = file.split("/")[-1]
                    TREE_FILE = TREE_FILE.replace(".nt_masked.fas", ".nwk")
                    TREE_FILE = TREE_DIR + "/" + TREE_FILE
                #end if
                print()  
                
                #Submit to HPC 
                

                # BUSTED S
                #existing = os.path.join(OUTPUT_DIR, name + ext + ".BUSTED.json")
                #if not os.path.isfile(existing):
                #    cmd = make_command(HYPHY, LIBPATH, BUSTED, file, TREE_FILE, gen_code, existing)
                #    print(cmd)
                #    subprocess.run(["qsub","-q", "epyc", "-V", "-l", "walltime=999:00:00", "-N", name, "-o", STDIN], input = (cmd), universal_newlines = True)
                #    count += 1
                #else:
                #    print ("CACHED %s" % existing)
                #end if

                               
                # BUSTED SMH
                existing = os.path.join(OUTPUT_DIR, name + ext + ".BUSTEDS.json")
                if not os.path.isfile(existing):
                    cmd = make_command(HYPHY, LIBPATH, BUSTEDSMH, file, TREE_FILE, gen_code, existing)
                    print(cmd)
                    subprocess.run(["qsub","-q", "epyc", "-V", "-l", "walltime=999:00:00", "-N", name, "-o", STDIN, "-e", STDIN_E], input = (cmd), universal_newlines = True) 
                    count += 1
                else:
                    print ("CACHED %s" % existing)
                #end if
                
                # ABSREL
                existing = os.path.join(OUTPUT_DIR, name + ext + ".ABSREL.json")
                if not os.path.isfile(existing):
                    cmd = make_command(HYPHY, LIBPATH, ABSREL, file, TREE_FILE, gen_code, existing)
                    print(cmd)
                    subprocess.run(["qsub","-q", "epyc", "-V", "-l", "walltime=999:00:00", "-N", name, "-o", STDIN, "-e", STDIN_E], input = (cmd), universal_newlines = True) 
                    count += 1
                else:
                    print ("CACHED %s" % existing)
                #end if
                
                # ABSREL MH
                existing = os.path.join(OUTPUT_DIR, name + ext + ".ABSREL-MH.json")
                if not os.path.isfile(existing):
                    cmd = make_command(HYPHY, LIBPATH, ABSREL, file, TREE_FILE, gen_code, existing)
                    cmd += " --multiple-hits Double+Triple"
                    print(cmd)
                    subprocess.run(["qsub","-q", "epyc", "-V", "-l", "walltime=999:00:00", "-N", name, "-o", STDIN, "-e", STDIN_E], input = (cmd), universal_newlines = True)
                    count += 1
                else:
                    print ("CACHED %s" % existing)
                #end if
                
                print()

                if count >= numsimul_jobs: break
                
            #end outer if          
        #end inner for
    #end outer for
#end method



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
    parser.add_argument('-islands', '--islands',
                        type=str,
                        help='Do you want to run FMM with the islands parameter?',
                        required=False,)


    args = parser.parse_args()
    path = args.alignments    


    #Load HyPhy Errors filelist
    print("# Checking STDIN for errors and outputting ERRORS.txt")
    os.system("python HYPHY_ERRORS.py")

    with open("ERRORS.txt", "r") as fh:
         data = fh.read()
    fh.close
    #end with

    data = data.split("\n")
    print(data)
    HYPHY_ERRORS_FILELIST = data
    #End - load hyphy errors filelist


    OUTPUT_DIR = args.output_dir
	
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)    

    TREE_DIR = ""

    TREE_DIR = args.tree_dir

    file_count = 0

    for root, dirs, files in os.walk(path):
        for file in files: file_count += 1
    
    num_of_runs = int(file_count/numsimul_jobs) + 1
    
    print("Total number of files:", file_count) 
    print("Number of 'runs' required':", num_of_runs)
    
    main(path, "", TREE_DIR)

    print("## Exiting...")
    sys.exit(1)

    """    
    x = 0
    while x < num_of_runs + 1:
        if args.islands == "Yes": 
            main(path, args.islands, TREE_DIR)
        else:
            main(path, "", TREE_DIR)
        print("Sleeping: ", str(datetime.datetime.now())) 
        time.sleep(3600)
        #time.sleep(1800)
        x += 1
        #end if
    #end while
    """
#end if
    
    

# =============================================================================
# END OF FILE
# =============================================================================
