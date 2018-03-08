# coding: utf-8

import contraster
import logging
logger = logging.getLogger('matcher')

import pandas as pd
import numpy as np


from sklearn.cluster import DBSCAN


def cluster(
    df:pd.DataFrame,
    eps:float=0.5,
    min_samples:int=1,
    algorithm:str='auto',
    leaf_size:int=30,
    n_jobs:int=1
) -> pd.DataFrame:
    """ Cluster the scored entities into individuals. Return the cluster ids
    indexed with the source row_id.
    """

    logger.info('Beginning clustering.')
    df = 1 - df
    clusterer = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric='precomputed',
        metric_params=None,
        algorithm=algorithm,
        leaf_size=leaf_size,
        p=None,
        n_jobs=n_jobs
    )

    clusterer.fit(X=df)
    logger.info('Clustering done! Assigning matched ids.')

    return pd.Series(
        index=df.index,
        data=clusterer.labels_
    )


def square_distances(upper_right, df1, df2):
    """ For now, this function uses recursion to fill in the self matches by
    relying on exact matches on source_id. For non-self-matches, the source_id
    will be the matched_id from the previous run, so we will be relying on our
    previous matches. If two elements share a matched_id, we score them as 1;
    else, we score them as 0. Once we start caching the distances matrices and
    storing the match metadata in the output, it may save time to check for the
    cache and use it if it is available, rather than recursing here (and forcing
    1 or 0 distances).
    """
    logger.info('Expanding distances matrix with self-matches.')
    upper_left = match(
        df1,
        df1.copy(),
        contraster.exact,
        ['source_id']
    ).pivot(index='row_id_left', columns='row_id_right', values='matches')
    lower_right = match(
        df2,
        df2.copy(),
        contraster.exact,
        ['source_id']
    ).pivot(index='row_id_left', columns='row_id_right', values='matches')
    left = pd.concat([upper_left, upper_right.T])
    right = pd.concat([upper_right, lower_right])

    return pd.concat([left, right], axis=1)


def generate_matched_ids(
    distances:pd.DataFrame,
    df1:pd.DataFrame,
    df2:pd.DataFrame,
    clustering_params:dict,
    self_match
) -> tuple:
    logger.info('Beginning clustering & id generation.')
    n = len(df1)
    m = len(df2)

    # for clustering, the distances must be a square matrix with all possible
    # pairs. if we are doing a self-match, this is what we have, but if we are
    # matching different data sources, we only have the upper right portion of
    # the matrix (the distances between elements in the different sets), and we
    # need to complete the square with the self-matches for each matrix, plus
    # the transpose of the distances we have (for the lower left portion)
    if not self_match:
        distances = square_distances(distances, df1, df2)

    ids = cluster(
        distances, **clustering_params
    )

    df1['matched_id'] = ids.head(n)
    df2['matched_id'] = ids.tail(m)

    logger.info('Matched ids generated')

    return (df1, df2)

