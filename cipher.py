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


################ Testing ##################
if __name__ == "__main__":
    cipher = RandomCipher()
    en = cipher.encrypt("Hello World!")
    dec = cipher.decrypt(en)
    print(en)
    print(dec)
