# coding: utf-8

from itertools import tee, islice


def ngram_generator(iterable, n):
    """
    Given an iterable, generates the n-gram
    """
    return zip(*((islice(seq, i, None) for i,seq in enumerate(tee(iterable,n)))))
