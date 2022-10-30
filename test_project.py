# File: test_project.py 

"""
Module: Test for project.py
Contains functions:
    - test_main
"""
# imports 
import pytest
import project
import cipher
import string
import numpy as np
    
def test_chunker():
    """
    Test for chunker function.
    """
    assert project.chunker('hello', 2) == ['he', 'el', 'll', 'lo']
    assert project.chunker('hello', 3) == ['hel', 'ell', 'llo']
    assert project.chunker('hello', 4) == ['hell', 'ello']
    assert project.chunker('world', 5) == ['world']
    assert project.chunker('hello', 6) == []
    assert project.chunker('', 2) == []


def test_count_matrix():
    """
    Test for count matrix
    """
    assert project.count_matrix(text='hello', n_gram=1) == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    assert project.count_matrix(text='hello', n_gram=2) == {'he': 1, 'el': 1, 'll': 1, 'lo': 1}
    assert project.count_matrix(text='this is a test', n_gram=1) == {'t':3, 'h':1, 'i':2, 's':3, 'a':1, 'e':1, ' ':3}


def test_random_key():
    """
    Test for random_key function.
    """
    assert len(project.random_key()) == 26
    assert ''.join(sorted(project.random_key())) == string.ascii_uppercase


def test_encrypt():
    """
    Test for encrypt function.
    """
    assert project.encrypt('Hi, How are you?', key=1) == 'Ij, Ipx bsf zpv?'
    assert project.encrypt('You okay?', key=2) == 'Aqw qmca?'
    assert project.encrypt('hello', key='BCDEFGHIJKLMNOPQRSTUVWXYZA') == 'ifmmp'


def test_decrypt():
    """
    Test for decrypt function.
    """
    assert project.decrypt('ifmmp', key=1) == 'hello'
    assert project.decrypt('jgnnq?', key=2) == 'hello?'
    assert project.decrypt('ifmmp', key='BCDEFGHIJKLMNOPQRSTUVWXYZA') == 'hello'
    assert project.decrypt(project.encrypt('hello world', key=1), key=1) == 'hello world'

def test_accuracy():
    """
    Test for accuracy function.
    """
    assert project.accuracy('hello', 'hello') == 1
    assert project.accuracy('hello', 'hillo') == 0.8
    assert project.accuracy('hello', 'hillo world') == 0.8
    assert project.accuracy('the world is beautiful', 'the world is beautiful') == 1
