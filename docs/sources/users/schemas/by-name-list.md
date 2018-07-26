# By-Name Schema

### 1. Internal Person ID
##### **Data Field Column Name** : `internal_person_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database identification number associated with the individual`
##### **Example** : `A023918475`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 2. Internal Event ID
##### **Data Field Column Name** : `internal_event_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database unique primary key for table`
##### **Example** : `498376`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 3. Full Name
##### **Data Field Column Name** : `full_name`
##### **Data Field Type** : `text`
##### **Description** : `Name of the individual; formatted in the order it would be spoken`
##### **Example** : `JANE ANDREA SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 4. Prefix
##### **Data Field Column Name** : `prefix`
##### **Data Field Type** : `text`
##### **Description** : `Prefix for an individual's name`
##### **Example** : `MS`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 5. First Name
##### **Data Field Column Name** : `first_name`
##### **Data Field Type** : `text`
##### **Description** : `First name of the individual`
##### **Example** : `JANE`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 6. Middle Name
##### **Data Field Column Name** : `middle_name`
##### **Data Field Type** : `text`
##### **Description** : `Middle name or middle initial of the individual`
##### **Example** : `ANDREA`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 7. Last Name
##### **Data Field Column Name** : `last_name`
##### **Data Field Type** : `text`
##### **Description** : `Last name of the individual`
##### **Example** : `SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 8. Suffix
##### **Data Field Column Name** : `suffix`
##### **Data Field Type** : `text`
##### **Description** : `Suffix of the individual's name`
##### **Example** : `JR`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 9. Birthdate
##### **Data Field Column Name** : `dob`
##### **Data Field Type** : `date`
##### **Description** : `Date of birth for the individual (YYYY-MM-DD or MM/DD/YY); fill in any missing digits with Xs`
##### **Example** : `1982-02-XX`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 10. SSN
##### **Data Field Column Name** : `ssn`
##### **Data Field Type** : `char(9)`
##### **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
##### **Example** : `XXXXX1234`
##### **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 11. SSN Last 4
##### **Data Field Column Name** : `ssn_last_4`
##### **Data Field Type** : `char(4)`
##### **Description** : `Last four digits of the social security number, if this is the only information that is collected.`
##### **Example** : `1234`
##### **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 12. Hash SSN
##### **Data Field Column Name** : `ssn_hash`
##### **Data Field Type** : `text`
##### **Description** : `Hashed social security number of the individual.`
##### **Example** : `f7c3bc1d808e04732adf679965ccc34ca7ae3441`
##### **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 13. Hash SSN Bigrams
##### **Data Field Column Name** : `ssn_bigrams`
##### **Data Field Type** : `text`
##### **Description** : `Hashed bigrams of the individuals social security number. This should be a list of 10 hashed values separated by commas.`
##### **Example** : `7b52009b64fd0a2a49e6d8a939753077792b0554,d435a6cdd786300dff204ee7c2ef942d3e9034e2,f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59,fb644351560d8296fe6da332236b1f8d61b2828a,54ceb91256e8190e474aa752a6e0650a2df5ba37,4d89d294cd4ca9f2ca57dc24a53ffb3ef5303122,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 14. DMV Number
##### **Data Field Column Name** : `dmv_number`
##### **Data Field Type** : `varchar`
##### **Description** : `Number on state-issued DMV ID`
##### **Example** : `S123-4567-7890`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 15. DMV State
##### **Data Field Column Name** : `dmv_state`
##### **Data Field Type** : `varchar(2)`
##### **Description** : `State in which the DMV ID was issued`
##### **Example** : `IL`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 16. Name of Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_name`
##### **Data Field Type** : `varchar`
##### **Description** : `The name of an additional state or federal ID collected`
##### **Example** : `CANADIAN SOCIAL INSURANCE NUMBER`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 17. Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_number`
##### **Data Field Type** : `varchar`
##### **Description** : `The number collected from an additional state or federal ID named above (e.g., FBI identification number)`
##### **Example** : `A12B3256`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 18. Race/Ethnicity
##### **Data Field Column Name** : `race`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Person doesn't know, R = Person refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### **Example** : `B`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 19. Ethnicity
##### **Data Field Column Name** : `ethnicity`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, PERSON DOESN'T KNOW, PERSON REFUSED, DATA NOT COLLECTED)`
##### **Example** : `HISPANIC`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 20. Sex/Gender
##### **Data Field Column Name** : `sex`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Person doesn't know, R = Person Refused, N = Data not collected)`
##### **Example** : `F`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 21. List Entry Date
##### **Data Field Column Name** : `list_entry_date`
##### **Data Field Type** : `date`
##### **Description** : `Date when person was identified as homeless or was added to the list. (YYYY-MM-DD or MM/DD/YY)`
##### **Example** : `7/15/04`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `NO`


### 22. Inactive Date
##### **Data Field Column Name** : `inactive_date`
##### **Data Field Type** : `date`
##### **Description** : `If the person is currently inactive with respect to the list (e.g., they are housed), the date this status started. (YYYY-MM-DD or MM/DD/YY)`
##### **Example** : `3/13/05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `NO`


### 23. Unsheltered Flag
##### **Data Field Column Name** : `unsheltered`
##### **Data Field Type** : `char(1)`
##### **Description** : `Indicator identifying whether or not the individual was unsheltered (N=No, Y=Yes, NULL=Missing)`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 24. Disability Flag
##### **Data Field Column Name** : `disability`
##### **Data Field Type** : `char(1)`
##### **Description** : `Indicator identifying whether or not the individual has a disability (N=No, Y=Yes, NULL=Missing)`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 25. Veteran Flag
##### **Data Field Column Name** : `veteran`
##### **Data Field Type** : `char(1)`
##### **Description** : `Indicator identifying whether or not the individual was identified as a veteran (N=No, Y=Yes, NULL=Missing)`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 26. CAT Date
##### **Data Field Column Name** : `cat_date`
##### **Data Field Type** : `date`
##### **Description** : `Date common assessment tool (e.g., VI-SPDAT) was last administered. (YYYY-MM-DD or MM/DD/YY)`
##### **Example** : `7/15/04`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 27. CAT Score
##### **Data Field Column Name** : `cat_score`
##### **Data Field Type** : `text`
##### **Description** : `Score on common assessment tool`
##### **Example** : `12`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 28. Source
##### **Data Field Column Name** : `source_name`
##### **Data Field Type** : `text`
##### **Description** : `Name of the data source, such as the office or service provider uploading the data`
##### **Example** : `Homeless Alliance of Dove County`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 29. Date Created
##### **Data Field Column Name** : `created_date`
##### **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 30. Date Updated
##### **Data Field Column Name** : `updated_date`
##### **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-19T01:23:45+05`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`