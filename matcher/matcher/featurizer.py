
import recordlinkage as rl
import pandas as pd

def truncate_string(s:pd.Series, n:int) -> pd.Series:
    if n > 0:
        s = s.astype(str).apply(lambda x: x[:n])
    elif n < 0:
        s = s.astype(str).apply(lambda x: x[n:])
    else:
        raise ValueError('I cannot compare strings of 0 length!!!')

    return s


def compare_exact_n_chars(s1:pd.Series, s2:pd.Series, n:int) -> pd.Series:
    s1 = truncate_string(s1, n)
    s2 = truncate_string(s2, n)

    return (s1 == s2).astype(float)


def lists_share_any_values(l1:pd.Series, l2:pd.Series) -> pd.Series:
    # make a pd.DataFrame from the columns, converting the strings to lists
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    
    # for each row, check whether any of the items in the first list is in the second
    return df.apply(lambda row: any(i in row.l2 for i in row.l1), axis=1).astype(float)


def lists_share_all_values(l1:pd.Series, l2:pd.Series) -> pd.Series:
    # make a pd.DataFrame from the columns, converting the strings to lists
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    
    # for each row, check whether all elements of l1 shared with l2 and vice versa
    l1_all = df.apply(lambda row: all(i in row.l2 for i in row.l1), axis=1)
    l2_all = df.apply(lambda row: all(i in row.l1 for i in row.l2), axis=1)

    return (l1_all & l2_all).astype(float)


def generate_features(pairs:pd.MultiIndex, df:pd.DataFrame) -> pd.DataFrame:
    compare_cl = rl.Compare()

    # full_name
    # full name is only given if name parts are not. maybe we should do some preprocessing on full names to create
    # name parts and use only the name parts, especially since it is possible for the jail and HMIS systems to
    # differ on what they use
    if 'full_name' in df.columns:
        compare_cl.exact('full_name', 'full_name', label='full_name_exacti_distance')
        compare_cl.string('full_name', 'full_name', method='jarowinkler', threshold=0.85, label='full_name_jarowinkler_distance')
        # compare_cl.string('full_name', 'full_name', method='qgram', threshold=0.85, label='full_name_qgram_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'full_name', 'full_name', 5, label='full_name_first_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'full_name', 'full_name', -5, label='full_name_last_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'full_name', 'full_name', 3, label='full_name_first_3_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'full_name', 'full_name', -3, label='full_name_last_3_distance')

    # prefix
    # we should preprocess prefixes to remove punctuation and possibly spaces
    if 'prefix' in df.columns:
        compare_cl.exact('prefix', 'prefix', label='prefix_exact_distance')
        compare_cl.string('prefix', 'prefix', method='jaro', threshold=0.85, label='prefix_jaro_distance')

    # first_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_first_name, first_word_first_name
    # - try using second+ word of first name as middle name if no middle name 
    if 'first_name' in df.columns:
        compare_cl.exact('first_name', 'first_name', label='first_name_exact_distance')
        compare_cl.string('first_name', 'first_name', method='jarowinkler', threshold=0.85, label='first_name_jarowinkler_distance')
        # compare_cl.string('first_name', 'first_name', method='qgram', threshold=0.85, label='first_name_qgram_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'first_name', 'first_name', 5, label='first_name_first_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'first_name', 'first_name', -5, label='first_name_last_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'first_name', 'first_name', 3, label='first_name_first_3_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'first_name', 'first_name', -3, label='first_name_last_3_distance')

    # middle_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_middle_name, first_word_middle_name, second_word_middle_name
    if 'middle_name' in df.columns:
        compare_cl.exact('middle_name', 'middle_name', label='middle_name_exact_distance')
        compare_cl.string('middle_name', 'middle_name', method='jarowinkler', threshold=0.85, label='middle_name_jarowinkler_distance')
        # compare_cl.string('middle_name', 'middle_name', method='qgram', threshold=0.85, label='middle_name_qgram_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'middle_name', 'middle_name', 5, label='middle_name_first_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'middle_name', 'middle_name', -5, label='middle_name_last_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'middle_name', 'middle_name', 3, label='middle_name_first_3_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'middle_name', 'middle_name', -3, label='middle_name_last_3_distance')

    # last_name
    # potential preprocessing steps:
    # - remove punctuation
    # - create: full_last_name, first_word_last_name, second_word_last_name
    if 'last_name' in df.columns:
        compare_cl.exact('last_name', 'last_name', label='last_name_exact_distance')
        compare_cl.string('last_name', 'last_name', method='jarowinkler', threshold=0.85, label='last_name_jarowinkler_distance')
        # compare_cl.string('last_name', 'last_name', method='qgram', threshold=0.85, label='last_name_qgram_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'last_name', 'last_name', 5, label='middle_name_first_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'last_name', 'last_name', -5, label='middle_name_last_5_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'last_name', 'last_name', 3, label='middle_name_first_3_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'last_name', 'last_name', -3, label='middle_name_last_3_distance')

    # suffix
    if 'suffix' in df.columns:
        # we should preprocess suffixes to remove punctuation and possibly spaces
        compare_cl.exact('suffix', 'suffix', label='suffix_exact_distance')
        compare_cl.string('suffix', 'suffix', method='jaro', threshold=0.85, label='suffix_jaro_distance')

    # dob
    # MUST BE CAST TO DATETIME DURING PREPROCESSING
    if 'dob' in df.columns:
        compare_cl.exact('dob', 'dob', label='dob_exact_distance')
        compare_cl.date('dob', 'dob', label='dob_date_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'dob', 'dob', 4, label='dob_year_exact_distance')

    # ssn
    # THIS SHOULD BE CONVERTED TO STRING. The SSN consists of 3 words, and numerical distances are only
    # VAGUELY meaningful (e.g., the first 3 digits increase roughly east to west but not in a rigorous way,
    # and the second 2 digits are given out in a fixed but non-monotonic order)
    # the first three digits are the "area code" of where the person was registered.
    # most people living in an area will have one of a few local area codes; therefore, the distinctiveness
    # of the area code may be useful for matching. we may want to preprocess ssn to extract the area code
    # to make this comparison.
    if 'ssn' in df.columns:
        compare_cl.exact('ssn', 'ssn', label='ssn_exact_distance')
        compare_cl.string('ssn', 'ssn', method='jaro', threshold=0.85, label='ssn_jaro_distance')
        # compare_cl.string('ssn', 'ssn', method='qgram', threshold=0.85, label='ssn_qgram_distance')
        # the last four digits are the "serial number" of the person (i.e., the most unique part of the number) 
        # and are often the only known/shared component, so we will run a special exact comparison on them
        compare_cl.compare_vectorized(compare_exact_n_chars, 'ssn', 'ssn', -4, label='ssn_last_4_distance')

    # ssn_hash
    # we can only compare these exact
    if 'ssn_hash' in df.columns:
        compare_cl.exact('ssn_hash', 'ssn_hash', label='ssn_hash_exact_distance')

    # dmv_number
    # THIS SHOULD BE CAST TO STRING. In some jurisdictions, they are strings and in others ints. To ensure
    # that we can generalize here, we need to convert to string for all of them.
    if 'dmv_number' in df.columns:
        compare_cl.exact('dmv_number', 'dmv_number', label='dmv_number_exact_distance')
        compare_cl.string('dmv_number', 'dmv_number', method='jaro', threshold=0.85, label='dmv_number_jaro_distance')
        # compare_cl.string('dmv_number', 'dmv_number', method='qgram', threshold=0.85, label='dmv_number_qgram_distance')

    # dmv_state
    if 'dmv_state' in df.columns:
        compare_cl.exact('dmv_state', 'dmv_state', label='dmv_state_exact_distance')

    # race
    # if race is not useful, we may want to consider some preprocessing around that various codes for
    # missingness (refused, doesn't know, NULL, etc.)
    # race codes are single characters but can be combined in a list. we will break it down and see if
    # (a) all races match, disregarding order;
    # (b) any race matches
    if 'race' in df.columns:
        compare_cl.compare_vectorized(lists_share_all_values, 'race', 'race', label='race_all_distance')
        compare_cl.compare_vectorized(lists_share_any_values, 'race', 'race', label='race_any_distance')

    # ethnicity
    # ethnicity encodes only Hispanic/Not Hispanic. for some databases, Hispanic is actually included
    # in the race categories instead of in a separate field. we may want to do some pre-processing to
    # to add H to the race list where the ethnicity field contains 'Hispanic'
    if 'ethnicity' in df.columns:
        compare_cl.exact('ethnicity', 'ethnicity', label='ethnicity_exact_distance')

    # sex
    # we accept 'TM' and 'TF', which are used primarily by HMIS systems to identify trans men and women.
    # in most criminal justice databases, there is no separate designation for trans men and women or
    # non-binary genders, and sex/gender may be entered based on self-identification, official state id,
    # or biological sex as determined by jail staff. so we will compare both the full value and just the
    # last letter
    if 'sex' in df.columns:
        compare_cl.exact('sex', 'sex', label='sex_exact_distance')
        compare_cl.compare_vectorized(compare_exact_n_chars, 'sex', 'sex', -1, label='sex_exact_last_letter_distance')

    # we will ignore address info for now, as it is especially unlikely to be useful for this problem
    # (e.g., maybe we only want to compare addresses from similar timeframes)

    # finally, generate all the comparisons and return the features
    return compare_cl.compute(pairs, df)
