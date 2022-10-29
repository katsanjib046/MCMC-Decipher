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
import os

# import my own module
import cipher

# some constants
LETTERS = string.ascii_lowercase + ' '


def main():
    """
    Main function.
    """
    # check the number of arguments
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python project.py <n_gram> <plain_text_file> <output_file> (optional:<key>)")
        sys.exit(1)
    try:
        n_gram = int(sys.argv[1])
        message_file = os.path.join('test_files', sys.argv[2])
        output_file = os.path.join('output_files', sys.argv[3])
        if len(sys.argv) == 5:
             # Get the key, if any
            try:
                key = sys.argv[4]
                if  len(key) == 1 or len(key) == 2:
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
        else:
            key = None
    except ValueError:
        print("Usage: python project.py <n_gram> <plain_text_file> <output_file> (optional:<key>)")
        sys.exit(1)

    # Get input from the user
    # Get message to be encrypted
    with open(message_file, 'r', encoding='utf8') as f:
        message = f.read().strip().lower()


    # get the cipher text
    cipher_text = encrypt(message, key)

    # Get the start time
    start_time = time.time()

    # Load the text file and return a count matrix
    print('Please wait while we process your request...')
    info = mcmc(cipher_text, message, n_gram=n_gram)

    # Get the end time
    end_time = time.time()

    # Print the time taken
    time_taken = end_time - start_time
    write_output(message, info, output_file, time_taken, n_gram)
    plot_score(info, output_file)
    print('Your request has been processed. Please check the output file.')
    
    


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


def count_matrix_unigram(file=None, text=None):
    """
    Function: To get the count matrix for unigram.
    Input:
        file -- File name
        text -- Text
    Output:
        count_matrix -- Count matrix
    """
    # letters, alphabet
    letters = list(string.ascii_lowercase)
    # Get the count matrix
    count_matrix = np.zeros((len(letters)))
    if file:
        with open(file, 'r', encoding='utf8') as f:
            text = f.read().lower()
    for i in range(len(text)):
        # Get the current letter and the next letter
        current_letter = text[i]
        # Get the index of the current letter and the next letter
        if current_letter in letters:
            current_index = letters.index(current_letter)
            # Increment the count
            count_matrix[current_index] += 1
    return count_matrix


def unigram_attack(cipher_text):
    """
    Function: To get the unigram attack.
    Input:
        cipher_text -- Cipher text
    Output:
        key -- Key
    """
    # Get the count matrix
    count_matrix = count_matrix_unigram(file='wp.txt')
    # Get the count matrix
    count_matrix_message = count_matrix_unigram(text=cipher_text)
    # Get the key
    key = get_key_unigram(count_matrix, count_matrix_message)
    return key


def get_key_unigram(count_matrix, count_matrix_message):
    """
    Function: To get the key for unigram attack.
    Input:
        count_matrix -- Count matrix
        count_matrix_message -- Count matrix for the message
    Output:
        key -- Key
    """
    # letters, alphabet
    letters = list(string.ascii_uppercase)
    # Get the key
    key = [i for i in range(len(letters))]
    # iterate over the count_matrix_message
    for i in range(len(count_matrix_message)):
        # Get the index of the maximum value in the count matrix message
        index_message = np.argmax(count_matrix_message)
        # get the corresponding letter
        letter_message = letters[index_message]
        # Get the index of the maximum value in the count matrix
        index_count_matrix = np.argmax(count_matrix)
        # Get the letter corresponding to the index
        letter_matrix = letters[index_count_matrix]
        # make replacement in the key
        key[index_message] = letter_matrix
        # Make the count matrix message and count matrix zero
        count_matrix_message[index_message] = -(i+1)
        count_matrix[index_count_matrix] = -(i+1)
    key = ''.join(key)
    return key


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


def mcmc(cipher_text, message, n_gram=2):
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
    tau = 1e-4

    # counting number of iterations
    count = 0
    

    info = dict()

    # get a random key
    # key = random_key()
    # get a key using unigram
    key = unigram_attack(cipher_text)

    # get the plain text
    plain_text = decrypt(cipher_text, key)

    # get the score
    score = get_score(plain_text, countMatrix, n_gram=n_gram)
    info[count] = {'iteration': count, 'key': key, 'score': score, 'plain_text': plain_text, 'accuracy': accuracy(plain_text, message)}

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
        
        if count % 5000 == 0:
            info[count] = {
                'iteration': count, 
                'key': key, 
                'score': score, 
                'plain_text': plain_text, 
                'accuracy': accuracy(plain_text, message)}

    info[count] = {
                'iteration': count, 
                'key': key, 
                'score': score, 
                'plain_text': plain_text, 
                'accuracy': accuracy(plain_text, message)}

    # return the plain text
    return info


def plot_score(info, file_name):
    """
    Function: To plot the score list.
    Input:
        score_list -- List of scores
    Output:
        None
    """
    # get the file name before the extension
    file_name = file_name.split('.')[0]
    # Get the score list
    score_list = [info[i]['score'] for i in info]
    # Plot the score list
    plt.plot(score_list)
    plt.xlabel('Iteration (*5000)')
    plt.ylabel('Score')
    plt.savefig(file_name + '_score.png')

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

def write_output(message, info, file_name, time_taken, n_gram):
    """
    Function: To write the output to a file.
    Input:
        message -- Message
        plain_text -- Plain text
        file_name -- File name
        time_taken -- Time taken
    Output:
        None
    """
    # Write the output to a file
    with open(file_name, 'w') as f:
        f.write('message: ' + message + '\n')
        f.write('time taken: ' + str(time_taken) + '\n')
        f.write('n_gram: ' + str(n_gram) + '\n')
        f.write('Iteration, Key, Score, Accuracy, Plain Text')
        for keys in info.keys():
            f.write('\n')
            f.write(str(info[keys]['iteration']) + ',')
            f.write(info[keys]['key'] + ',')
            f.write(str(info[keys]['score']) + ',')
            f.write(str(info[keys]['accuracy'])+ ',')
            f.write(info[keys]['plain_text'])


# ------------------ Testing and Running ------------------
if __name__ == '__main__':
    main()

