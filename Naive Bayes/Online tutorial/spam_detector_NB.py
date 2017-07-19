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

    dictionary = Counter(x for x in all_words if x.isalpha() and len(x) != 1)
    dictionary = dictionary.most_common(3000)
    return dictionary

def print_dict(dict_to_print):
    '''Print all elements of a dictionary'''
    for k,v in dict_to_print.items():
        print("%s - %s" % (str(k), str(v)))

if __name__ == "__main__":
    train_dir = r"C:\Users\brwaters\Documents\GitHub\Machine-Learning\Naive Bayes\Online tutorial\train-mails"

    my_dict = make_Dictionary(train_dir)

    print(my_dict)