# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 19:34:33 2017

@author: beano
"""

from collections import defaultdict
import math, re, random

def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

def print_dict(dict_to_print):
    '''Print all elements of a dictionary'''
    for k,v in dict_to_print.items():
        print("%s - %s" % (str(k), str(v)))

def tokenize(message):
    """Return the tokenized version of a string"""
    message = message.lower() # convert to lowercase
    all_words = re.findall("[a-z0-9']+", message) # extract the words
    return set(all_words) # remove duplicates
    
def count_words(training_set):
    """
    Counts words that are to be classified as spam against words that aren't
    training set consists of pairs (message, is_spam)
    """
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in tokenize(message):
            counts[word][0 if is_spam else 1] += 1
    return counts

def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    """turn the word_counts into a list of triplets
    w, p(w | spam) and p(w | ~spam)"""
    return [(w,
            (spam + k) / (total_spams + 2 * k),
            (non_spam + k) / (total_non_spams + 2 * k))
            for w, (spam, non_spam) in counts.items()]

def spam_probability(word_probs, message):
    '''
    Based on word probabities and message content, 
    return the probability of the message being spam
    '''
    message_words = tokenize(message)
    log_prob_if_spam = log_prob_if_not_spam = 0.0
    # iterate through each word in our vocabulary
    for word, prob_if_spam, prob_if_not_spam in word_probs:
        # if *word* appears in the message,
        # add the log probability of seeing it
        if word in message_words:
            log_prob_if_spam += math.log(prob_if_spam)
            log_prob_if_not_spam += math.log(prob_if_not_spam)
        # if *word* doesn't appear in the message
        # add the log probability of _not_ seeing it
        # which is log(1 - probability of seeing it)
        else:
            log_prob_if_spam += math.log(1.0 - prob_if_spam)
            log_prob_if_not_spam += math.log(1.0 - prob_if_not_spam)
    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)
    return prob_if_spam / (prob_if_spam + prob_if_not_spam)
        
class NaiveBayesClassifier:
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []
        
    def train(self, training_set):
        # count spam and non-spam messages
        num_spams = len([is_spam
                        for message, is_spam in training_set if is_spam])
        num_non_spams = len(training_set) - num_spams
        # run training data through our "pipeline"
        word_counts = count_words(training_set)
        self.word_probs = word_probabilities(word_counts,
                                             num_spams,
                                             num_non_spams,
                                             self.k)
    def classify(self, message):
        return spam_probability(self.word_probs, message)

def main():
    # Test tokenize function
    words = tokenize('This was the first test string that was used and will probably be the last... Or maybe not the last')
    print(words)
    
    training_set = [('Hey now, less of it', 1),
                    ('Hardly now, I did not think that anyway', 1),
                    ('Maybe it is', 0),
                    ('Ok, maybe not',0)]
    
    # Test count_words function
    freq_dict = count_words(training_set)
    print_dict(freq_dict)
    
    # Test word_probabilities
    triples = word_probabilities(freq_dict, 2, 2)
    for tri in triples:
        print(tri)
        
    # Test spam_probability
    spam_prbs = spam_probability(triples, 'Anyway, it hardly is less')
    print(spam_prbs)
    
if __name__ == "__main__":
    main()

