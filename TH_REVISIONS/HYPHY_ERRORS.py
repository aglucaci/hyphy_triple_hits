#!/usr/bin/python


import os
import sys


STDIN_Folder = "STDIN"
FILENAMES = []


def process_stdin(filename):
   with open(filename, "r") as fh:
       data = fh.read()
       if "The mapping between original and normalized tree sequence names must be one to one in call to" in data:
           print([data]) 
           return "ERROR"
       return ""
   #end with
#end method
       

with open("ERRORS.txt", "w") as fh:
    fh.write("")
fh.close()


for subdir, dirs, files in os.walk(STDIN_Folder):
    for n, file in enumerate(files):
        if not file.endswith(".swp") and not file.endswith(".swo"):
            filepath = subdir + os.sep + file
            print(n+1, file)
            check_errors = process_stdin(filepath)
            if check_errors != "":
                #Bad file, write to exclusion list
                filename_nexus = file.split(".")
                filename_nexus = ".".join([filename_nexus[0], filename_nexus[1], filename_nexus[2], "nex"])          
                print(filename_nexus)

                #Changed to ouput set not list, avoids duplicate filenames  
                FILENAMES += [filename_nexus]

                #with open("ERRORS.txt", "a+") as fh:
                #     fh.write(filename_nexus + "\n") 
                ##end with
            #end if
        #end if
    #end for
#end for

with open("ERRORS.txt", "a+") as fz:
    for filename in set(FILENAMES):    
        fz.write(filename + "\n")
#end with




# End of file





