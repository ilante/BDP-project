#!/bin/bash

#####################################################################################################
# Script for generating input for libsvm runs the python script 'svm_training_input_2.py'           #
#####################################################################################################
# Generates input for libsvm training from dssp like fasta files and their
# corresponding profile files. Output is one line per residue in the profile
# with the corresponding class of the central residue in column 1. Classes for
# H,E,C are 1, 2, 3.
###########################################################################################
# optional arguments:
#   -h, --help            show this help message and exit
#   -s , --secondarystructure 
#                         Path to "dssp" directory containing all secondary
#                         structures in fasta-like format needed.
#   -p , --profile        Path to directory containing all profile files needed.
#   -i , --ids            Path to file containing IDs of current training set.
#   -w [], --winsize []   Window size of the sliding window. Default value = 17.
#                         Must be **ODD** numbered integer!
#   -o , --output         Path output directory for saving input for libsvm
#                         training input.

for i in {0..1}
do
    # Variables:
    ids_1="/Users/ila/01-Unibo/00_BDP1/BDP-project/test_jobs_svm_input/ids_train/ids_tiny_train_job_${i}"
    ids_2="/Users/ila/01-Unibo/00_BDP1/BDP-project/test_jobs_svm_input/ids_test/ids_tiny_test_job_${i}"
    profile_path="/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/seqprofile_training"
    ss_path="/Users/ila/01-Unibo/archive/02_Lab2/files_lab2_project/all_data/trainingset/dssp"
    o1="/Users/ila/01-Unibo/00_BDP1/BDP-project/test_jobs_svm_input/in_train/train${i}.svm"
    o2="/Users/ila/01-Unibo/00_BDP1/BDP-project/test_jobs_svm_input/in_test/test${i}.svm"
    /Users/ila/01-Unibo/00_BDP1/BDP-project/scripts/svm_training_input_2.py -i ${ids_1} -p ${profile_path} -s ${ss_path} -o ${o1}
    /Users/ila/01-Unibo/00_BDP1/BDP-project/scripts/svm_training_input_2.py -i ${ids_2} -p ${profile_path} -s ${ss_path} -o ${o2}
done
