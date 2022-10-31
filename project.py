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
import collections as c

# import my own module
import cipher

# some constants
LETTERS = string.ascii_lowercase + ' '


def main(argv=None, multiple=False):
    """
    Main function.
    Gets the input from the user and calls the required functions.
    The final output are written to a file.
    """
    if argv is None:
        argv = sys.argv
    
    # check the number of arguments
    if len(argv) != 4 and len(argv) != 5:
        print("Usage: python project.py <n_gram> <plain_text_file> <output_file> (optional:<key>)")
        sys.exit(1)
    try:
        n_gram = int(argv[1])
        message_file = os.path.join('test_files', argv[2])
        output_file = os.path.join('output_files', argv[3])
        if len(argv) == 5:
             # Get the key, if any
            try:
                key = argv[4]
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
    
    # return the info if multiple is true
    if multiple:
        return info, time_taken
    else:
        write_output(message, info, output_file, time_taken, n_gram)
        plot_score(info, output_file, n_gram)
    print('Your request has been processed. Please check the output file.')
    
    
def chunker(seq, size):
    """
    Function: To split a string into chunks of a given size.
    Input:
        seq -- String
        size -- Size
    Output:
        chunk -- Chunk
    """
    return [''.join(seq[pos:pos + size]) for pos in range(0, len(seq)-size+1)]


def count_matrix(file=None, text=None, n_gram=2):
    """
    Function: 
        To count the number of times a letter is followed by another letter in a given text file.
    Input:
        file -- Text file
        text -- Text
        n_gram -- n_gram
    Output: 
        count_dict -- Count dictionary
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

    # create a list of all the letters in the text
    letters_list = [letter.lower() for letter in text if letter.isalpha() or letter == ' ']

    # make chuncks of 2 letters
    chunks = chunker(letters_list, n_gram)

    # create a dictionary of all the letters and their counts
    count_dict = c.Counter(chunks)

    return count_dict


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
    currentMatrix = count_matrix(text=plain_text, n_gram=n_gram)
    for key in currentMatrix.keys():
        if key in probMatrix.keys():
            score += (1+currentMatrix[key]) * np.log(1+probMatrix[key])

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
    countMatrix = count_matrix(file='wp.txt', n_gram=n_gram)
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
    key = random_key()

    # get the plain text
    plain_text = decrypt(cipher_text, key)


    # get the score
    score = get_score(plain_text, countMatrix, n_gram=n_gram)
    info[count] = {'iteration': count, 'key': key, 'score': score, 'plain_text': plain_text, 'accuracy': accuracy(plain_text, message)}

    # keep the best
    best = {
        'key': key,
        'plain_text': plain_text,
        'score': score,
        'accuracy': accuracy(plain_text, message)
    }

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
            if score > best['score']:
                best['key'] = key
                best['plain_text'] = plain_text
                best['score'] = score
                best['accuracy'] = accuracy(plain_text, message)   
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
                'accuracy': accuracy(plain_text, message),
                }
    info['best'] = best

    # return the plain text
    return info


def plot_score(info, file_name,n_gram=2):
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
    # score_list = [info[i]['score'] for i in info]
    # get the accuracy list
    accuracy_list = [info[i]['accuracy'] for i in info]
    # Plot the score list
    plt.plot(accuracy_list, label='n_gram={}'.format(n_gram))
    plt.xlabel('Iteration (*5000)')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Vs Iteration for different n_grams')
    plt.legend()
    plt.savefig(file_name + '_accuracy.png')



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
    with open(file_name, 'a+') as f:
        f.write('message: ' + message + '\n')
        f.write('time taken: ' + str(time_taken) + '\n')
        f.write('n_gram: ' + str(n_gram) + '\n')
        f.write('Iteration, Key, Score, Accuracy, Plain Text')
        for keys in list(info.keys())[:-1]:
            f.write('\n')
            f.write(str(info[keys]['iteration']) + ',')
            f.write(info[keys]['key'] + ',')
            f.write(str(info[keys]['score']) + ',')
            f.write(str(info[keys]['accuracy'])+ ',')
            f.write(info[keys]['plain_text'])
        f.write('\n\n')
        f.write('Best Key: ' + info['best']['key'] + '\n')
        f.write('Best Score: ' + str(info['best']['score']) + '\n')
        f.write('Best Accuracy: ' + str(info['best']['accuracy']) + '\n')
        f.write('Best Plain Text: ' + info['best']['plain_text'])
        f.write('\n\n\n')   


# ------------------ Testing and Running ------------------
if __name__ == "__main__":
    main()

