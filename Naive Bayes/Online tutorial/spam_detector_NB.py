__author__ = "Brian Waters"

import os
from collections import Counter
import numpy as np


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

    dictionary = Counter(x for x in all_words if x.isalpha() and len(x) != 1)
    dictionary = dictionary.most_common(3000)
    return dictionary

def print_dict(dict_to_print):
    '''Print all elements of a dictionary'''
    for k,v in dict_to_print.items():
        print("%s - %s" % (str(k), str(v)))

def extract_features(mail_dir):
    files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0
    for fil in files:
        with open(fil) as fi:
            for i,line in enumerate(fi):
                if i == 2:
                    words = line.split()
                    for word in words:
                        wordID = 0
                        for j, d in enumerate(dictionary):
                            if d[j] == word:
                                wordID = j
                                features_matrix[docID, wordID] = words.count(word)
            docID = docID + 1
    return features_matrix



if __name__ == "__main__":
    train_dir = r"C:\Users\brwaters\Documents\GitHub\Machine-Learning\Naive Bayes\Online tutorial\train-mails"

    my_dict = make_Dictionary(train_dir)

    train_matrix = extract_features(train_dir)

    print(my_dict)