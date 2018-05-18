# coding: utf-8

import pandas as pd

from sklearn.cluster import DBSCAN

import matcher.ioutils as ioutils

from matcher.logger import logger


class Clusterizer():

    def __init__(self, algorithm=sklearn.cluster.DBSCAN, **params):

        self.params = params

        self.clusterer = algorithm(**params)


    def run(self, distances:pd.DataFrame) -> pd.DataFrame:
        """ Cluster the scored entities into individuals. Return the cluster ids
        indexed with the source row_id.
        """
        logger.info('Beginning clustering & id generation.')        
        squared_distances = self._square_distance_matrix(distances)
        
        logger.info('Beginning clustering.')
        
        self.clusterer.fit(X=squared_distances)

        logger.info('Clustering done! Assigning matched ids.')
        
        ids = pd.Series(
            index=distances.index,
            data=clusterer.labels_
        )
        
        max_cluster_id = ids.max()
        replacement_ids = pd.Series(range(max_cluster_id + 1, max_cluster_id + len(ids[ids == -1]) + 1), index=ids[ids==-1].index)
        ids[ids == -1] = replacement_ids
        logger.debug(f'IDs: {ids}')
        logger.debug(f'Replaced noisy singleton ids with \n{replacement_ids}')
        
        logger.info('Matched ids generated')
        
        return ids.astype(str)

    def _square_distance_matrix(self, df:pd.DataFrame) -> pd.DataFrame:
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

