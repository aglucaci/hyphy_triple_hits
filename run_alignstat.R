## R script ######
library("AlignStat")

setwd("~/Documents/TRIPLE_HITS/Realignment_testing/AlignStat")

# Example data loading
#data("../data/reference_alignment")
#data("../data/comparison_alignment")
#data("reference_alignment")
#data("comparison_alignment")

ref = "../selectome_aligned_fasta/ENSGT00390000000002.Euteleostomi.002.fasta"
#comp = "../mafft/ENSGT00390000000002.Euteleostomi.002.fasta"
comp = "../mafft_changed_filenames/ENSGT00390000000002.Euteleostomi.002.fasta"

# Alignment comparison calculation
#PAC <- compare_alignments  (reference_alignment, comparison_alignment, CS=TRUE, SP=TRUE)
PAC <- compare_alignments  (ref, comp, CS=TRUE, SP=TRUE)

# Results visualisation
plot_similarity_heatmap    (PAC)
plot_dissimilarity_matrix  (PAC)
plot_similarity_summary    (PAC, CS=TRUE, cys=TRUE)
plot_dissimilarity_summary (PAC, stack=TRUE)
plot_SP_summary            (PAC, CS=TRUE)
