import numpy as np
import sys
from numpy import savetxt # do I really need that?
import pandas as pd
import os
import glob

# Remember style matters: https://github.com/ilante/python-cheatsheet#style-matters
# my_funct, my_var MY_CONSTANT MyClass

def make_libsvm_input(id_file, profiledir, dsspdir, ws): #, ws, odir
    '''
    Input (1) id_file, (2) profile directory, (3) dssp directory, (4) window size (5) out directory.
    '''
    with open(id_file, 'r') as ids:
        id_list = ids.readlines() # List of all ids
        # looping on id list
        for i in id_list:
            # removing trailing \n
            seqid=i.rstrip() 
            propath = os.path.join(profiledir, seqid+'.profile') #joining paths for profile
            sspath = os.path.join(dsspdir, seqid+'.dssp') #joining paths for dssp SS file
            # print('profile ', propath, '\n', 'ss ', sspath)
            with open(propath, 'r') as profile, open(sspath, 'r') as ssfile:
                prolines = profile.readlines() #list of prolines
                sslines = ssfile.readlines()[1].rstrip() #list of ss only (ditching line 0 = id)
                
                svm_lines = []
                # Creating np arr containing indecis of the residue
                arr_indx = np.zeros((ws,20))
                ind = 1
                for i in range(ws):
                    for j in range(20):
                        arr_indx[i,j]=int(ind)
                        ind += 1 # increment by 1
                arr_indx = arr_indx.astype(int)
                # print(arr_indx)
                
                line_list = []
                for line in range(0, len(prolines)):
                    if sslines[line] == 'H':
                        line_list.append(1)
                    elif sslines[line] == 'E':
                        line_list.append(2)
                    else:
                        line_list.append(3) # works for 'C' and '-'
                    lindex = -1
                    for i in range(((ws-1)//2),-((ws-1)//2)-1,-1): # in our case -8 to + 8
                        lindex += 1
                        print(lindex)
                        # if (line-i) >= 0 and (line-i) < len(prolines):

    return

test_ids = '/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/cv_ids_clean/testing/test_set4'

# test_ids = '/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/test_cv_ids/train4'

propath = '/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/seqprofile_training/'
spath = '/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/dssp/'
make_libsvm_input(test_ids, propath, spath, 3)