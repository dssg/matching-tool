# coding: utf-8

import pandas as pd

import matcher.ioutils as ioutils

from matcher.logger import logger

def preprocess(df:pd.DataFrame, upload_id:str, jurisdiction:str) -> pd.DataFrame:
    # full_name
    # full name is only given if name parts are not. maybe we should do some preprocessing on full names to create
    # name parts and use only the name parts, especially since it is possible for the jail and HMIS systems to
    # differ on what they use

    # prefix
    # we should preprocess prefixes to remove punctuation and possibly spaces
    if 'prefix' in df.columns:
        logger.debug('Removing punctuation from prefixes')
        df['prefix'] = df['prefix'].str.replace('[^\w\s]','')

    # first_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_first_name, first_word_first_name
    # - try using second+ word of first name as middle name if no middle name 

    # middle_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_middle_name, first_word_middle_name, second_word_middle_name

    # last_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_last_name, first_word_last_name, second_word_last_name

    # suffix
    if 'suffix' in df.columns:
        logger.debug('Removing punctuation from suffixes')
        df['suffix'] = df['suffix'].str.replace('[^\w\s]','')

    # dob
    # MUST BE CAST TO DATETIME DURING PREPROCESSING
    if 'dob' in df.columns:
        logger.debug('Converting date of birth to datetime')
        df['dob'] = pd.to_datetime(df['dob'])

    # ssn
    # THIS SHOULD BE CONVERTED TO STRING. The SSN consists of 3 words, and numerical distances are only
    # VAGUELY meaningful (e.g., the first 3 digits increase roughly east to west but not in a rigorous way,
    # and the second 2 digits are given out in a fixed but non-monotonic order)
    # the first three digits are the "area code" of where the person was registered.
    # most people living in an area will have one of a few local area codes; therefore, the distinctiveness
    # of the area code may be useful for matching. we may want to preprocess ssn to extract the area code
    # to make this comparison.
    if 'ssn' in df.columns:
        logger.debug('Converting social security number to str')
        df['ssn'] = df['ssn'].astype(str)

    # dmv_number
    # THIS SHOULD BE CAST TO STRING. In some jurisdictions, they are strings and in others ints. To ensure
    # that we can generalize here, we need to convert to string for all of them.
    if 'dmv_number' in df.columns:
        logger.debug('Converting dmv number to str')
        df['dmv_number'] = df['dmv_number'].astype(str)

    # race
    # make race into a list
    # eventually, we will want to combine secondary race and race into a single field
    if 'race' in df.columns:
        logger.debug('Converting race to list')
        df['race'] = df['race'].fillna('').str.split(',')
        logger.debug(f"Races observed in preprocessed df: {df['race']}")

    # ethnicity
    # ethnicity encodes only Hispanic/Not Hispanic. for some databases, Hispanic is actually included
    # in the race categories instead of in a separate field. we may want to do some pre-processing to
    # to add H to the race list where the ethnicity field contains 'Hispanic'

    logger.info('Preprocessing done!')
    logger.debug(f"The preprocessed dataframe has the following columns: {df.columns}")
    logger.debug(f"The preprocessed dimensions of the dataframe is: {df.shape}")
    ioutils.write_dataframe_to_s3(features.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/preprocessed_data/{upload_id}')
    return df

