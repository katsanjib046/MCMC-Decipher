# File: project.py
"""
Module: Implementation of MCMC on Cryptography.
Probability matrix is calculated using war and peace by Leo Tolstoy.
Contains functions:
    - main
    - count_matrix
    - probability_matrix
    - random_key
"""

# Importing external libraries
import numpy as np
import random
import string
import time
import sys
import matplotlib.pyplot as plt

# import my own module
import cipher

# some constants
LETTERS = string.ascii_lowercase + ' '


def main():
    """
    Main function.
    """

    # Get input from the user
    # Get message to be encrypted
    message = input('Enter the message: ')

    # Get the key, if any
    try:
        key = input('Enter the key. Press Enter for RandomCipher: ')
        if key == '':
            key = None
        elif  len(key) == 1 or len(key) == 2:
            try:
                key = int(key)
                if not 0 < key < 26:
                    raise ValueError 
            except ValueError:
                raise ValueError
        elif len(key) != 26:
            raise ValueError
    except ValueError:
        print('Invalid key')
        sys.exit(1)


    # get the cipher text
    cipher_text = encrypt(message, key)

    # Get the start time
    start_time = time.time()

    # Load the text file and return a count matrix
    print('Thanks for your patience. 😊')
    print('Processing...')
    countMatrix = count_matrix('wp.txt')
    probMatrix = probability_matrix(countMatrix)
    plain_text, score_list = mcmc(cipher_text, countMatrix)

    # Get the end time
    end_time = time.time()

    # Print the time taken
    print('Time taken to decrypt the message: ', end_time - start_time)
    print('Cipher text: ', cipher_text)
    print('Plain text: ', plain_text)
    plot_score(score_list)
    # print(probMatrix)
    


def count_matrix(file=None, text=None):
    """
    Function: 
        To count the number of times a letter is followed by another letter in a given text file.
    Input:
        file -- Text file
    Output: 
        count_matrix -- Count matrix
    """
    # letters, alphabet, and space
    letters = LETTERS

    if file is not None:
        # Open the file
        with open(file, 'r', encoding='utf8') as f:
            # Read the file
            text = f.read().lower()
    elif text is not None:
        text = text.lower()

    # Initialize the count matrix
    count_matrix = np.zeros((len(letters), len(letters)))

    # Loop through the text
    for i in range(len(text) - 1):
        # Get the current letter and the next letter
        current_letter = text[i]
        next_letter = text[i + 1]

        # Get the index of the current letter and the next letter
        if current_letter in letters:
            current_index = letters.index(current_letter)
            if next_letter in letters:
                next_index = letters.index(next_letter)

                # Increment the count matrix
                count_matrix[current_index, next_index] += 1

    # Return the count matrix
    return count_matrix


def probability_matrix(count_matrix):
    """
    Function: 
        To calculate the probability matrix.
    Input:
        count_matrix -- Count matrix
    Output: 
        probability_matrix -- Probability matrix
    """
    # Get the sum of each row
    row_sums = count_matrix.sum(axis=1)

    # Divide each row by the sum of the row
    probability_matrix = count_matrix / row_sums[:, np.newaxis]

    # Return the probability matrix
    return probability_matrix


def random_key():
    """
    Function: 
        To generate a random Solution key.
    Input:
        None
    Output: 
        key -- Random key
    """
    # letters, alphabet
    letters = list(string.ascii_uppercase)

    # Shuffle the letters
    random.shuffle(letters)

    # Return the key
    letters = ''.join(letters)
    return letters


def encrypt(message, key=None):
    """
    Function: 
        To encrypt the message.
    Input:
        message -- Message to be encrypted
        key -- Key to encrypt the message
    Output: 
        cipher_text -- Encrypted message
    """
    # letters, alphabet
    letters = list(string.ascii_uppercase)

    # get a cipher class
    if key is None:
        cipher_class = cipher.RandomCipher()
    elif type(key)==str:
        cipher_class = cipher.SubstitutionCipher(key)
    else:
        cipher_class = cipher.CaeserCipher(key)


    # Encrypt the message
    cipher_text = cipher_class.encrypt(message)

    # Return the cipher text
    return cipher_text


def decrypt(message, key=None):
    """
    Function: 
        To decrypt the message.
    Input:
        message -- Message to be decrypted
        key -- Key to decrypt the message
    Output: 
        plain_text -- Decrypted message
    """
    # letters, alphabet
    letters = list(string.ascii_uppercase)

    # get a cipher class
    if type(key) == str:
        cipher_class = cipher.SubstitutionCipher(key)
    elif type(key) == int:
        cipher_class = cipher.CaeserCipher(key)
    else:
        raise NotImplementedError

    # Decrypt the message
    plain_text = cipher_class.decrypt(message)

    # Return the plain text
    return plain_text


def get_score(plain_text, probMatrix):
    """
    Function:
        To get the score of the plain text.
    Input:
        plain_text -- Plain text
        probMatrix -- Probability matrix
    Output:
        score -- Score of the plain text
    """
    # letters, alphabet
    letters = list(string.ascii_lowercase + ' ')
    score = 0
    currentMatrix = count_matrix(text=plain_text)
    for i in range(len(plain_text)-1):
        # Get the current letter and the next letter
        current_letter = plain_text[i]
        next_letter = plain_text[i + 1]
        # Get the index of the current letter and the next letter
        if current_letter.lower() in letters:
            current_index = letters.index(current_letter)
            if next_letter.lower() in letters:
                next_index = letters.index(next_letter)
                # Increment the score
                score += (1+currentMatrix[current_index, next_index]) * np.log(1+probMatrix[current_index, next_index])
    return score

def get_new_key(key):
    """
    Function:
        To get a new key.
    Input:
        key -- Current key
    Output:
        new_key -- New key
    """
    # letters, alphabet
    letters = list(string.ascii_uppercase)
    # Get the index of the letters
    index1 = random.randint(0, 25)
    index2 = random.randint(0, 25)
    # Get the new key
    new_key = list(key)
    # random swap
    new_key[index1], new_key[index2] = new_key[index2], new_key[index1]
    new_key = ''.join(new_key)
    return new_key


def mcmc(cipher_text, prob_matrix):
    """
    Function: Given a cipher_text and prob_matrix, it tries to decrypt the message.
    Input:
        cipher_text -- cipher text to be decrypted
        prob_matrix -- prob_matrix computed based on the count_matrix for the given text
    
    Output:
        plain_text -- decrypted plain text
    """
    # regulating temperature
    Tmax = 10000
    T = Tmax
    Tmin = 0.1
    # regulating cooling rate
    alpha = 0.99

    # counting number of iterations
    count = 0
    

    score_list = []
    # letters, alphabet
    letters = list(string.ascii_uppercase)

    # get a random key
    key = random_key()

    # get the plain text
    plain_text = decrypt(cipher_text, key)

    # get the score
    score = get_score(plain_text, prob_matrix)
    score_list.append(score)

    # loop for N times
    while T > Tmin:
        count += 1
        # get a new key
        new_key = get_new_key(key)

        # get the new plain text
        new_plain_text = decrypt(cipher_text, new_key)

        # get the new score
        new_score = get_score(new_plain_text, prob_matrix)

        # get the difference in score
        diff =   new_score - score
        if diff > 0:
            key = new_key
            plain_text = new_plain_text
            score = new_score
        else:
            T = Tmax * alpha ** count
            prob = np.exp(diff/T)
            if prob < random.random():
                key = new_key
                plain_text = new_plain_text
                score = new_score
        if count % 100 == 0:
            score_list.append(score)

    # return the plain text
    return plain_text, score_list


def plot_score(score_list):
    """
    Function: To plot the score list.
    Input:
        score_list -- List of scores
    Output:
        None
    """
    # Plot the score list
    plt.plot(score_list)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.show()
    print(score_list[:10])




# ------------------ Testing and Running ------------------
if __name__ == '__main__':
    main()

