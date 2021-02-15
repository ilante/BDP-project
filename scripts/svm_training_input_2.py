#!/anaconda3/bin/python
import sys
import os
import argparse
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=200)
#linewidth forces np to print each line of the array into one line on term
import time

# To know how long the program takes for each run
start_time = time.time()

def get_ids_list(id_list):
    '''
    Args:(1) id_list - contains ids of profiles and ss_dssp_dirs to be opened
    Returns:
    Rstripped list of ids
    '''
    rstripped_id_list = []
    with open(id_list, 'r') as open_ids:
        all_ids = open_ids.readlines()
        for i in all_ids:
            rstripped_id_list.append(i.rstrip())
    return rstripped_id_list


def add_padding(profile, winsize):
    '''
    Arguments: (1) full path to sequence profile file, (2) winsize must be odd integer.
    Returns:
    padded profile: Padding on 'top' and 'bottom' is d 
    calculated as winsize//2.
    '''
    pro_mat = np.loadtxt(profile)
    pad = (int(winsize)//2)
    pad_mtrx = np.zeros((pad,20))
    padded_profile = np.concatenate((pad_mtrx, pro_mat, pad_mtrx))
    return padded_profile, pad

def obtain_input(dssp_file, profile, winsize, out_file):
    '''
    Arguments: (1) dssp_file full path to ss structure files, 
    (2) full path to profile file,
    (3) windowsize 17 is recomended (and set as default in argparser below).
    (4) full path to output file --> Writes vectorized profiles to a '.svm' file 
    which serves as input to svm-train for libsvm.
    '''
    padded_profile, pad = add_padding(profile, winsize) # unpacking padded pro + pad
    ss_dict = {"H" : "1", "E" : "2", "-" : 3, "C" : 3}    #secondary structure elements as classes

    with open(dssp_file, 'r') as dssp_open, open(out_file, 'a') as svm_out_file:
        for line in dssp_open:
            if line[0] == ">":
                continue
            else:
                ss = line.rstrip()

        # assigning i to ss identifier ('H', 'E', 'C' or '-')
        # assigning j to index of ss in the string
        
        for i, j in zip(ss, range(len(ss))):
            vector_list, feature_index =  [], 0 
            j += (winsize//2)                             # ADJUST according to winsize
            for row_of_window in padded_profile[j-pad:j+1+pad]:
                for feature in row_of_window:
                    feature_index += 1 # for lbsvm: MUST start indexing at value 1
                    if feature == 0:
                        continue
                    else:
                        vector_list.append(str(feature_index)+':'+str(feature))
            joined_vector = ' '.join(vector_list) 
            ss_class = str(ss_dict[i])
            class_and_feature_vector = ss_class+' '+joined_vector+'\n'
            # print(class_and_feature_vector, end='')
            svm_out_file.write(class_and_feature_vector) # appending to svm out file -> generating one large file
    return

# p = '/Users/ila/01-Unibo/00_BDP1/BDP-project/test_files/profiles/d4klia1.profile'
# d= '/Users/ila/01-Unibo/00_BDP1/BDP-project/test_files/dssp/d4klia1.dssp'
# seems to work

# p = '/Users/ila/01-Unibo/00_BDP1/BDP-project/test_files/profiles/microtest.profile'
# d = '/Users/ila/01-Unibo/00_BDP1/BDP-project/test_files/dssp/microtest.dssp'


parser = argparse.ArgumentParser(description='Generates input for libsvm training from dssp like fasta files and their corresponding profile files. \n Output is one line per residue in the profile with the corresponding class of the central residue in column 1. Classes for H,E,C are 1, 2, 3.')
parser.add_argument('-s', '--secondarystructure', metavar='', type=str, required=True, help='Path to "dssp" directory containing all secondary structures in fasta-like format needed.')
parser.add_argument('-p', '--profile', type=str, metavar='', required=True, help='Path to directory containing all profile files needed.')
parser.add_argument('-i', '--ids', type=str, metavar='', required=False, help='Path to file containing IDs of current training set.')
parser.add_argument('-w', '--winsize', type=int,  metavar='', default=17, nargs='?', const=17, help='Window size of the sliding window. Default value = 17. Must be **ODD** numbered integer!') 
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='Path output directory for saving input for libsvm training input. ')
args = parser.parse_args()

if __name__ == "__main__":
    clean_ids = get_ids_list(args.ids)

    for i in clean_ids:
        pro_path = os.path.join(args.profile, i+'.profile')
        dss_path = os.path.join(args.secondarystructure, i+'.dssp')
        if i+'.profile' in os.listdir(args.profile):
            obtain_input(dss_path, pro_path, args.winsize, args.output)
        else: 
            continue
    
    elapsed_seconds = float(time.time() - start_time)
    if elapsed_seconds > 60:
        minutes = elapsed_seconds/60
        print("--- %s minutes ---" % minutes)
    else:
        print("--- %s seconds ---" % (time.time() - start_time))
