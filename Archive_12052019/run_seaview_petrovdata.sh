clear


SEAVIEW="/Users/phylo/Downloads/seaview4/seaview.app/Contents/MacOS/seaview"
DATADIR="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/"
SAMPLE_DATA="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/ENSG00000267796.fa"


echo "Starting to generate BioNJ trees from alignments"

echo "SEAVIEW APP: "$SEAVIEW

echo "DATA DIRECTORY: "$DATADIR

echo "Number of files:"$(ls "$DATADIR" | wc -l)

#echo "DEBUG - TRYING ONE"
#touch OUTPUT-BioNJ_tree
#echo "COMMAND: $SEAVIEW $SAMPLE_DATA -build_tree -o poop.tree -distance observed -NJ "


for f in "$DATADIR"*.fa
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  #cat $f
  #OUTPUT="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/ENSG00000267796-BioNJ_tree"
  
  base="${f##*/}"

  #BioNJ TREE

  #OUTPUT="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/Trees/BioNJ/"$base"-BioNJ_tree"
  #$SEAVIEW -build_tree -distance observed -o "$OUTPUT" "$SAMPLE_DATA"

  #NJ TREE

  OUTPUT="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/Trees/NJ/"$base"-NJ_tree"
  $SEAVIEW -build_tree -distance observed -NJ -o "$OUTPUT" "$SAMPLE_DATA"

done



#OUTPUT="/Users/phylo/Documents/Pond Lab/bestrecip_prank_alignments/ENSG00000267796-BioNJ_tree"
#$SEAVIEW -build_tree -distance observed -NJ -o "$OUTPUT" "$SAMPLE_DATA"





#echo "DONE"
