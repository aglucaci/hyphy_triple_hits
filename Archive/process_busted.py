import re, sys, csv, argparse, json, os

def float01 (value):
    fvalue = float(value)
    if fvalue < 0. or fvalue > 1.:
         raise argparse.ArgumentTypeError("%s is an invalid rate " % value)
    return fvalue

def describe_vector (vector):
    vector.sort()
    l = len (vector)
    return {'count': l, 'min': vector[0], 'max': vector[-1], 'mean': sum(vector)/l, 'median':  vector [l//2] if l % 2 == 1 else 0.5*(vector[l//2-1]+vector[l//2]), "IQR": [vector [l//4], vector [(3*l)//4]] }

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='describe BUSTED p-values from a set of runs'
    )
 
    parser.add_argument (
        '-d', '--directory',
        type=str,
        help='Scan this directory',
        required = True,
    ) 
    
    parser.add_argument (
        '-p', '--pvalue',
        type=float01,
        help='Bin based on this p-value cutoff',
        required = True,
    ) 

    parser.add_argument (
        '-j', '--json',
        type=argparse.FileType ('w'),
        help='Write analysis information as JSON here',
        required = False,
    ) 

    parser.add_argument (
        '-c', '--csv',
        type=argparse.FileType ('w'),
        help='Write analysis information as CSV here',
        required = False,
    ) 
    
    parser.add_argument (
        '-m', '--meme',
        type=argparse.FileType ('w'),
        help='Compare to MEME results and tabulate p-values vs evidence ratios here',
        required = False,
    ) 
     
    parser.add_argument (
        '-s', '--single',
        default = False,
        action='store_true'
    ) 

    parser.add_argument (
        '-b', '--batch',
        default = False,
        action='store_true'
    ) 
     
    args = None
    retcode = -1
    args = parser.parse_args()
    
    json_by_file         = {}
    by_directory         = {}
     
    limiter = 100
    
    if args.meme:
        comparison = csv.writer(args.meme, delimiter=',')
        comparison.writerow (['Site','MEME','BUSTED_constrained','BUSTED_null'])
   
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            name, ext = os.path.splitext (file)
            if len (ext) > 0 and ext in ('.json'):
                if root not in by_directory:
                    if args.single and len (by_directory):
                        continue
                        
                    by_directory[root] = {'hits' : [], 'times' : []}
                            
                            
                with open (os.path.join (root, file), "r") as fh:
                    try:
                        json_data = json.load (fh)                        
                        rate_disrtibution =  sorted(json_data["fits"]["Unconstrained model"]["rate distributions"]["FG"], key=lambda record: record[0])
                                                        
                        tree_string =  json_data["fits"]["Unconstrained model"]["tree string"]
                        br_len = [k for k in tree_string.replace ("(",":").replace(")",":").replace(",",":").split (":") if len(k) > 0]                            
                        sequences = len (br_len) / 2


                        file_tag = name.split ('.')
                        file_tag = file_tag [0] + "." + file_tag[2].replace ('0', '')
                        
                        p_value = json_data["test results"]["p"]
                        by_directory[root]['hits'].append (p_value)
                        
                        if args.json or args.csv:
                            json_by_file [file_tag] = {"p" : p_value, "sequences": sequences , "max_omega" : rate_disrtibution[-1][0], "max_omega_weight": rate_disrtibution[-1][1], "L": json_data["fits"]["Unconstrained model"]["tree length"], "sites": len (json_data["profiles"]["unconstrained"][0])}
                        
                        by_directory[root]['times'].append (json_data["timers"]["overall"])
                        
                        if args.meme:
                            #find the meme file 
                            trunk, dump = os.path.splitext (name)
                            
                            ers = json_data['evidence ratios'] if 'evidence ratios' in json_data else None
                            
                            meme_csv = trunk + ".meme.csv"
                            
                            if ers:
                                with open (os.path.join (root, meme_csv), "r") as meme_file:
                                    meme_reader = csv.reader (meme_file)
                                    next (meme_reader)
                                    for i,l in enumerate(meme_reader):
                                        comparison.writerow ([str(i+1), l[6], ers['constrained'][0][i] if ers else 'N/A', ers['optimized null'][0][i] if ers else 'N/A'])
                                
                                
                            
                    except Exception as e:
                        #print (e)
                        pass
                    
    if args.json:                    
        json.dump (json_by_file, args.json)
    
    if args.csv:
        csv_dump = csv.writer(args.csv, delimiter=',')
        rows = ['p', 'sites', 'sequences', 'L', 'max_omega', 'max_omega_weight']
        csv_dump.writerow (['File'] + rows)
        for file, data in json_by_file.items():
           csv_dump.writerow ([file] + [data[k] for k in rows]) 
            
        
    for dir, data in iter (sorted (by_directory.items(), key = lambda record: record [0])):
        print ("%s,%d,%.4f" % (dir, len (data['hits']), len ([k for k in data['hits'] if k <= args.pvalue]) / len (data['hits'])))
        
        
    #print ("p-values", describe_vector(significant_results))
    #sc = len ([k for k in significant_results if k <= args.pvalue])
    #print ("significant results %d / %g %%" % (sc, sc / len (significant_results) * 100))
    #print ("Run times", describe_vector(times))
    
    
    sys.exit(retcode)



