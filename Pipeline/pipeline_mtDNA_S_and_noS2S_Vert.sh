#!/bin/bash 
clear
echo "## ANALYSIS PIPELINE FOR TRIPLE HITS"
echo "Used for mtDNA analysis"
echo "Current date : $(date) @ $(hostname)"
echo "WD: "$(pwd)
echo ""


#Do variable for FITTERS folder
#VERTEBRATEfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Vertebrate_mtDNA_FITTERS"
#INVERTEBRATEfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"
#COMBINEDfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/updatedAnalysis_mtDNA_combined(FASTA_AND_FITTERS)"



# USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING
BASEDIRECTORY="/Users/alex/Documents/TRIPLE_HITS"

#FITTERS="/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
FITTERS="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Vertebrate_mtDNA_FITTERS"
#FITTERS="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"
FITTERS_NOSS="/Users/alex/Documents/TRIPLE_HITS/mtDNA_noS2S/updatedAnalysis_mtDNA_combined_FITTERS"

CSVFILE="mtDNA_noS2S_SRV.csv"
CIRCOSTEXTFILE="mtDNA_noS2S_SRV.txt"
OUTPUT_FOLDER="../analysis/mtDNA_noS2S"

# ^^^^^^ USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING ^^^^^^^^

[ -d $OUTPUT_FOLDER ] || mkdir $OUTPUT_FOLDER

#If output file exists, skip

# ==============================================================================
# pipeline_circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
# ==============================================================================
echo "(1) Running: pipeline_circos_grab_site_substitution_data.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CIRCOSTEXTFILE

#[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ]] || echo "It does exist?"
#[[ ! -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ]] || echo "It does exist?"
#[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ] || echo "It does exist? deux"

[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ]] || python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE > $OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data.txt
#python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE

# ==============================================================================
# pipeline_parse_fitter_json.py <FITTERS DIRECTORY> <OUTPUTCSV>
# ==============================================================================
echo ""
echo "(2) Running: pipeline_parse_fitter_json.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CSVFILE

[[ -e $OUTPUT_FOLDER/$CSVFILE ]] || python pipeline_parse_fitter_json.py $FITTERS $OUTPUT_FOLDER/$CSVFILE


# ==============================================================================
# pipeline_plot_csv.py <INPUTCSV>
# ==============================================================================
echo ""
echo "(3) Running: pipeline_plot_csv.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots

[ -d $OUTPUT_FOLDER/Plots ] || python pipeline_plot_csv.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/ > $OUTPUT_FOLDER/pipeline_plot_csv.txt

# ==============================================================================
# pipeline_pvalue_vs_seqlength.py <INPUTCSV>
# ==============================================================================
echo ""
echo "(4) Running: pipeline_pvalue_vs_seqlength.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots/pvalue_vs_seqlength

#[ -d $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength ] || mkdir $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength
[ -d $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength ] || python pipeline_pvalue_vs_seqlength.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength/

# ==============================================================================
# pipeline_plot_2LogEvidenceRatio.py <FITTERDIR> <OUTPUT_DIR>
# ==============================================================================
echo ""
echo "(5) Running: pipeline_plot_2LogEvidenceRatio.py"
echo "    This creates the 2*Ln*Evidence ratio plots"
[ -d $OUTPUT_FOLDER/Plots/EvidenceRatioPlots ] || python pipeline_plot_2LogEvidenceRatio.py $FITTERS $OUTPUT_FOLDER/Plots/EvidenceRatioPlots

# ==============================================================================
# pipeline_spatial_analysis_THDHSH.py <FITTERDIR> <OUTPUT_DIR>
# ==============================================================================
echo ""
echo "(6) Running: pipeline_spatial_analysis_THDHSH.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots/spatial_analysis
[ -d $OUTPUT_FOLDER/Plots/spatial_analysis ] || python pipeline_spatial_analysis_THDHSH.py $FITTERS $OUTPUT_FOLDER/Plots/spatial_analysis

# ==============================================================================
# pipeline_plot_w_and_wo_Serines.py <FITTERS> <NOS2S_FITTERS>
# ==============================================================================
echo ""
echo "(7) Running: pipeline_plot_w_and_wo_Serines.py"
python pipeline_plot_w_and_wo_Serines.py $FITTERS $FITTERS_NOSS
python pipeline_plot_w_and_wo_Serines.py $FITTERS $FITTERS_NOSS
# ==============================================================================
# End of pipeline
# ==============================================================================
