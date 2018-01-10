# coding: utf-8

from itertools import tee, islice

from typing import Iterable, List

def ngram_generator(iterable:Iterable, n:int) -> List:
    """
    Given an iterable, generates the n-gram
    """
    return zip(*((islice(seq, i, None) for i,seq in enumerate(tee(iterable,n)))))
