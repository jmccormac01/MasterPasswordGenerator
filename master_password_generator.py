"""
Generator Master Passwords for use with password managers

This code takes inspiration from:

    Computerphile Password Cracking:
    https://www.youtube.com/watch?v=7U-RbOKanYs
    Computerphile Password Choice:
    https://www.youtube.com/watch?v=3NjQ9b3pgIg
    XKCD Password Strength:
    https://xkcd.com/936/

and uses Peter Norvig's compilation of the 1/3 million
most frequent English words:
    http://norvig.com/ngrams/count_1w.txt
    http://norvig.com/ngrams/
"""
import sys
import random
import argparse as ap
from datetime import datetime
import numpy as np

# pylint: disable = too-few-public-methods
# pylint: disable = invalid-name
# pylint: disable = redefined-outer-name

class Range(object):
    """
    Taken from stack overflow question 12116685 on how
    to specify a range with argparse. Added __repr__
    improvment from comment by RickardSjogren for better
    reporting from argparse
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= other <= self.end
    def __repr__(self):
        return '{0}-{1}'.format(self.start, self.end)

class Symbols(object):
    """
    Simple class holding keyboard symbols for inserting
    into generated passwords
    """
    symbols = ['!', '@', '£', '$', '%', '^', '&', '*', '(', ')',
               '-', '_', '+', '=', '{', '}', '[', ']', ':', ';',
               '|', '<', '>', '?']

def argParse():
    """
    Parse the command line argumentions

    Parameters
    ----------
    None

    Returns
    -------
    args : array-like
        Command line arguments object

    Raises
    ------
    None
    """
    description = """
                Generate master passwords for password managers.
                This code uses a random sample of the top 1/3M words
                along with user words and symbols. It generates long
                un-brute-force-able passwords that should be resilient
                to dictionary cracks also.
                """
    parser = ap.ArgumentParser(description=description)
    parser.add_argument('min_length',
                        type=int,
                        help='Minimum number of characters in password',
                        choices=[Range(10, 50)])
    parser.add_argument('--obscurity',
                        type=float,
                        help='Level of obscurity for password words. \
                              Smaller number means more obscure.',
                        choices=[Range(0.1, 1.0)],
                        default=0.9)
    parser.add_argument('--user_words',
                        type=str,
                        help='Comma separated list of user words to include')
    parser.add_argument('--word_override',
                        help='Override check for user words duplicated in the real word list',
                        action='store_true')
    parser.add_argument('--symbols',
                        type=int,
                        help='Number of random symbols to insert in final password')
    parser.add_argument('--caps',
                        type=int,
                        help='Number of characters to convert to upper case in final password')
    return parser.parse_args()

def readWordList(filename):
    """
    Read in the 1/3 million most commonly uses words

    This function takes around 0.5s on a macbook to read
    in the list of words.

    Parameters
    ----------
    filename : str
        Name of the file containing the list of commonly
        used words

    Returns
    -------
    words : array-like
        List of words read from filename
    scores : array-like
        List of corresponding scores to words

    Raises
    ------
    None
    """
    words, scores = [], []
    word_file = open(filename).readlines()
    for line in word_file:
        word, score = line.split()
        words.append(word)
        scores.append(score)
    return words, np.array(scores).astype(int)

def limitWordList(words, scores, obscurity_factor):
    """
    Trim down the list of words using the obscurity factor

    For example, if obsercurity factor = 0.1 (10%), we would
    return the bottom 10% of the list of commonly used words

    Parameters
    ----------
    words : array-like
        List of commonly used words
    scores : array-like
        The frequency of each word's use
    obscurity_factor : float
        Decimal number between 0 and 1 which denotes
        how obscure we want the words used to be

    Returns
    -------
    words : array-like
        Trimmed list of more obscure words
    scores : array-like
        Trimmed list of scores for the trimmed list of
        obscure words

    Raises
    ------
    None
    """
    word_list_length = len(scores)
    cut = int(word_list_length*obscurity_factor)
    return words[-cut:], scores[-cut:]

def insertSymbol(password, symbol, index):
    """
    Insert a symbol at a given position in a password

    Parameters
    ----------
    password : str
        Password to edit
    symbol : str
        Symbol string to insert into the password
    index : int
        Position in the password to do the insertion

    Returns
    -------
    password : str
        New password string with sumbol inserted at index

    Raises
    ------
    None
    """
    return password[:index] + symbol + password[index:]

if __name__ == "__main__":
    # start a timer to see how long this takes
    t1 = datetime.utcnow()
    # parse the commmand line args
    args = argParse()
    # read in Peter Norbig's list of 1/3 M commonly used words
    word_list = "common_words_ranked.txt"
    words, scores = readWordList(word_list)
    # limit the word list based on the most obscure fraction
    words, scores = limitWordList(words, scores, args.obscurity)
    # set up a blank password list
    password = []
    # grab any user supplied user words
    # add them to the password list
    if args.user_words:
        user_words = args.user_words.split(',')
        for user_word in user_words:
            if user_word in words and not args.word_override:
                print("User word '{}' is in the word list, quiting!".format(user_word))
                sys.exit(1)
            password.append(user_word)
    # fill the password word list with random words, on
    # top of any previous user words to generate a password length
    # to satisfy the minimum length
    while len(''.join(password)) < args.min_length:
        selection = random.choice(words)
        if selection not in password:
            password.append(random.choice(words))
    print('Password word list: {}'.format(password))
    # shuffle the list then make the list into a password string
    random.shuffle(password)
    password_string = ''.join(password)
    print('Password shuffled string: {}'.format(password_string))
    # add capitals at this point if requested
    if args.caps:
        indices = random.sample(range(0,len(password_string)), args.caps)
        print('Capitalising character indices: {}'.format(indices))
        password_string = ''.join(c.upper() if i in indices else c for i, c in enumerate(password_string))
        print(password_string)
    # finally, if requested, add in some random symbols to make
    # things even more difficult to crack
    if args.symbols:
        symbols = Symbols.symbols
        symbol_indices = random.sample(range(1, len(password_string)-1), args.symbols)
        print('Adding random symbols at indices: {}'.format(symbol_indices))
        for i in range(0, len(symbol_indices)):
            password_string = insertSymbol(password_string,
                                           random.choice(symbols),
                                           symbol_indices[i])
    print('MASTER PASSWORD: {}'.format(password_string))
    t2 = datetime.utcnow()
    print(t2-t1)

