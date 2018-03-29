# coding: utf-8

import pandas as pd
import numpy as np


from sklearn.cluster import DBSCAN

from . import api

def cluster(
    distances:pd.DataFrame,
    eps:float=0.5,
    min_samples:int=1,
    algorithm:str='auto',
    leaf_size:int=30,
    n_jobs:int=1
) -> pd.DataFrame:
    """ Cluster the scored entities into individuals. Return the cluster ids
    indexed with the source row_id.
    """

    api.app.logger.info('Beginning clustering.')

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

    clusterer.fit(X=distances)
    api.app.logger.info('Clustering done! Assigning matched ids.')

    return pd.Series(
        index=distances.index,
        data=clusterer.labels_
    )


def generate_matched_ids(
    distances:pd.DataFrame,
    DF:pd.DataFrame,
    clustering_params:dict
) -> pd.DataFrame:
    
    api.app.logger.info('Beginning clustering & id generation.')

    ids = cluster(
        distances, **clustering_params
    )
    max_cluster_id = ids.max()
    replacement_ids = pd.Series(range(max_cluster_id + 1, max_cluster_id + len(ids[ids == -1]) + 1), index=ids[ids==-1].index)
    ids[ids == -1] = replacement_ids
    api.app.logger.debug(f'IDs: {ids}')
    api.app.logger.debug(f'Replaced noisy singleton ids with \n{replacement_ids}')
    df = DF.copy()
    
    df['matched_id'] = ids

    api.app.logger.info('Matched ids generated')

    return (df)                 

