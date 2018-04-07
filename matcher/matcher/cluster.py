# coding: utf-8

import pandas as pd
import numpy as np


from sklearn.cluster import DBSCAN

import matcher.ioutils as ioutils

from matcher.logger import logger

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

    logger.info('Beginning clustering.')

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
    logger.info('Clustering done! Assigning matched ids.')

    return pd.Series(
        index=distances.index,
        data=clusterer.labels_
    )


def square_distance_matrix(df:pd.DataFrame) -> pd.DataFrame:
    # create a copy, swap the indicies
    tmp_df = df.copy()
    tmp_df.reset_index(inplace=True)
    tmp_df.rename(
        mapper={'matcher_index_left': 'matcher_index_right', 'matcher_index_right': 'matcher_index_left'},
        axis='columns',
        inplace=True
    )
    tmp_df.set_index(['matcher_index_left', 'matcher_index_right'], inplace=True)

    # concat original & df with swapped indices; square the matrix, filling in 0 distance for self-pairs
    return pd.concat([df, tmp_df]).matches.unstack(level=-1, fill_value=0)


def generate_matched_ids(
    distances:pd.DataFrame,
    DF:pd.DataFrame,
    clustering_params:dict,
    jurisdiction:str,
    upload_id=str,
    block_name='',
) -> pd.DataFrame:
    
    logger.info('Beginning clustering & id generation.')
    distances = square_distance_matrix(distances)
    ioutils.write_dataframe_to_s3(distances.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/square_distances/{upload_id}/{block_name}')

    ids = cluster(
        distances, **clustering_params
    )
    ioutils.write_dataframe_to_s3(ids.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/raw_cluster_ids/{upload_id}/{block_name}')
    max_cluster_id = ids.max()
    replacement_ids = pd.Series(range(max_cluster_id + 1, max_cluster_id + len(ids[ids == -1]) + 1), index=ids[ids==-1].index)
    ids[ids == -1] = replacement_ids
    logger.debug(f'IDs: {ids}')
    logger.debug(f'Replaced noisy singleton ids with \n{replacement_ids}')
    
    logger.debug(f'Adding the block name ({block_name}) to the matched_ids.')
    ids = str(block_name) + ids.astype(str)
    logger.debug(f'New IDs: \n{ids}')
    
    df = DF.copy()
    
    df['matched_id'] = ids
    logger.info('Matched ids generated')

    return (df)                 


def generate_singleton_id(df:pd.DataFrame, block_name:str) -> pd.DataFrame:
    df['matched_id'] = block_name + '0'
    logger.info(f'Singleton has id {df.matched_id.values[0]}')
    return df

