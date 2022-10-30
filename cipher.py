# File cipher.py Implementing substitution ciphers

""" Module cipher: contains substitution cipher class. Caeser Cipher and Random Cipher are implemented as
subclasses.
"""

################# Necessary Imports ##################

import random



################ Substitution Cipher #################

class SubstitutionCipher:
    """A class that takes 26 uppercase characters in arbitrary order, passed as a string: 'ABC...', and uses that for encoding
    and decoding messages.
    """
    def __init__(self, encoder):
        """Initializing the class. """
        self._forward = encoder                             # forward passing or encoder is given by the user
        self._backward = self._decoder()                    # shift to decrypt message, decoder


    def _decoder(self):
        """Given an encoder, this gives the shift to decoder. """
        decoder = [None] * 26                                   # List of 26 entries with no elements
        encoder = list(self._forward)                           # Giving a name for simplicity
        for i in range(len(encoder)):
            decoder[ord(encoder[i]) - ord('A')] = chr(ord('A') + i) # encoder's 0th position is to be mapped to a and so on
        return ''.join(decoder)

    def encrypt(self, message):
        """Given a message, it encrypts the message"""
        return self._transform(message, self._forward)

    def decrypt(self, message):
        """Given an encrypted message, it decrypts the message."""
        return self._transform(message, self._backward)

    def _transform(self, message, code):
        """Given a message and a code (either encrypting or decrypting), makes the necessary transformation"""
        msg = list(message)
        for i in range(len(msg)):
            if msg[i].isupper():
                msg[i] = code[ord(msg[i])- ord('A')]
            elif msg[i].islower():
                msg[i] = code[ord(msg[i]) - ord('a')].lower()   # Because the code has all upper case, make it lower
        return ''.join(msg)


############### Caeser Cipher #############
class CaeserCipher(SubstitutionCipher):
    """Defines a class for CaeserCipher, which takes a shift to generate code for encoding.
    This is a subclass of SubstitutionCipher.
    """
    def __init__(self, shift):
        """Initializes CaeserCipher with a shift."""
        self._shift = shift
        encoder = [None] * 26       # array for encryption

        for k in range(26):
            encoder[k] = chr((k + shift) % 26 + ord('A'))  # for capital letters
        self._forward = ''.join(encoder)                    # storing as string to keep fixed
        self._backward = self._decoder()


############## Random Cipher ###############
class RandomCipher(SubstitutionCipher):
    """Defines a class for RandonCipher, which builts an encoder by randomly permuting alphabets.
    This is a subclass of SubstitutionCipher.
    It requires no input for code generation.
    """
    def __init__(self):
        """Initializes RandomCipher."""
        self._forward = self._codeGen()
        self._backward = self._decoder()

    def _codeGen(self):
        """Randomly permutes aplphabets to generate a code for encryption. """
        alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        code = random.sample(alpha, k =len(alpha))              # using random.sample instead of random.shuffle (why?)
        return ''.join(code)


############### Transposition Cipher ###############
class TranspositionCipher:
    """
    Defines a class for Transposition Cipher, which takes a key to encrypt and decrypt messages.
    Also called as columnar transposition cipher.
    """
    def __init__(self, key):
        """Initializes TranspositionCipher with a key. The key is a permutation."""
        self._key = key
        self._keyLen = len(key)

    def encrypt(self, message):
        """Encrypts the message using the key."""
        cipherText = [''] * self._keyLen
        for col in range(self._keyLen):
            pointer = col
            while pointer < len(message):
                cipherText[col] += message[pointer]
                pointer += self._keyLen
        # reorder the cipher text according to the key
        print(cipherText)
        cipherDraft = [cipherText[self._key.index(i)] for i in sorted(self._key)]
        print(cipherDraft)
        return ''.join(cipherDraft)

    def decrypt(self, message):
        """Decrypts the message using the key."""
        # calculate the number of rows in the draft
        numRows = self._keyLen
        # calculate the number of columns in the draft
        numCols = (len(message) // numRows)
        # split the message into rows
        rowList = [''] * numRows
        for row in range(numRows):
            rowList[row] = message[row*numCols:(row+1)*numCols]
        
        # reorder the columns according to the key
        print(rowList)
        plainDraft = [''] * numRows
        for i,item in enumerate(sorted(self._key)):
            plainDraft[self._key.index(item)] = rowList[i]
        print(plainDraft)
        # get back the message from the draft
        plainText = ''
        for col in range(numCols):
            for row in range(numRows):
                if col < len(plainDraft[row]):
                    plainText += plainDraft[row][col]
        return plainText

                

        

################ Testing ##################
if __name__ == "__main__":
    cipher = TranspositionCipher('CIPHER')
    message = "THIS IS WIKIPEDIA AND THIS IS A TEST"
    

