#!/usr/bin/python
#-*- coding:utf-8 -*-
import numpy as np
import re
import itertools
from collections import Counter

def clean_str(string):
    string = re.sub(r"[^\w\u0100-\uffff]", " ", string) # _ reserved
    #string = re.sub(r"[^A-Za-z0-9\u0100-\uffff]", " ", string) # without _
    string = re.sub(r"[［,］,（,）, 】, 【,＝,＋,《,》,！]", " ", string)
    string = re.sub(r"[。,，,：,:,｜,、,～,“,”]", " ", string)
    string = re.sub(r"[」,「,－,-,–,']", " ", string)
    #string = re.sub(r"[」,「,－,-,–,♝,❣,♔,♘,,☻,']", " ", string)
    #string = re.sub(r"[❂,◡,❂,♦,✪,☼]", " ", string)
    string = re.sub(r"[0-9]", " ", string)
    string = re.sub( '\s+', ' ', string  ).strip()
    return string.strip().lower()

def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(positive_data_file, "r").readlines())
    #positive_examples = [s.strip().split('\t')[-1] for s in positive_examples]
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r").readlines())
    #negative_examples = [s.strip().split('\t')[-1] for s in negative_examples]
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words

    positive_examples = [clean_str(sent) for sent in positive_examples]
    negative_examples = [clean_str(sent) for sent in negative_examples]

    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]

    return positive_examples, negative_examples, positive_labels, negative_labels

def load_data_and_labels_for_eval(data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    examples = list(open(data_file, "r").readlines())
    #examples = [s.strip().split('\t')[-1] for s in examples]
    examples = [s.strip() for s in examples]
    # Split by words
    x_text = [clean_str(sent) for sent in examples]
    return x_text

def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
