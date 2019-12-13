#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:39:17 2019

@author: Alexander G. Lucaci

Generate codon simulations with indel variation.
"""

# =============================================================================
# Imports
# =============================================================================
import os
import subprocess

# 20 taxa
newick_tree = "(((t5:0.8387175682,(t15:0.5062256691,t20:0.4268791114):0.2616007966):0.6595019614,(((t13:0.2706014984,t10:0.0950807028):0.3844690423,((t4:0.4765229183,t6:0.1098402012):0.9078059539,((t8:0.5782247176,t17:0.3210065537):0.2936283879,t3:0.1973517456):0.1450195813):0.007349848282):0.6517515222,((t7:0.1301021155,t11:0.1222830669):0.07541335584,(t1:0.98157748,t2:0.05400245683):0.7176890965):0.3630311065):0.2223174456):0.8117952493,((t12:0.2945194815,t19:0.444623478):0.7230126909,((t14:0.9236292241,t16:0.005563544575):0.5505843789,(t18:0.8419787451,t9:0.7891180061):0.4485002037):0.8197243938):0.4382306426);"

# =============================================================================
# Declares
# =============================================================================
control_file = []

control_file.append("/////////////////////////////////////////////////////////////////////////////////////")
control_file.append("//                                                                                 //")
control_file.append("//  INDELible V1.03 control file - basiccodon.txt                                  //")
control_file.append("//                                                                                 //")
control_file.append("//      A basic introduction to the structure of the INDELible control file.       //")
control_file.append("//                                                                                 //")
control_file.append("/////////////////////////////////////////////////////////////////////////////////////")
control_file.append("")
control_file.append("// It is useful to know that anything on a line after two forward slashes is ignored.")
control_file.append("")
control_file.append("/*")
control_file.append("   Another useful thing to know is that anything after a forward slash and star")
control_file.append("   is ignored until INDELible sees a star followed by a forward slash later on.")
control_file.append("*/     ")
control_file.append("")
control_file.append("[TYPE] CODON 1     	//  EVERY control file must begin with a [TYPE] command.")
control_file.append("			//  The number after 'CODON' can be 1 or 2 and chooses the ")
control_file.append("			//  algorithm that INDELible uses (see manuscript). Both give ")
control_file.append("			//  identical results but in some cases one is quicker.")
control_file.append("			//  Other blocks and commands following this statement")
control_file.append("			//  can come in any order you like.")
control_file.append("")
control_file.append("[MODEL]    modelname          //  Evolutionary models are defined in [MODEL] blocks.")
control_file.append("  [submodel]     2.5  1.0     //  Substitution model is M0 with kappa=2.5, omega=0.5")
control_file.append("  [insertmodel]  POW  1.7 500 //  Power law insertion length distribution (a=1.7, M=500)")
control_file.append("  [deletemodel]  POW  1.8 500 //  Power law deletion length distribution (a=1.8, M=500)")
control_file.append("  [indelrate]    0.1          //  insertion rate = deletion rate = 0.1")
control_file.append("                              //  relative to average substitution rate of 1.   ")
control_file.append("")
#control_file.append("[TREE] treename ((((A:0.2, B:0.3):0.3,(C:0.5, D:0.3):0.2):0.3, E:0.7):1.0);")
control_file.append("[TREE] treename " + newick_tree)

control_file.append("")
control_file.append("        ")
control_file.append("//  User trees are defined here")
control_file.append("")
control_file.append("")
control_file.append("[PARTITIONS] partitionname             //  [PARTITIONS] blocks say which models go with")

# SEQUENCE LENGTH

control_file.append("  [treename modelname 500]            //  which trees and define the length of the")
control_file.append("                                       //  sequence generated at the root (1000 here).")
control_file.append("")
control_file.append("[EVOLVE] partitionname 1 CODON_INDEL_SIMS_t1_  //  This will generate 100 replicate datasets ")

#control_file.append("partitionname 5 outputname2")
#control_file.append("partitionname 5 outputname3")
control_file.append("        ")
control_file.append("        ")
control_file.append("// The true alignment will be output in a file named outputname_TRUE.phy")
control_file.append("// The unaligned sequences will be output in a file named outputname.fas")
control_file.append("// To learn how to implement more complicated simulations (or different ")
control_file.append("// models) please consult the manual or the other example control files.")


INDEL_RATE = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
INDEL_RATE += [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]
INDEL_RATE += [0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3]
INDEL_RATE += [0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4]
INDEL_RATE += [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5]

OUTPUT_FILENAME_TAG = "CODON_INDEL_SIMS_"

num_output_files = 30 #number of files to simulate

# =============================================================================
# Main subroutine
# =============================================================================
#Need to generate a new tree

#Loop over indel rates, 0.1, 1.0 in steps of 0.1
#Write out control file.
#Generate simulations
#25 taxa, 300 codons


#Run the indelible binary.

def main(RATE):
    with open("control.txt", "w") as f: #this should rewrite the control.txt each time.
        
        for line in control_file:
            #print(line)
            
            if "indelrate" in line: #adjust indelrate
                pass
                f.write("  [indelrate]    " + str(RATE) + "          //  insertion rate = deletion rate = 0.1")
                continue
            
            if "EVOLVE" in line:
                #write the line, write how many files we want as output
                #and then continue
                f.write(line + "\n")
                for n in range(2, num_output_files + 1):
                    f.write("partitionname 1 CODON_INDEL_SIMS_t1_" + str(n) + "\n")
                continue
            
            f.write(line + "\n")
            
    f.close()
        
    
    #Run Indelible.
    print("# Running INDELible")
    subprocess.run("./indelible")
        
    
    #once this is ran,
    #copy the output files to a folder with the indel rate
    
    folder = str(RATE).replace(".", "_")
    
    subprocess.run(["mkdir", folder])
    #subprocess.run(["mv", "*.phy", "0_1"], shell=True)
    #subprocess.run(["mv", "*.fas", "0_1/"], shell=True)
    
    subprocess.run(["mv *.phy " + folder], shell=True)
    subprocess.run(["mv *.fas " + folder], shell=True)
    
# =============================================================================
# Main
# =============================================================================
#print(os.path.realpath(__file__)) # PATH TO FILE
#print(os.path.dirname(os.path.realpath(__file__)))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

for rate in INDEL_RATE:
    CHECK = CURRENT_DIR + "/" + str(rate).replace(".", "_")
    #print(CHECK)
    #print(os.path.exists(CHECK))
    if not os.path.exists(CHECK):
        main(rate)
        #print(os.path.exists(CHECK)) 



#for rate in INDEL_RATE:
#    if not os.path.exists(OUTPUT_DIR):
#    os.makedirs(OUTPUT_DIR)
#    main(rate)
#break

# =============================================================================
#  End of file
# =============================================================================