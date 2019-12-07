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
control_file.append("[TREE] treename ((((t22:0.7884912707,((t14:0.8485323223,t20:0.875784308):0.05844755005,((t29:0.9256454913,t8:0.5681589271):0.6796265363,t30:0.2025386344):0.9573877391):0.08610738721):0.921048284,(((t3:0.9725932428,t17:0.4366256092):0.6381316015,((t16:0.3180074089,t27:0.3864220553):0.2001682797,t21:0.5908179402):0.4302841208):0.4914731416,(t11:0.2886261365,t2:0.8246886986):0.2573057537):0.569526993):0.6803977506,(t10:0.06485857069,(t6:0.001371138263,(((t7:0.3931164765,t12:0.07855357323):0.406146232,(t26:0.9711873827,t23:0.8914815376):0.08172181295):0.4853650811,(t9:0.3540119417,t24:0.01268518576):0.5522214433):0.6867216111):0.939245726):0.7275894266):0.8185117426,((t4:0.5687292085,((t15:0.9149642589,t25:0.1793684226):0.3222816291,t5:0.571961625):0.3456264588):0.1211217023,(t1:0.1853761284,((t13:0.4666023802,(t28:0.6691324431,t18:0.7461213013):0.3977537802):0.7462856739,t19:0.4380299225):0.7384211062):0.4651579566):0.9417840841);")
control_file.append("")
control_file.append("        ")
control_file.append("//  User trees are defined here")
control_file.append("")
control_file.append("")
control_file.append("[PARTITIONS] partitionname             //  [PARTITIONS] blocks say which models go with")
control_file.append("  [treename modelname 900]            //  which trees and define the length of the")
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
                    f.write("partitionname 1 CODON_INDEL_SIMS_" + str(n) + "\n")
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
    #break

# =============================================================================
#  End of file
# =============================================================================