# coding: utf-8

import os

import logging
import logging.config


log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploader_logging.ini')

logging.config.fileConfig(log_file_path)
logger = logging.getLogger()
