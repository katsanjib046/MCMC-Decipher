# File: multiple_run.py
"""
Module: Implementation of MCMC on Cryptography. This file runs the mcmc several times and keeps the data.
Contains functions:
    - main
    - multiple_run
    - plot
"""

# imports
import project
import cipher
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time


def main(argv, runs=100):
    """
    Main function.
    """
    data = multiple_run(argv, runs)
    # save the data
    with open(os.path.join('output_files', argv[3]), 'a') as f:
        f.write('\n')
        f.write(f'{data["message"]},{data["length"]},{data["n_gram"]},{data["average_time"]},{data["average_accuracy"]},{data["num_success"]},{data["runs"]}')

def multiple_run(argv, runs):
    """
    Function: This function runs the main function of project.py several times to get statistics.
    inputs:
        - runs: number of times the algorithm is run.
    outputs:
        - None
    """
    total_time = 0
    num_success = 0
    sum_of_accuracy = 0
    # open the argument to get the message
    with open(os.path.join('test_files',argv[2]), 'r', encoding='utf8') as f:
        message = f.read().strip().lower()

    for i in range(runs):
        print(f'run {i}')
        info, time_taken = project.main(argv, multiple=True)
        total_time += time_taken
        # check the accuracy for this run
        if info['best']['accuracy'] == 1:
            num_success += 1
        # total accuracy
        sum_of_accuracy += info['best']['accuracy']



    # find the average time taken    
    average_time = total_time / runs
    # find the average accuracy
    average_accuracy = sum_of_accuracy / runs
    # length of the plain text
    length = len(info['best']['plain_text'])
    # n_gram used
    n_gram = argv[1]

    data = {
        'message': message[:60] + '...' if len(message) > 60 else message,
        'average_time': average_time,
        'average_accuracy': average_accuracy,
        'length': length,
        'n_gram': n_gram,
        'num_success': num_success,
        'runs': runs
    }

    # return the data
    return data

###### testing and running ########
if __name__ == '__main__':
    for j in [1,3,4]:
        print(f'running for file {j}')
        for i in range(1,6):
            print(f'running for n_gram {i}')
            main(['project.py', str(i), 'test'+str(j)+'.txt' ,'data.csv'], runs=10)