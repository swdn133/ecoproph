
import argparse
import os
import pandas as pd
import sys
import time

def reduce_dataset_minutes(directory):   
    os.makedirs(directory+"\\minutes", exist_ok=True)
    cnt = 0
    error_cnt = 0
    for filename in os.listdir(directory):
        # only consider the dataset files
        if filename.endswith(".dat"):
            file = os.path.join(directory, filename)
            start = time.time()
            try:
	            with open(file) as f:
	                cnt += 1 # just to track progress
	                header_line = 0
	                for line in f.readlines():
	                    # Find the header_line to parse the csv 
	                    if (line[0:8] == "YYYYMMDD"):
	                        break;  # found header
	                    header_line += 1
	                df = pd.read_csv(file, sep=';\t', dtype={'hhmmss': object}, header=header_line, engine='python')
	                print("{} - {}s".format(cnt, time.time()-start))
	                df['secs'] = df['hhmmss'].astype(str).str[4:]
	                # drop unnecessary 59 seconds - just keep the first second
	                df = df[df.secs == '00']
	                newfile = directory + "\\minutes\\" + filename[:-8] + "_min.csv"
	                print(newfile)
	                # save the resulting file
	                df.to_csv(newfile, sep=';')
            except:
	            print("!!! Unexpected Error:", sys.exc_info()[0])
	            print("FILE: ", file)
	            error_cnt += 1

    return error_cnt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="", help="Path with .dat files")
    args = parser.parse_args()

    assert os.path.isdir(args.path), "Path does not lead to a directory"
    # run the main function
    num_errors = reduce_dataset_minutes(args.path)
    print("Finished with {} Errors!".format(num_errors))