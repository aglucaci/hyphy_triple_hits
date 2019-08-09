#NOTES
#2019
#Run Alignstat on realigned and reference selectome alignments
#Alexander Lucaci
#command line cmd: /Library/Frameworks/R.framework/Versions/3.3/Resources/Rscript run_alignstat.R 
#wd: /Users/alex/Documents/TRIPLE_HITS/Realignment_testing/AlignStat/R

## IMPORTS
library("AlignStat")

## DECLARES
setwd("~/Documents/TRIPLE_HITS/Realignment_testing/AlignStat")
start_time <- Sys.time()

REF_PATH = "../selectome_aligned_fasta"
COMP_PATH = "../mafft_changed_filenames"
OUTPUT_PATH = "results"

## HELPER FUNCTIONS
run_alignstat = function(ref, comp, output_filename){
  print("Creating empty output file")
  file.create(output_filename)
  
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
count = 0

for (file in files) {
  print(paste(count, length(files),sep="/"), quote = FALSE)
  print(paste("reference file:", file))
  ref = file
  comp = paste(COMP_PATH, basename(ref), sep="/")
  print(paste("comparison file:", comp))
  output_filename = paste(OUTPUT_PATH, paste(basename(ref), ".out", sep=""), sep="/")
  #CHECK IF OUTPUT_FILENAME EXISTS, continue
  if (file.exists(output_filename)){
    print(paste("CACHED", output_filename))
    #CONTINUE
  }
  
  if (!file.exists(output_filename)){
    run_alignstat(ref, comp, output_filename)
  }
  
  end_time <- Sys.time()
  print(paste("RUN TIME:", end_time - start_time))
  count = count + 1 
}


## END OF FILE
#https://stackoverflow.com/questions/14958516/looping-through-all-files-in-directory-in-r-applying-multiple-commands
#https://stackoverflow.com/questions/14904983/how-do-i-check-the-existence-of-a-local-file
