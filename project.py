# File: project.py
"""
Module: Implementation of MCMC on Cryptography.
Probability matrix is calculated using war and peace.
Contains functions:
    - main
"""

# Importing libraries
import numpy as np
import random
import string
import time


def main():
    # Load the text file, which is war and peace
    with open('wp.txt', 'r', encoding='utf8') as file:
        data = file.read()
        print(data)





# ------------------ Testing and Running ------------------
if __name__ == '__main__':
    main()

