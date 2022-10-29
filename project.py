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
    # check the number of arguments
    if len(sys.argv) != 2:
        print("Usage: python project.py <n_gram>")
        sys.exit(1)
    try:
        n_gram = int(sys.argv[1])
    except ValueError:
        print("Usage: python project.py <n_gram>")
        sys.exit(1)

    # Get input from the user
    # Get message to be encrypted
    message = input('Enter the message: ')
    if len(message) == 0:
        message = 'I am the king of the world'
        message = message + ' '
        message = message.lower()
        message = message * 10

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
    plain_text, score_list = mcmc(cipher_text, n_gram=n_gram)

    # Get the end time
    end_time = time.time()

    # Print the time taken
    print('Time taken to decrypt the message: ', end_time - start_time)
    print('Cipher text: ', cipher_text)
    print('Plain text: ', plain_text)
    plot_score(score_list)
    # print(probMatrix)
    # print the accuracy
    print('Accuracy: ', accuracy(plain_text, message))
    


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


def get_score(plain_text, probMatrix, n_gram=2):
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
    letters = list(LETTERS)
    score = 0
    if n_gram == 2:
        currentMatrix = count_matrix(text=plain_text)
        for i in range(len(plain_text)-1):
            # Get the current letter and the next letter
            current_letter = plain_text[i]
            next_letter = plain_text[i + 1]
            # Get the index of the current letter and the next letter
            current_index = letters.index(current_letter)
            next_index = letters.index(next_letter)
            # Increment the score
            score += (1+currentMatrix[current_index, next_index]) * np.log(1+probMatrix[current_index, next_index])
    elif n_gram == 3:
        currentMatrix = count_matrix_trigram(text=plain_text)
        for i in range(len(plain_text)-2):
            # Get the current letter and the next letter
            current_letter = plain_text[i]
            next_letter = plain_text[i + 1]
            third_letter = plain_text[i + 2]
            # Get the index of the current letter and the next letter
            current_index = letters.index(current_letter)
            next_index = letters.index(next_letter)
            third_index = letters.index(third_letter)
            # Increment the score
            score += (1+currentMatrix[current_index, next_index, third_index]) * np.log(1+probMatrix[current_index, next_index, third_index])
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


def mcmc(cipher_text, n_gram=2):
    """
    Function: Given a cipher_text and prob_matrix, it tries to decrypt the message.
    Input:
        cipher_text -- cipher text to be decrypted
        prob_matrix -- prob_matrix computed based on the count_matrix for the given text
    
    Output:
        plain_text -- decrypted plain text
    """
    # get the count matrix for reference text
    print("Getting the count matrix for reference text...")
    if n_gram == 2:
        countMatrix = count_matrix(file='wp.txt')
    elif n_gram == 3:
        countMatrix = count_matrix_trigram(file='wp.txt')
    print("Count matrix for reference text is ready.")
    # regulating temperature
    Tmax = 1000
    T = Tmax
    Tmin = 1
    # regulating cooling rate
    tau = 1e-5

    # counting number of iterations
    count = 0
    

    score_list = []

    # get a random key
    key = random_key()

    # get the plain text
    plain_text = decrypt(cipher_text, key)

    # get the score
    score = get_score(plain_text, countMatrix, n_gram=n_gram)
    score_list.append(score)

    # loop until the temperature is less than the minimum temperature
    while T > Tmin:
        count += 1
        T = Tmax * np.exp(-tau * count)
        # get a new key
        new_key = get_new_key(key)

        # get the new plain text
        new_plain_text = decrypt(cipher_text, new_key)

        # get the new score
        new_score = get_score(new_plain_text, countMatrix, n_gram=n_gram)

        # get the difference in score
        diff =   new_score - score
        if diff >= 0:
            key = new_key
            plain_text = new_plain_text
            score = new_score
        else:
            prob = np.exp(diff / T)
            if random.random() < prob:
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
    print(score_list[-10:])

def matrix_info(matrix):
    """
    Function: To print the matrix information.
    Input:
        matrix -- Matrix
    Output:
        None
    """
    # Print the matrix information
    print('Matrix shape: ', matrix.shape)
    print('Matrix sum: ', matrix.sum())
    print('Matrix max: ', matrix.max())
    print('Matrix min: ', matrix.min())


def accuracy(given_text, predicted_text):
    """
    Function: To get the accuracy.
    Input:
        given_test -- Given test
        predicted_test -- Predicted test
    Output:
        accuracy -- Accuracy
    """
    # Get the accuracy
    accuracy = 0
    for i in range(len(given_text)):
        if given_text[i] == predicted_text[i]:
            accuracy += 1
    accuracy = accuracy / len(given_text)
    return accuracy

def count_matrix_trigram(file=None, text=None):
    """
    Function: To get the count matrix for trigram.
    Input:
        file -- File name
        text -- Text
    Output:
        count_matrix -- Count matrix
    """
    # letters, alphabet
    letters = list(LETTERS)
    # Get the count matrix
    count_matrix = np.zeros((len(letters), len(letters), len(letters)))
    if file:
        with open(file, 'r', encoding='utf8') as f:
            text = f.read().lower()
    for i in range(len(text)-2):
        # Get the current letter and the next letter
        current_letter = text[i]
        next_letter = text[i + 1]
        next_next_letter = text[i + 2]
        # Get the index of the current letter and the next letter
        if current_letter in letters and next_letter in letters and next_next_letter in letters:
            current_index = letters.index(current_letter)
            next_index = letters.index(next_letter)
            next_next_index = letters.index(next_next_letter)
            # Increment the count
            count_matrix[current_index, next_index, next_next_index] += 1
    return count_matrix


# ------------------ Testing and Running ------------------
if __name__ == '__main__':
    main()

