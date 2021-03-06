# Updating the Matching Service

Modifying the matching service is neccesary if you would like to change or improve matching results, experiment on matching algorithm configurations, speed up the matching process, or make other changes to how matching is done. This document provides an overview of the matching process (including how to configure the specific steps using the [matcher configuration file](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml)), and guidelines on how to make changes under common circumstances.

## Overview of the Matching Process

When a user successfully uploads a new data file to the webapp, the webapp calls [do_match()](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/tasks.py#L28) to begin a new matching job, instructing the matcher about which files to match and where to find them. From this point, the matching process proceeds like this:

1.  **Load and combine event data:** [load_data_for_matching()](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/ioutils.py#L42) loads and combines into a single data frame all of the data files passed by the webtool, retaining only the columns specified in the [keys](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml#L1) section of the matcher configuration file. This section of the configuration file is a simple list, where each line should begin with a `-` and contain the name of a column that is shared by *all* of the schemas to be matched:

        keys:
            # Which columns to select for matching
            - first_name
            - middle_name
            - last_name
            - dob
            - ssn
            - dmv_number
            - dmv_state
            - race
            - ethnicity
            - sex

2. **Exact deduplication:** Before beginning the algorithmic matching process, we [drop all rows that are exact duplicates](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/ioutils.py#L64) of another row on the matching keys (e.g., match exactly on first name, last name, date of birth, social security number, gender, and race).

3. **Preprocessing:** The deduplicated data are then sent to [preprocess.py](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/preprocess.py) to be cleaned and to enforce data types. Any data cleaning rules (e.g., cleaning out punctuation from strings, removing white space, converting data types) should be added to this file.

4. **Record linkage:** From here, the matching algorithm proceeds by breaking the data into smaller subsets (blocking), generating contrasts on each of these subsets, and then clustering records into matched groups using a split-apply-combine methodology. Each of these steps is described below.

    - **Blocking:** Comparing all records to each other is wasteful. Most record pairs are not true matches. We can identify subsets of record pairs that are more likely to contain matches and only make comparisons on them, saving both computation time and memory. The matcher uses *blocking* to do this, [subsetting](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/matcher.py#L33) the records into a dictionary smaller dataframes based on the the [blocking keys](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml#L14) in the matcher configuration file. Blocking rules should be entered as a dictionary of key-value pairs, where each key is a name of a column, and each value is the number of characters to use for blocking. For example, the rule `dob: 3` includes all people who share the first three "letters" of their date of birth (i.e., their decade of birth when dates are in YYYY-MM-DD format) in the same block. Records are only compared to each other if they share values on **all** of the keys. 
    
            blocking_rules:
                last_name: 2
                dob: 3
                first_name: 1
        
    - **Indexing:** Blocks with a single record will be [assigned a unique matched id](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/matcher.py#L44) and skip the remaining matching steps. For each block with more than one record, the matcher [identifies all *unique* record pairs](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/matcher.py#L67). If the block includes Jon, Jane, and Joe, it will compare Jon with Jane, Jon with Joe, and Jane with Joe, but it will ignore self-comparisons like Jon with Jon or duplicate comparisons like Jane with Jon.
    
    - **Contrasting:** Next, the matcher will use the contraster compare the records' values on the preprocessed columns (e.g., how different are the first names in a pair of records?). The [contraster](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/contraster.py#L42) contains several methods for making comparisons on a column in the preprocessed data. Several methods are wrappers for contrast methods available in the [`recordlinkage`](https://pypi.org/project/recordlinkage/) package. New types of contrasts can be created by adding methods to the contraster.
    
        [Configuring the contrasts](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml#L24) is a matter of specifying in a dictionary which methods you would like to call on each preprocessed column, and what arguments, if any, you would like to pass to that method. The top level keys are the names of the preprocessed columns you want to make comparisons on. The values for these keys are lists of dictionaries with the keys `method` and `args` (optional, a dictionary of arguments to be passed to the named method). Each `method`/`args` pair should be preceded by a `-` to indicate that it is an item in the list. The following configuration will make three contrasts on the `first_name` field (do the first names match exactly? do the first names have exactly the same first 5 letters? how far apart are the first names using the [Jaro-Winkler metric](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)?) and two comparisons on the `race` field (do the two records share any races? do they share all of their races?):
    
            contrasts:
                first_name:
                    - method: compare_exact 
                    - method: compare_exact 
                      args:
                           n_chars: 5
                    - method: compare_string_distance
                      args:
                           method: jarowinkler
                race:
                    - method: compare_list
                      args:
                           method: any
                    - method: compare_list
                      args:
                           method: all
        
        It is important to note here that including a column in the *keys* section of the configuration will ensure that it is used for exact deduplication in step 2, but if you would like it to be used in the record linkage process, you must include one or more contrasts on that column. In addition, if you rename a column or create a new column in any changes to the preprocessing step, you will need to add a key and contrasts for that column to the contrasts section of the configuration file.
        
    - **Scoring:** The contrasts step creates many different comparisons for a pair of records; the scoring step combines all of these comparisons into a single distance score that summarizes how different the two records are, with lower scores indicating more similar records. The matcher has several options for scoring when it calls the [`compactify()`](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) function. The default in the matcher itself is to take the simple mean of all of the contrast values. This can be changed by changed the `operation` parameter [when the `compactify()` function is called](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) and/or by adding new operations to the `compactify()` function.
    
    - **Clustering and assigning matched_ids:** To determine which groups of records belong to a single person, the matcher uses a [clustering algorithm](https://en.wikipedia.org/wiki/Cluster_analysis). Which algorithm it uses and the hyperparameters of the algorithm are specified in the [clusterer section of the matcher config](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml#L101). This section should contain an installed `method` as a top level key and a dictionary of `args` to pass to that method. 
    
            clusterer:
                method: sklearn.cluster.DBSCAN
                args:
                    eps: 0.2
                    min_samples: 1
                    algorithm: auto
                    leaf_size: 30
                    n_jobs: 4

        The matcher has only been tested with [scikit-learn's implementation of DBSCAN](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) and will not work with any other method without making code changes to the [clusterer](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/cluster.py).
        
5. **Saving results and notifying the webapp:** Once the record linkage step is done, the matcher has a dataframe of deduplicated and matched records. To [complete its output](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/ioutils.py#L111), it re-loads the original source data and joins the matched ids to each table's primary key, writing the results to a file named `matched` in the same directory as the merged data it received from the webapp. It then notifies the webapp that its job is complete, so the webapp can upload the new matched_ids to the database and make the results available to end users.

## Common Adjustments to the Matcher

### Adding or Increasing Use of a Data Field
If you would like to add a new field to the matcher algorithm, you will need to add it in multiple places in the [matcher configuration file](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml). The column name should be listed as a key in the `keys` section of the configuration file. This will cause it to be used for exact deduplication and to be included in the data sent to the matcher algorithm. You may also wish to add [pre-processing steps](https://github.com/dssg/matching-tool/blob/81ed73ba55dc4a6bccbce789325ca8c0a47c8684/matcher/matcher/preprocess.py) to reformat the data before matching. To compare records on this field in the matcher, you will need to add contasts to the `contrasts` section of the configuration file. 

Because the default behavior of the matcher when it calls the [`compactify()`](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) function is to take a simple average of the contrasts, adding more contrasts for a field adds more weight to that field. For example, in the [default configuration file](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml), there are six comparisons for first name but only one comparison for middle name, meaning that the matcher weights the first name six times as strongly as the middle name. If we wanted to weight middle name higher, we could add additional contrasts on the middle name, such as examining the Jaro-Winkler distance between the middle names in a pair of records. Note that if you add the same contrast multiple times for a single data field, they will overwrite each other rather than being used multiple times. You can see what a newly added contrast looks like and how it affects the scores by examining the cached contrasts in the `match_cache/contrasts` folder in the jurisdiction's root storage directory.

Manually assigning weights to each contrast would require code changes to the [`compactify()`](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) function to support weighting (and to allow for user input of weighting).

### Removing or Decreasing Use of a Data Field
If you would like to remove a field from the matcher algorithm completely, you will need to remove it from both the `keys` and the `contrasts` sections of the [matcher configuration file](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml). The column name should be listed as a key in the `keys` section of the configuration file.

If you simply would like decrease how much that matcher uses the data field, you should remove contrasts for that field. Because the default behavior of the matcher when it calls the [`compactify()`](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) function is to take a simple average of the contrasts, removing some of the contrasts for a field will decrease the weight to that field. For example, in the [default configuration file](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml), there are six comparisons for first name but only one comparison for middle name, meaning that the matcher weights the first name six times as strongly as the middle name. If we wanted to decrease the relative weight of the first name, we could remove contrasts on the first name, such as only comparing the exact first name and its Jaro-Winkler distance. Then, first name would only be counted twice as much as middle name. However, we would also have changed *how* we use first name by discregarding partial string comparisons on the first and last 3 and 5 letters. You can see how this change affects the scores by examining the cached contrasts in the `match_cache/contrasts` folder in the jurisdiction's root storage directory.

Manually assigning weights to each contrast would require code changes to the [`compactify()`](https://github.com/dssg/matching-tool/blob/master/matcher/matcher/rules.py#L18) function to support weighting (and to allow for user input of weighting).

### Stopping the Matcher from Caching so Many Files
The matcher stores a lot of information in its cache to allow you to diagnose problems and test how changes to the configuration affect different stages of the process (e.g., what does a newly added contrast look like? how does it affect the scores?). These are stored in the `match_cache` folder in your base directory. This folder can be occasionally cleared to remove the backlog of files.

If you find the space used by the matcher excessive, or if you are not making changes to the matching algorithm that you want to test, you may want to disable much of this caching. To do this remove or comment out the lines in the matcher where it writes these files to disk using the `write_dataframe()` function:

 - [cluster.py](https://github.com/dssg/matching-tool/blob/81ed73ba55dc4a6bccbce789325ca8c0a47c8684/matcher/matcher/cluster.py#L73) caches the squared distance matrix and the raw cluster ids for each block, so there are two lines to remove.
 - [matcher.py](https://github.com/dssg/matching-tool/blob/81ed73ba55dc4a6bccbce789325ca8c0a47c8684/matcher/matcher/matcher.py#L83) caches the contrasts for each block.
 - [ioutils.py](https://github.com/dssg/matching-tool/blob/0dac113cb1652c956c2e7358cd1e6163ca7aff25/matcher/matcher/ioutils.py#L73) caches the loaded, deduplicated data.
 - [preprocess.py](https://github.com/dssg/matching-tool/blob/81ed73ba55dc4a6bccbce789325ca8c0a47c8684/matcher/matcher/preprocess.py#L83) caches the preprocessed data to allow you to examine the affect of preprocessing on the raw data.

**Note:** Only remove `write_dataframe()` calls writing to the `match_cache`. Other writes are critical to the function of the matching tool.
