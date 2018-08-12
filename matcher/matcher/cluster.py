# coding: utf-8

import datetime
import numpy as np
import pandas as pd
import sklearn

import matcher.ioutils as ioutils

from matcher.logger import logger


class Clusterer():

    def __init__(self, clustering_algorithm=sklearn.cluster.DBSCAN, **kwargs):
        self.kwargs = kwargs
        self.clusterer = clustering_algorithm(**kwargs)
        self.metadata = {'clusterer_initialization_time': datetime.datetime.now()}

    def run(self, distances:pd.DataFrame) -> pd.DataFrame:
        """ Cluster the scored entities into individuals. Return the cluster ids
        indexed with the source row_id.
        """
        self.metadata['clusterer_run_time'] = datetime.datetime.now()
        logger.info('Beginning clustering & id generation.')

        squared_distances = self._square_distance_matrix(distances)
        self.metadata['square_distance_matrix_dimensions'] = squared_distances.shape

        logger.debug('Squared the distances. Beginning clustering.')
        self.clusterer.fit(X=squared_distances)
        self.metadata['clusterer_fit_time'] = datetime.datetime.now

        logger.debug('Clustering done! Assigning matched ids.')
        ids = self._generate_ids(squared_distances.index.values, self.clusterer.labels_).astype(str)
        self.metadata['clusterer_finished_time'] = datetime.datetime.now()

        return ids

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
        
        # concat original & df with swapped indices;
        # square (unstack) the matrix, filling in 0 distance for self-pairs
        return pd.concat([df, tmp_df]).score.unstack(level=-1, fill_value=0)

    def _generate_ids(self, index:pd.Index, labels:np.array) -> pd.Series:
        logger.debug(f'index {len(index)}')
        logger.debug(f'labels {len(labels)}')
        ids = pd.Series(index=index, data=labels, name='matched_id')
        logger.debug(f'ids {ids}')
        max_cluster_id = ids.max()
        self.metadata['num_clusters_found'] = max_cluster_id
        self.metadata['num_noisy_clusters'] = len(ids[ids == -1])

        replacement_ids = pd.Series(
            data=range(max_cluster_id + 1, max_cluster_id + len(ids[ids == -1]) + 1),
            index=ids[ids == -1].index
        )
        ids[ids == -1] = replacement_ids
        logger.info('Matched ids generated')
        
        return ids

