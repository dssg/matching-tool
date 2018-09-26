# coding: utf-8

import copy
import datetime
import hashlib
import importlib
import json
from typing import List

import pandas as pd
import numpy as np
import sklearn

import matcher.blocker as blocker
import matcher.contraster as contraster
import matcher.scorer as scorer
import matcher.cluster as cluster
import matcher.matcher as matcher
import matcher.utils as utils

from matcher.logger import logger


class Pipeline:
    def __init__(
        self,
        config:dict
    ):
        self.config = config
        self.initialization_time = datetime.datetime.now()
        self.run_start_time = None
        self.matchers = {}
        self.matches = None
        self.run_end_time = None
        self.initialize_components()
        
    def initialize_components(self):
        if 'blocking_rules' in self.config.keys():
            blocking_rules = self.config['blocking_rules']
        else:
            blocking_rules = None
        self.blocker = blocker.Blocker(blocking_rules)

        self.contraster = contraster.Contraster(self.config['contrasts'])
        
        self.scorer = scorer.Scorer(operation=self.config['scorer']['operation'])
        
        module_name, class_name = self.config['clusterer']['algorithm'].rsplit(".", 1)
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        self.clusterer = cluster.Clusterer(
            clustering_algorithm=cls,
            **self.config['clusterer']['args']
        )

        self.base_matcher = matcher.Matcher(
            self.contraster,
            self.scorer,
            self.clusterer
        )

    def run(self, df:pd.DataFrame):
        self.run_start_time = datetime.datetime.now()
        logger.info('Matcher run started! Vroom vroom!')
        
        logger.info('Starting blocking!')
        blocks = self.blocker.run(df)

        logger.info(f'Blocking done! Starting matching {len(blocks)} blocks.')
        matchers = {}
        matches = []
        for key, block in blocks:
            logger.debug(f"Matching group {key} of size {len(block)}")
            matcher = copy.deepcopy(self.base_matcher)
            matches.append(''.join(key) + matcher.run(df=block).astype(str))
            matchers[''.join(key)] = matcher

        self.matchers.update(matchers)
        matches = pd.DataFrame({'matched_id': pd.concat(matches)})
        self.matches = matches

        self.run_end_time = datetime.datetime.now()

