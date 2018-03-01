# coding: utf-8


import pandas as pd
import numpy as np

from typing import List

from difflib import SequenceMatcher

import Levenshtein 
from Levenshtein import ratio, distance

# String distances

def exact(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    Calculates the "exact distance" between all the selected columns
    """

    for col in keys:
        df[f"exact_distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: row[0] == row[1], axis = 1)
     
    return df

def truncate_strings(df:pd.DataFrame, keys: List, length=4) -> pd.DataFrame:

    for col in keys:
        df[f"truncate_distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: row[0][:length] == row[1][:length], axis = 1)
    
    return df

def longest_common_substring(df:pd.DataFrame, keys: List) -> pd.DataFrame:

    def _LCSS(str1, str2):
        seqMatch = SequenceMatcher(None, str1, str2)
        match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
        return match.size
    
    for col in keys:
        df[f"LCSS_distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: _LCSS(row[0], row[1]), axis = 1)

    return df

def levenshtein(df:pd.DataFrame, keys: List) -> pd.DataFrame:

    for col in keys:
        df[f"Levenshtein_distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: distance(row[0], row[1]), axis = 1)

    return df

def hamming(df:pd.DataFrame, keys: List, length=3) -> pd.DataFrame:
    """
    The Hamming distance is simply the number of different characters. This means that the length of both strings should be the same
    """
    for col in keys:
        df[f"Hamming_distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: Levenshtein.hamming(row[0][:length], row[1][:length]), axis = 1)

    return df

def qgram(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    NOTE: This expects ngrams as input.
    
    By default it will search for columns that end in "grams" (see transforms.py)
    
    The number of common q-grams is divided by the number of q-grams of the shortest input string.
    """

    if keys is None:
        keys = list(df.columns[df.columns.str.endswith('grams')])

    def _similarity(s1, s2):
        min_size = min(len(s1), len(s2))

        return len(s1.intersection(s2))/min_size
        
    for col in keys:
        df[f"qgram_metric_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: _similarity(row[0], row[1]), axis = 1)

    
    return df

def jaro(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    (From: https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
    The Jaro distance between two words is the minimum number of single-character transpositions required to change one word into the other.

    \begin{equation}
    sim_j = \big\{ 0   if m = 0, \frac{1}{3}\big\(\frac{m}{|s_1|} + \frac{m}{|s_2|} + \frac{m - t}{m} otherwise
    \end{equation}

    Where 
    $s_i$ is the length of the string $s$
    $m$ is the number of /matching characters/
    $t$ is half the number of transpositions
    """
    for col in keys:
        df[f"Jaro_similarity_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: Levenshtein.jaro(row[0], row[1]), axis = 1)

    return df


def jaro_winkler(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    (From: https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)

    Jaro–Winkler similarity uses a prefix scale $p$  which gives more favorable ratings to strings that match from the beginning for a set prefix length $l$ . 
    Given two strings $s_1$ and $s_2$, their Jaro–Winkler similarity is:
    
    \begin{equation}
    sim_{w} = sim_j + (l\cdot p (1 - \sim_j))
    \end{equation}

    where
    $\sim_j$ is the jaro similarity
    $l$ is the length of common prefix at the start of the string up to a maximum of four characters
    $p$ is a constant scaling factor for how much the score is adjusted upwards for having common prefixes. $p$ should not exceed $0.25$, otherwise the distance can become larger than 1. The satndard value is $p = 0.1$.

    The Jaro Winkler distance $d_w = 1 - sim_w$.

    NOTE: THIS FUNCTION CALCULATES THE SIMILARITY
    """
    for col in keys:
        df[f"Jaro_Winker_similarity_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: Levenshtein.jaro_winkler(row[0], row[1]), axis = 1)

    return df


