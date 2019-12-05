#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:39:17 2019

@author: user
"""

# =============================================================================
# Imports
# =============================================================================
import os
import subprocess

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
control_file.append("[TREE] treename ((((A:0.2, B:0.3):0.3,(C:0.5, D:0.3):0.2):0.3, E:0.7):1.0);")
control_file.append("")
control_file.append("        ")
control_file.append("//  User trees are defined here")
control_file.append("")
control_file.append("")
control_file.append("[PARTITIONS] partitionname             //  [PARTITIONS] blocks say which models go with")
control_file.append("  [treename modelname 1000]            //  which trees and define the length of the")
control_file.append("                                       //  sequence generated at the root (1000 here).")
control_file.append("")
control_file.append("[EVOLVE] partitionname 1 CODON_INDEL_SIMS_1  //  This will generate 100 replicate datasets ")



#control_file.append("partitionname 5 outputname2")
#control_file.append("partitionname 5 outputname3")
control_file.append("        ")
control_file.append("        ")
control_file.append("// The true alignment will be output in a file named outputname_TRUE.phy")
control_file.append("// The unaligned sequences will be output in a file named outputname.fas")
control_file.append("// To learn how to implement more complicated simulations (or different ")
control_file.append("// models) please consult the manual or the other example control files.")


INDEL_RATE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

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
    with open("control.txt", "w") as f:
        
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
                    f.write("partitionname 1 output" + str(n) + "\n")
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
    
for rate in INDEL_RATE:
    main(rate)

# =============================================================================
#  End of file
# =============================================================================
