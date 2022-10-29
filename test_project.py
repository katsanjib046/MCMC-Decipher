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


def test_count_and_prob_matrix():
    """
    Test count matrix function.
    """
    count_matrix = project.count_matrix(file='wp.txt')
    prob_matrix = project.probability_matrix(count_matrix)
    assert count_matrix.shape == (27, 27)
    assert prob_matrix.shape == (27, 27)
    # probability for each row must sum to 1
    for i in range(27):
        assert 0.99999 < prob_matrix[0,:].sum() <= 1

def test_count_matrix_trigram():
    """
    Test for count_matrix_trigram function.
    """
    count_matrix = project.count_matrix_trigram(file='wp.txt')
    assert count_matrix.shape == (27, 27, 27)
    

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
