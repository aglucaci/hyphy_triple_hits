PERL=/home/martink/bin/perl
TABLEVIEWER_DIR=/home/martink/work/circos/svn/tools/tableviewer
CIRCOS_DIR=/home/martink/work/circos/svn-tags/circos-tableviewer/
WORKING_DIR=/home/martink/www/htdocs/tableviewer/tmp/akqrbmn
cd /home/martink/www/htdocs/tableviewer/tmp/akqrbmn
$PERL $TABLEVIEWER_DIR/bin/parse-table -conf etc/parse-table.conf -file uploads/table.txt -segment_order=ascii,size_desc -placement_order=row,col -interpolate_type count -color_source row -transparency 1 -fade_transparency 0 -ribbon_layer_order=size_asc > data/parsed.txt
cat data/parsed.txt | $TABLEVIEWER_DIR/bin/make-conf -dir data
$PERL $CIRCOS_DIR/bin/circos -param random_string=akqrbmn -conf etc/circos.conf
cd /home/martink/www/htdocs/tableviewer/tmp/akqrbmn; /home/martink/bin/perl /home/martink/work/circos/svn-tags/circos-tableviewer//bin/circos -param random_string=akqrbmn -conf /home/martink/www/htdocs/tableviewer/tmp/akqrbmn/etc/circos.conf 2>&1 > /home/martink/www/htdocs/tableviewer/tmp/akqrbmn/results/report.txt
tar cvfz circos-tableviewer-akqrbmn.tar.gz *
