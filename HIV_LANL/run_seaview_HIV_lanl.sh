clear

SEAVIEW="/Users/alex/Documents/TRIPLE_HITS/seaview4/seaview.app/Contents/MacOS/seaview"
DATADIR="/Users/alex/Documents/TRIPLE_HITS/Preprocessing/HIVDB-2017-DNA/HIV1-2017-Filtered/ForHyphy/"


echo "Starting to generate BioNJ trees from alignments"
echo "SEAVIEW APP: "$SEAVIEW
echo "DATA DIRECTORY: "$DATADIR
echo "Number of files:"$(ls "$DATADIR" | wc -l)


for f in "$DATADIR"*.fasta
do
    echo "Processing $f file..."
    base="${f##*/}"
    OUTPUT="/Users/alex/Documents/TRIPLE_HITS/Preprocessing/HIVDB-2017-DNA/HIV1-2017-Filtered/ForHyphy/BioNJ/"$base"-BioNJ_tree.nwk"
    $SEAVIEW -build_tree -distance observed -o "$OUTPUT" "$f"
done
	


