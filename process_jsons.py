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
        '-l', '--lengths',
        type=argparse.FileType ('w'),
        help='Write branch length CSV to',
        required = True,
    ) 

    parser.add_argument (
        '-j', '--json',
        type=argparse.FileType ('w'),
        help='Write filetag -> branches under selection JSON here',
        required = True,
    )
     
 
    args = None
    retcode = -1
    args = parser.parse_args()
    
    branches_by_rates    = [0,0,0,0]
    proportions_by_rates = [0,0,0,0]
    significant_results  = []
    corrected_results    = []
    times                = []
    lengths_p            = []
    json_by_file         = {}
    
    
    limiter = 100
    
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            name, ext = os.path.splitext (file)
            if len (ext) > 0 and ext in ('.json'):
                with open (os.path.join (root, file), "r") as fh:
                    try:
                        json_data = json.load (fh)
                        local_counts = [0,0,0,0]
                        
                        tree_string =  json_data["fits"]["Full model"]["tree string"]
                        
                        br_len = [k for k in tree_string.replace ("(",":").replace(")",":").replace(",",":").split (":") if len(k) > 0]
                        br_len_d = {}
                        k = 0
                        while k < len (br_len):
                            br_len_d [br_len[k]] = float (br_len[k+1])
                            k += 2
                            
                        sequences = len (br_len_d)
                        DA=0.5*(json_data["fits"]["Full model"]["AIC-c"]+2*json_data["fits"]["Full model"]["log-likelihood"])
                        DF = json_data["fits"]["Full model"]["parameters"]
                        sites = round(DA*(DF+1)/(DA-DF)) // sequences     
                    
                        
                        file_tag = name.split ('.')
                        file_tag = file_tag [0] + "." + file_tag[2].replace ('0', '')
                        
                        for branch,rates in json_data["fits"]["Full model"]["rate distributions"].items():
                            r = json.loads (rates)
                            local_counts[len (r) - 1] += 1
                            lengths_p.append ([len (r),br_len_d[branch], json_data["test results"][branch]["uncorrected p"], json_data["test results"][branch]["p"], sites, sequences])
                            
                        all = sum (local_counts)
                        for k in range (4):
                            branches_by_rates [k] += local_counts[k]
                            proportions_by_rates [k] += local_counts[k] / all
                    
                        if (local_counts[2] > 0):
                            print (local_counts, file)
                        corrected_results.append (len([1 for test in json_data["test results"].values() if test ["p"] < args.pvalue]))
                        significant_results.append (len([1 for test in json_data["test results"].values() if test ["uncorrected p"] < args.pvalue]))
                        
                        json_by_file [file_tag] = [corrected_results[-1], significant_results[-1]]
                        
                        times.append (json_data["timers"]["overall"])
                        if len (times) > limiter:
                            pass
                            
                    except Exception as e:
                        #print (e)
                        pass
                        
    columns = ['Rates', 'Length', 'RawP', 'CorrectedP', 'Sites', 'Sequences']

    csv_writer = csv.writer (args.lengths)
    csv_writer.writerow (columns)

    for this_row in lengths_p:
       csv_writer.writerow (this_row)

    files = sum (proportions_by_rates)                    
    
    print ("Branches by rate", branches_by_rates)
    print ([k / files for k in proportions_by_rates])
    print ("Raw results", describe_vector(significant_results))
    print ("Selection along at least one branch", len ([k for k in significant_results if k > 0]))
    print ("Corrected results", describe_vector(corrected_results))
    print ("Selection along at least one branch", len ([k for k in corrected_results if k > 0]))
    print ("Run times", describe_vector(times))
    
    json.dump (json_by_file, args.json)
    
    sys.exit(retcode)



