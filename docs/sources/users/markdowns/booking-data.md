# Schemas - Data Fields

### 1. Internal Person ID
##### **Data Field Column Name** : `internal_person_id`
##### **Data Field Type** : `varchar`
##### **Description** : `The primary internal database identification number associated with the individual. If there is also a secondary person ID, use this field for the highest quality id (i.e., the one most trusted to identify unique individuals)`
##### **Example** : `A023918475`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 2. Internal Event ID
##### **Data Field Column Name** : `internal_event_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database unique primary key for table`
##### **Example** : `498376`
##### **Required by Upload System** : `~ - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 3. Inmate Number
##### **Data Field Column Name** : `inmate_number`
##### **Data Field Type** : `varchar`
##### **Description** : `County or Jurisdiction identifier for inmates (if different from Internal ID)`
##### **Example** : `MA94816`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 4. Full Name
##### **Data Field Column Name** : `full_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the individual; formatted in the order it would be spoken`
##### **Example** : `JANE ANDREA SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 5. Prefix
##### **Data Field Column Name** : `prefix`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Prefix for an individual's name`
##### **Example** : `MS`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 6. First Name
##### **Data Field Column Name** : `first_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `First name of the individual`
##### **Example** : `JANE`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 7. Middle Name
##### **Data Field Column Name** : `middle_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Middle name or middle initial of the individual`
##### **Example** : `ANDREA`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 8. Last Name
##### **Data Field Column Name** : `last_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Last name of the individual`
##### **Example** : `SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 9. Suffix
##### **Data Field Column Name** : `suffix`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Suffix of the individual's name`
##### **Example** : `JR`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 10. Birthdate
##### **Data Field Column Name** : `dob`
##### **Data Field Type** : `date`
##### **Description** : `Date of birth for the individual (YYYY-MM-DD); fill in any missing digits with Xs`
##### **Example** : `1982-02-XX`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 11. SSN
##### **Data Field Column Name** : `ssn`
##### **Data Field Type** : `char(9)`
##### **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
##### **Example** : `XXXXX1234`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 12. Hash SSN
##### **Data Field Column Name** : `ssn_hash`
##### **Data Field Type** : `text`
##### **Description** : `Hashed social security number of the individual.`
##### **Example** : `f7c3bc1d808e04732adf679965ccc34ca7ae3441`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
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


### 14. Fingerprint ID
##### **Data Field Column Name** : `fingerprint_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal ID number based on the individual's fingerprint, if different from internal id or inmate number`
##### **Example** : `9876543`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 15. DMV Number
##### **Data Field Column Name** : `dmv_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number on state-issued DMV ID`
##### **Example** : `S123-4567-7890`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 16. DMV State
##### **Data Field Column Name** : `dmv_state`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `State in which the DMV ID was issued`
##### **Example** : `IL`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 17. Name of Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The name of an additional state or federal ID collected`
##### **Example** : `CANADIAN SOCIAL INSURANCE NUMBER`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 18. Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The number collected from an additional state or federal ID named above (e.g., FBI identification number)`
##### **Example** : `A12B3256`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 19. Race/Ethnicity
##### **Data Field Column Name** : `race`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Inmate doesn't know, R = Inmate refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### **Example** : `B`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 20. Ethnicity
##### **Data Field Column Name** : `ethnicity`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, INMATE DOESN'T KNOW, INMATE REFUSED, DATA NOT COLLECTED)`
##### **Example** : `HISPANIC`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 21. Sex/Gender
##### **Data Field Column Name** : `sex`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Inmate doesn't know, R = Inmate Refused, N = Data not collected)`
##### **Example** : `F`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 22. Hair Color
##### **Data Field Column Name** : `hair_color`
##### **Data Field Type** : `char(3)-uppercase`
##### **Description** : `Color of the individual's hair (BLD = Bald, BLK = Black, BLN = Blond or Strawberry, BLU = Blue, BRO = Brown, GRY = Gray or Partially Gray, GRN = Green, ONG = Orange, PNK = Pink, PLE = Purple, RED = Red or Auburn, SDY = Sandy, WHI = White, S/P = salt and pepper, BLE = bleached, OTH = other, XXX = Unknown or Completely Bald)`
##### **Example** : `PNK`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 23. Eye Color
##### **Data Field Column Name** : `eye_color`
##### **Data Field Type** : `char(3)-uppercase`
##### **Description** : `Color of the individual's eyes (BLK = Black, BRO = Brown, GRN = Green, MAR = Maroon, PNK = Pink, BLU = Blue, GRY = Gray, HAZ = Hazel, MUL = Multicolored, XXX = Unknown)`
##### **Example** : `MUL`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 24. Height 
##### **Data Field Column Name** : `height`
##### **Data Field Type** : `int`
##### **Description** : `individual's height, recorded in three digits, with the first digit indicating feet and the second and third digits indicating inches`
##### **Example** : `507`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 25. Weight
##### **Data Field Column Name** : `weight`
##### **Data Field Type** : `int`
##### **Description** : `Individual's weight, in pounds`
##### **Example** : `165`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 26. Street Address
##### **Data Field Column Name** : `street_address`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Residential street address of the individual`
##### **Example** : `123 MAIN ST`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 27. City
##### **Data Field Column Name** : `city`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `City in which in the individual resides`
##### **Example** : `PLEASANTVILLE`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 28. State
##### **Data Field Column Name** : `state`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `State in which the individual resides`
##### **Example** : `MD`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 29. Postal Code
##### **Data Field Column Name** : `postal_code`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Postal code of the individual's residential street address`
##### **Example** : `12334`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 30. County
##### **Data Field Column Name** : `county`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `County in which the individual resides`
##### **Example** : `DOVE COUNTY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 31. Country
##### **Data Field Column Name** : `country`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Country in which the individual resides`
##### **Example** : `USA`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 32. Birth Place
##### **Data Field Column Name** : `birth_place`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Individual's place of birth`
##### **Example** : `INDIANAPOLIS, IN`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 33. Booking Number
##### **Data Field Column Name** : `booking_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Jail system identifier for booking event, if different from internal event ID`
##### **Example** : `I3958-12`
##### **Required by Upload System** : `~ - at least 1`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 34. Jail Entry Date
##### **Data Field Column Name** : `jail_entry_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date when the individual entered jail (YYYY-MM-DDTHH:MM:SS+TZ)`
##### **Example** : `2004-07-15T1:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `NO`


### 35. Jail Exit Date
##### **Data Field Column Name** : `jail_exit_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date when the individual exited jail (YYYY-MM-DDTHH:MM:SS+TZ)`
##### **Example** : `2004-07-19T13:45:06+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 36. Homelessness Flag
##### **Data Field Column Name** : `homeless`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Indicator identifying whether or not the individual was homeless (N=No, Y=Yes)`
##### **Example** : `N`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 37. Mental Health Flag
##### **Data Field Column Name** : `mental_health`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Indicator identifying whether or not the individual was identified as having mental health symptoms (N=No, Y=Yes)`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 38. Veteran Flag
##### **Data Field Column Name** : `veteran`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Indicator identifying whether or not the individual was identified as a veteran (N=No, Y=Yes)`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 39. Special Initiative
##### **Data Field Column Name** : `special_initiative`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `This field can be used to flag whether someone was booked under a special initiative or program that may be useful in identifying or prioritizing clients for housing services. Values should be Y or N to indicate whether someone was arrested as part of a special initiative.`
##### **Example** : `N`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 40. Bond Amount
##### **Data Field Column Name** : `bond_amount`
##### **Data Field Type** : `int`
##### **Description** : `Dollar amount of bond set for this jail stay`
##### **Example** : `5000`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 41. Arresting Agency
##### **Data Field Column Name** : `arresting_agency`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of agency (e.g., police department) that arrested the individual`
##### **Example** : `DOVE COUNTY POLICE`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 42. Bed Number
##### **Data Field Column Name** : `bed`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number of the bed in a multi-person cell where the individual is housed`
##### **Example** : `1`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 43. Cell Number
##### **Data Field Column Name** : `cell`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number of the cell in which the individual is housed`
##### **Example** : `3A`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 44. Block ID
##### **Data Field Column Name** : `block`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name or number of the housing block or pod where the individual is housed`
##### **Example** : `D`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 45. Building ID
##### **Data Field Column Name** : `building`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name or number of building where the individual is housed`
##### **Example** : `MAIN JAIL`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 46. Annex ID
##### **Data Field Column Name** : `annex`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name or number of annex where the individual is housed`
##### **Example** : `FEMALE`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 47. Floor Number
##### **Data Field Column Name** : `floor`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name or number of the floor where the individual is housed`
##### **Example** : `2`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 48. Classification Code
##### **Data Field Column Name** : `classification`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Classification or security group code for the housing unit where the individual is located`
##### **Example** : `III`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 49. Detention Type
##### **Data Field Column Name** : `detention`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Type of detention or custody to which the person is assigned (e.g., PRETRIAL, SENTENCE, HOLD)`
##### **Example** : `PRETRIAL`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 50. Location Type
##### **Data Field Column Name** : `location_type`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Housing type classification, if additional information is recorded or if location is not able to be formatted in the other fields (e.g., general population, high security, periodic imprisonment, electronic monitoring, medical needs, etc.)`
##### **Example** : `*custom`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 51. Location Date
##### **Data Field Column Name** : `location_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Time moved into a new location type; if location data are not provided, should be a copy of Jail Entry Date (YYYY-MM-DDTHH:MM:SS+TZ)`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `NO`


### 52. Case Number
##### **Data Field Column Name** : `case_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Case number or court docket associated with booking`
##### **Example** : `17CR002184`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 53. Source
##### **Data Field Column Name** : `source_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the data source, such as the specific jail`
##### **Example** : `DOVE COUNTY CORRECTIONAL FACILITY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 54. Date Created
##### **Data Field Column Name** : `created_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 55. Date Updated
##### **Data Field Column Name** : `updated_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-19T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`