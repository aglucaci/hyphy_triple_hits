import os, argparse, subprocess, re, sys


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='scan the directory of NGS files and process them'
    )
    parser.add_argument(
        '-a', '--alignments',
        type=str,
        help='the directory that contains sequence alignments',
        required=True,
    )
    

    args = parser.parse_args()
    
    numbers = re.compile ("^\.[0-9]+$")

    for root, dirs, files in os.walk(args.alignments):
        for each_file in files:
            name, ext = os.path.splitext(each_file)
            if len(ext) > 0 and ext in ['.mt', '.nex'] or numbers.match (ext)  :
                existing = os.path.join (args.alignments, name + ext + ".FITTER.json")
                if not os.path.isfile (existing):
                    file = os.path.join (root, name + ext)
                    gen_code = 'Universal' if ext != '.mt' else 'Vertebrate mtDNA'
                    print (file, gen_code)
                    subprocess.run (["qsub", "-V", "-l walltime=240:00:00 h=!n6&!n7&!n8&!n5'"], input = ('/home/swisotsky/bin/hyphy-dev/hyphy/HYPHYMP LIBPATH=/home/swisotsky/bin/hyphy-dev/hyphy/res/ /home/swisotsky/bin/hyphy-dev/hyphy/res/TemplateBatchFiles/SelectionAnalyses/FitMultiModel.bf "%s" %s' % (gen_code, file)), universal_newlines = True)
                else:
                    print ("CACHED %s" % existing)

    

    sys.exit(0)
