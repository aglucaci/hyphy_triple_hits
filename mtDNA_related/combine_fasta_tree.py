# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 18:07:47 2019

@author: alexander lucaci

usage:
    
    python combine_fasta_tree.py <path to fasta> <path to treefile> <is tree file nexus? (type: "nexus")> <output directory>
    
    for mtDNA see below
    
    for SELECTOME: E:\TRIPLE HITS\SELECTOME_TRIP_AMMENDED\selectome_trip_ammended
    
    aligned fasta =
    
    tree file = E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON
    
    output dir = 
"""

# =============================================================================
# Imports
# =============================================================================
import os , sys

# =============================================================================
# Declares
# =============================================================================
#for selectome, nexus and aligned fasta

print(len(sys.argv))
print(sys.argv[0])

sys.exit(3)

#if sys.argv[1] != "": 
#DNA_path = sys.argv[1]


#for mtDNA data
DNA_path = r"E:\TRIPLE HITS\updatedAnalysis_mtDNA\updatedAnalysis_mtDNA"
fasta_ending = ".fas"
treefile_ending = ".txt-TREE"
alt_treefile_ending = ".fa-TREE"
output_dir = r"E:\TRIPLE HITS\updatedAnalysis_mtDNA\for_hyphy"
output_ending = ".fa"
#files = [f for r, d, f in os.walk(SELECTOME)]
#existing = [os.path.join(SELECTOME, file) for file in files[0]]
#name, ext = os.path.splitext(each_file)



# =============================================================================
# helper functions
# =============================================================================
def read_nexus_grab_tree():
    pass

def write(filename, data, mode):
    with open(filename, mode) as f:
        f.write(data)
    f.close()

# =============================================================================
# 
# =============================================================================

cnt = 0 
exclude_directorys = ['mrbayesresults', 'dNdSresults', 'dNdS4x4random', 'dNdS4x4default', 'dndsrateclasses']

for root, directory, files in os.walk(DNA_path):
    """
    print("CURRENT ROOT AND DIR:", root, directory)
    
    for item in exclude_directorys: 
        print(root, item)
           #if item in root.split("\\"):
               
           #    continue    
    """
    
    for n, file in enumerate(files):
        
        name, ext = os.path.splitext(file) 
        
        #if ext == fasta_ending or ext == treefile_ending:
        if ext == fasta_ending: #found a fasta
            #print(root, file, name)
            
            if os.path.isfile(os.path.join("\\", root, name + treefile_ending)):
                the_treefile_ending = treefile_ending
                
            if os.path.isfile(os.path.join("\\", root, name + alt_treefile_ending)):
                the_treefile_ending = alt_treefile_ending
            
            
            #if os.path.isfile(os.path.join("\\", root, name + treefile_ending)) or os.path.isfile(os.path.join("\\", root, name + alt_treefile_ending)): #found our pair
            if 1 == 1:   
                #create new file with the same name and output_ending
                output_file = os.path.join(output_dir, name + output_ending)
                
                write(output_file, "" , "w+")
                
                #take the original fasta file
                with open(os.path.join("\\", root, file)) as f:
                    for n, line in enumerate(f):
                        #write it to the file in the output dir
                        if line != "\n":
                            write(output_file, line, "a+")
                        #print([line])
                f.close()

                #take the original tree file
                try:
                    with open(os.path.join("\\", root, name + the_treefile_ending)) as f:
                        for n, line in enumerate(f):
                            #write it to the bottom, after the alignment
                            write(output_file, line, "a+")
                    f.close()
                    
                    print(cnt, "found pair FASTA:", root, file)
                    print(cnt, "found pair TREE:", root, name + the_treefile_ending)
                    
                    cnt += 1
                except:
                    #del file
                    print("removing:", output_file)
                    os.remove(output_file)
                    continue
                
        #if cnt > 2: break
                #done
                
        
                
print(cnt)