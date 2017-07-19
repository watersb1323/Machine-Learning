__author__ = "Brian Waters"

import os
from collections import Counter


def make_Dictionary(train_dir):
    """
    Read through all test files and create a dictionary of words
    and the number of times they appear in spam emails.
    :param train_dir: Directory where training information can be found
    :return: Dictionary of words and counts of each word
    """
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:  # Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words

    dictionary = Counter(all_words)
    # Paste code for non-word removal here(code snippet is given below)
    return dictionary

if __name__ == "__main__":
    train_dir = ""

    make_Dictionary(train_dir)