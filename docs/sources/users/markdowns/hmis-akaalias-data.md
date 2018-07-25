# Schemas

### 1. **Internal Person ID**
    1. **Data Field Column Name** : `internal_person_id`
    2. **Data Field Type** : `varchar`
    3. **Description** : `Internal database identification number associated with the individual`
    4. **Required by Upload System** : `NO`
    5. **Required for Good Match** : `YES`
    6. **Nullable** : `YES`


### 2. Internal Event ID
##### * **Data Field Column Name** : `internal_event_id`
##### * **Data Field Type** : `varchar`
##### * **Description** : `Internal database unique primary key for table`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 3. Full Name
##### * **Data Field Column Name** : `full_name`
##### * **Data Field Type** : `text`
##### * **Description** : `Name of the individual; formatted in the order it would be spoken`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `NO`


### 4. Prefix
##### * **Data Field Column Name** : `prefix`
##### * **Data Field Type** : `text`
##### * **Description** : `Prefix for an individual's name`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 5. First Name
##### * **Data Field Column Name** : `first_name`
##### * **Data Field Type** : `text`
##### * **Description** : `First name of the individual`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 6. Middle Name
##### * **Data Field Column Name** : `middle_name`
##### * **Data Field Type** : `text`
##### * **Description** : `Middle name or middle initial of the individual`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 7. Last Name
##### * **Data Field Column Name** : `last_name`
##### * **Data Field Type** : `text`
##### * **Description** : `Last name of the individual`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `NO`


### 8. Suffix
##### * **Data Field Column Name** : `suffix`
##### * **Data Field Type** : `text`
##### * **Description** : `Suffix of the individual's name`
##### * **Required by Upload System** : `* either full name or name parts required but not both`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 9. Birthdate
##### * **Data Field Column Name** : `dob`
##### * **Data Field Type** : `date`
##### * **Description** : `Date of birth for the individual (YYYY-MM-DD or MM/DD/YY); fill in any missing digits with Xs`
##### * **Required by Upload System** : `YES`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 10. SSN
##### * **Data Field Column Name** : `ssn`
##### * **Data Field Type** : `char(9)`
##### * **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
##### * **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 11. SSN Last 4
##### * **Data Field Column Name** : `ssn_last_4`
##### * **Data Field Type** : `char(4)`
##### * **Description** : `Last four digits of the social security number, if this is the only information that is collected.`
##### * **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 12. Hash SSN
##### * **Data Field Column Name** : `ssn_hash`
##### * **Data Field Type** : `text`
##### * **Description** : `Hashed social security number of the individual.`
##### * **Required by Upload System** : `** either SSN, SSN Last 4, or hashed SSN are required but not all three`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 13. Hash SSN Bigrams
##### * **Data Field Column Name** : `ssn_bigrams`
##### * **Data Field Type** : `text`
##### * **Description** : `Hashed bigrams of the individuals social security number. This should be a list of 10 hashed values separated by commas.`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 14. DMV Number
##### * **Data Field Column Name** : `dmv_number`
##### * **Data Field Type** : `varchar`
##### * **Description** : `Number on state-issued DMV ID`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 15. DMV State
##### * **Data Field Column Name** : `dmv_state`
##### * **Data Field Type** : `varchar(2)`
##### * **Description** : `State in which the DMV ID was issued`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 16. Name of Additional State or Federal ID
##### * **Data Field Column Name** : `additional_id_name`
##### * **Data Field Type** : `varchar`
##### * **Description** : `The name of an additional state or federal ID collected`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 17. Additional State or Federal ID
##### * **Data Field Column Name** : `additional_id_number`
##### * **Data Field Type** : `varchar`
##### * **Description** : `The number collected from an additional state or federal ID named above (e.g., FBI identification number)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 18. Race/Ethnicity
##### * **Data Field Column Name** : `race`
##### * **Data Field Type** : `char(1)-uppercase`
##### * **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Person doesn't know, R = Person refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### * **Required by Upload System** : `YES`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 19. Ethnicity
##### * **Data Field Column Name** : `ethnicity`
##### * **Data Field Type** : `text-uppercase`
##### * **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, PERSON DOESN'T KNOW, PERSON REFUSED, DATA NOT COLLECTED)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 20. Sex/Gender
##### * **Data Field Column Name** : `sex`
##### * **Data Field Type** : `char(2)-uppercase`
##### * **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Person doesn't know, R = Person Refused, N = Data not collected)`
##### * **Required by Upload System** : `YES`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 21. List Entry Date
##### * **Data Field Column Name** : `list_entry_date`
##### * **Data Field Type** : `date`
##### * **Description** : `Date when person was identified as homeless or was added to the list. (YYYY-MM-DD or MM/DD/YY)`
##### * **Required by Upload System** : `YES`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `NO`


### 22. Inactive Date
##### * **Data Field Column Name** : `inactive_date`
##### * **Data Field Type** : `date`
##### * **Description** : `If the person is currently inactive with respect to the list (e.g., they are housed), the date this status started. (YYYY-MM-DD or MM/DD/YY)`
##### * **Required by Upload System** : `YES`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `NO`


### 23. Unsheltered Flag
##### * **Data Field Column Name** : `unsheltered`
##### * **Data Field Type** : `char(1)`
##### * **Description** : `Indicator identifying whether or not the individual was unsheltered (N=No, Y=Yes, NULL=Missing)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 24. Disability Flag
##### * **Data Field Column Name** : `disability`
##### * **Data Field Type** : `char(1)`
##### * **Description** : `Indicator identifying whether or not the individual has a disability (N=No, Y=Yes, NULL=Missing)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 25. Veteran Flag
##### * **Data Field Column Name** : `veteran`
##### * **Data Field Type** : `char(1)`
##### * **Description** : `Indicator identifying whether or not the individual was identified as a veteran (N=No, Y=Yes, NULL=Missing)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 26. CAT Date
##### * **Data Field Column Name** : `cat_date`
##### * **Data Field Type** : `date`
##### * **Description** : `Date common assessment tool (e.g., VI-SPDAT) was last administered. (YYYY-MM-DD or MM/DD/YY)`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 27. CAT Score
##### * **Data Field Column Name** : `cat_score`
##### * **Data Field Type** : `text`
##### * **Description** : `Score on common assessment tool`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 28. Source
##### * **Data Field Column Name** : `source_name`
##### * **Data Field Type** : `text`
##### * **Description** : `Name of the data source, such as the office or service provider uploading the data`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `YES`
##### * **Nullable** : `YES`


### 29. Date Created
##### * **Data Field Column Name** : `created_date`
##### * **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### * **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`


### 30. Date Updated
##### * **Data Field Column Name** : `updated_date`
##### * **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### * **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### * **Required by Upload System** : `NO`
##### * **Required for Good Match** : `NO`
##### * **Nullable** : `YES`