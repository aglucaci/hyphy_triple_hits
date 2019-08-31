"""
@usage on silverback:

python36 directoryscanner_PETROV_noS2S.py -a /home/aglucaci/TRIPLE_HITS/data/PETROV/bestrecip_prank_alignments

useful command for deleting empty json output files:

find . -size 0 -delete

"""

""" IMPORTS """
import os, argparse, subprocess, re, sys
import argparse
import subprocess
import re
import sys

""" DECLARES """
#batch_file = "/home/aglucaci/hyphy-develop/res/hyphy-analyses/FitMultiModel/FitMultiModel.bf"
batch_file = "/home/aglucaci/hyphy-develop/res/hyphy-analyses/FitMultiModel/FitMultiModel_serineless.bf"
HYPHY = "/home/aglucaci/hyphy-develop/HYPHYMP"
LIBPATH = "/home/aglucaci/hyphy-develop/res/"
TREE_DIR="/home/aglucaci/TRIPLE_HITS/data/PETROV/bestrecip_prank_alignments/Trees/BioNJ/ForHyPhy"
OUTPUT_DIR="/home/aglucaci/TRIPLE_HITS/analysis/PETROV/noS2S_FITTERS/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

""" MAIN SUBROUTINE """
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

    args = parser.parse_args()

    numbers = re.compile ("^\.[0-9]+$")

    count = 0

    for root, dirs, files in os.walk(args.alignments):
        for each_file in files:
            name, ext = os.path.splitext(each_file)
            if len(ext) > 0 and ext in ['.mt', '.nex', '.fa'] or numbers.match (ext)  :
                #existing = os.path.join (args.alignments, name + ext + ".FITTER.json")
                existing = os.path.join(OUTPUT_DIR, name + ext + ".FITTER.json")

                if not os.path.isfile (existing):
                    file = os.path.join (root, name + ext)
                    #gen_code = 'Universal' if ext != '.mt' else 'Vertebrate mtDNA'
                    #https://github.com/veg/hyphy/blob/master/res/TemplateBatchFiles/TemplateModels/chooseGeneticCode.def
                    gen_code = "Universal"
                    #gen_code = "Vertebrate-mtDNA"
                    #gen_code = "Invertebrate-mtDNA"
                    print (file, gen_code)
                    #print (os.path.join(TREE_DIR, file.split("/")[-1] + "-BioNJ_tree_hyphy.nwk"))
                    TREE_FILE = os.path.join(TREE_DIR, file.split("/")[-1] + "-BioNJ_tree_hyphy.nwk")
                                       #subprocess.run (["qsub", "-q", "epyc", "-V", "-l walltime=12:00:00"], input = ('/home/aglucaci/hyphy-develop/HYPHYMP LIBPATH=/home/aglucaci/hyphy-develop/res/ /home/aglucaci/hyphy-develop/res/hyphy-analyses/FitMultiModel/FitMultiModel.bf ' + '--alignment ' + file + ' --code ' + gen_code), universal_newlines = True)

                    #subprocess.run (["qsub", "-q", "epyc", "-V", "-l walltime=12:00:00"], input = ('/home/aglucaci/hyphy-develop/HYPHYMP LIBPATH=/home/aglucaci/hyphy-develop/res/ /home/aglucaci/hyphy-develop/res/hyphy-analyses/FitMultiModel/FitMultiModel.bf ' + '--alignment ' + file + ' --tree ' + TREE_FILE + ' --code ' + gen_code), universal_newlines = True
                    input_string = ""
                    input_string += HYPHY
                    input_string += " LIBPATH="
                    input_string += LIBPATH + " "
                    input_string += batch_file
                    input_string += " --alignment " + file
                    input_string += " --tree " + TREE_FILE
                    input_string += " --code " + gen_code
                    #input_string += " --output " + OUTPUT_DIR+name+ext+".FITTER.json"
                    input_string += " --output " + existing

                    #print(input_string)

                    subprocess.run (["qsub", "-V", "-l walltime=12:00:00"], input = (input_string), universal_newlines = True)

                    #subprocess.run (["qsub", "-V", "-l walltime=12:00:00"], input = ('/home/aglucaci/hyphy-develop/HYPHYMP LIBPATH=/home/aglucaci/hyphy-develop/res/ /home/aglucaci/hyphy-develop/res/hyphy-analyses/FitMultiModel/FitMultiModel_serineless.bf ' + '--alignment ' + file + ' --tree ' + TREE_FILE + ' --code ' + gen_code), universal_newlines = True)
                    count += 1
                    if count == 2: sys.exit(1)
                else:
                    print ("CACHED %s" % existing)

    sys.exit(0)


"""
  END OF FILE
"""
