#NOTES
#2019
#Run Alignstat on realigned and reference selectome alignments
#Alexander Lucaci


## IMPORTS
library("AlignStat")

## DECLARES
setwd("~/Documents/TRIPLE_HITS/Realignment_testing/AlignStat")

REF_PATH = "../selectome_aligned_fasta"
COMP_PATH = "../mafft_changed_filenames"
OUTPUT_PATH = "results"

## HELPER FUNCTIONS
run_alignstat = function(ref, comp, output_filename){
  print("COMPARING ALIGNMENTS..")
  PAC = compare_alignments  (ref, comp, CS=TRUE, SP=TRUE)
  
  #temp = PAC$sum_of_pairs
  #cat(temp, "text.txt")
  print("CREATING DATAFRAME")
  df <- NULL
  df$File <- basename(ref)
  df$SP <- PAC$sum_of_pairs$sum.of.pairs.score
  df$PS <- PAC$sum_of_pairs$reverse.sum.of.pairs.score
  df$CS <- PAC$sum_of_pairs$column.score
  df$Score <- PAC$similarity_score
  df$CS_score <- PAC$column_score$column.score
  
  print("WRITING DATAFRAME TO FILE")
  write_df(df, output_filename)
}

write_df = function(df, filename){
  write.table(df, file = filename)
}

## MAIN SUBROUTINE
print("STARTING SCRIPT..")
files <- list.files(path=REF_PATH, pattern="*.fasta", full.names=TRUE, recursive=FALSE)

#paste(COMP_PATH, basename(files[1]), sep="/")
print("ENTERING FOR LOOP..")
for (file in files) {
  print("starting analysis for:")
  print(ref)
  ref = file
  comp = paste(COMP_PATH, basename(ref), sep="/")
  output_filename = paste(OUTPUT_PATH, paste(basename(ref), ".out", sep=""), sep="/")
  run_alignstat(ref, comp, output_filename)
}


## END OF FILE
#https://stackoverflow.com/questions/14958516/looping-through-all-files-in-directory-in-r-applying-multiple-commands