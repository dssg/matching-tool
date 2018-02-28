# coding: utf-8

from itertools import tee, islice

from typing import Iterable, List, Dict

import pandas as pd

def ngram_generator(iterable:Iterable, n:int) -> List:
    """
    Given an iterable, generates the n-gram
    """
    return zip(*((islice(seq, i, None) for i,seq in enumerate(tee(iterable,n)))))

def ngrammer(df:pd.DataFrame, to_ngrams:List, n=2) -> pd.DataFrame:
    for col in to_ngrams:
        df[f"{col}_{n}grams"] = df[col].apply(ngram_generator, n=n).apply(list)
    return df

def unite(df:pd.DataFrame, to_unite:Dict) -> pd.DataFrame:
    for key, cols in to_unite.items():
        df[key] = df[cols].apply(lambda x: ' '.join(x), axis = 1)
    return df

def split(df:pd.DataFrame, to_split:List, separator=" ") -> pd.DataFrame:
    for col in to_split:
        df2=df[col].str.split(separator, expand=True)
        df2.rename(mapper=lambda x: f"{col}_{x}", axis=1, inplace=True)
        df = pd.concat([df, df2], axis=1)
    return df
        
def transformer(df:pd.DataFrame, to_ngrams:List, to_unite:Dict, to_split:List) -> pd.DataFrame:
    df = ngrammer(ngrammer(
                 split(
                     unite(df, to_unite),
                     to_split, separator=" "),
        to_ngrams, n=2),
                  to_ngrams, n=3)
    
    return df

    
