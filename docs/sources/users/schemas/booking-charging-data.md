# Booking Charge Schema

### 1. Internal Person ID
##### **Data Field Column Name** : `internal_person_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database identification number associated with the individual`
##### **Example** : `A023918475`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 2. Internal Event ID
##### **Data Field Column Name** : `internal_event_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database unique primary key for booking table`
##### **Example** : `498376`
##### **Required by Upload System** : `~ - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 3. Internal Charge ID
##### **Data Field Column Name** : `internal_charge_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database identification number for the charge/statute (if exists)`
##### **Example** : `23028`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 4. Inmate Number
##### **Data Field Column Name** : `inmate_number`
##### **Data Field Type** : `varchar`
##### **Description** : `County or Jurisdiction identifier for inmates (if different from Internal ID)`
##### **Example** : `MA94816`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 5. Full Name
##### **Data Field Column Name** : `full_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the individual; formatted in the order it would be spoken`
##### **Example** : `JANE ANDREA SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 6. Prefix
##### **Data Field Column Name** : `prefix`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Prefix for an individual's name`
##### **Example** : `MS`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 7. First Name
##### **Data Field Column Name** : `first_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `First name of the individual`
##### **Example** : `JANE`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 8. Middle Name
##### **Data Field Column Name** : `middle_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Middle name or middle initial of the individual`
##### **Example** : `ANDREA`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 9. Last Name
##### **Data Field Column Name** : `last_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Last name of the individual`
##### **Example** : `SMITH`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 10. Suffix
##### **Data Field Column Name** : `suffix`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Suffix of the individual's name`
##### **Example** : `JR`
##### **Required by Upload System** : `* either full name or name parts required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 11. Birthdate
##### **Data Field Column Name** : `dob`
##### **Data Field Type** : `date`
##### **Description** : `Date of birth for the individual (YYYY-MM-DD); fill in any missing digits with Xs`
##### **Example** : `1982-02-XX`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 12. SSN
##### **Data Field Column Name** : `ssn`
##### **Data Field Type** : `char(9)`
##### **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
##### **Example** : `XXXXX1234`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 13. Hash SSN
##### **Data Field Column Name** : `ssn_hash`
##### **Data Field Type** : `text`
##### **Description** : `Hashed social security number of the individual.`
##### **Example** : `f7c3bc1d808e04732adf679965ccc34ca7ae3441`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 14. Hash SSN Bigrams
##### **Data Field Column Name** : `ssn_bigrams`
##### **Data Field Type** : `text`
##### **Description** : `Hashed bigrams of the individuals social security number. This should be a list of 10 hashed values separated by commas.`
##### **Example** : `7b52009b64fd0a2a49e6d8a939753077792b0554,d435a6cdd786300dff204ee7c2ef942d3e9034e2,f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59,fb644351560d8296fe6da332236b1f8d61b2828a,54ceb91256e8190e474aa752a6e0650a2df5ba37,4d89d294cd4ca9f2ca57dc24a53ffb3ef5303122,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 15. Fingerprint ID
##### **Data Field Column Name** : `fingerprint_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal ID number based on the individual's fingerprint, if different from internal id or inmate number`
##### **Example** : `9876543`
##### **Required by Upload System** : `* - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 16. DMV Number
##### **Data Field Column Name** : `dmv_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number on state-issued DMV ID`
##### **Example** : `S123-4567-7890`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 17. DMV State
##### **Data Field Column Name** : `dmv_state`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `State in which the DMV ID was issued`
##### **Example** : `IL`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 18. Name of Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The name of an additional state or federal ID collected`
##### **Example** : `CANADIAN SOCIAL INSURANCE NUMBER`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 19. Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The number collected from an additional state or federal ID named above (e.g., FBI identification number)`
##### **Example** : `A12B3256`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 20. Race/Ethnicity
##### **Data Field Column Name** : `race`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Inmate doesn't know, R = Inmate refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### **Example** : `B`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 21. Ethnicity
##### **Data Field Column Name** : `ethnicity`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, INMATE DOESN'T KNOW, INMATE REFUSED, DATA NOT COLLECTED)`
##### **Example** : `HISPANIC`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 22. Sex/Gender
##### **Data Field Column Name** : `sex`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Inmate doesn't know, R = Inmate Refused, N = Data not collected)`
##### **Example** : `F`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 23. Hair Color
##### **Data Field Column Name** : `hair_color`
##### **Data Field Type** : `char(3)-uppercase`
##### **Description** : `Color of the individual's hair (BLD = Bald, BLK = Black, BLN = Blond or Strawberry, BLU = Blue, BRO = Brown, GRY = Gray or Partially Gray, GRN = Green, ONG = Orange, PNK = Pink, PLE = Purple, RED = Red or Auburn, SDY = Sandy, WHI = White, XXX = Unknown or Completely Bald)`
##### **Example** : `PNK`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 24. Eye Color
##### **Data Field Column Name** : `eye_color`
##### **Data Field Type** : `char(3)-uppercase`
##### **Description** : `Color of the individual's eyes (BLK = Black, BRO = Brown, GRN = Green, MAR = Maroon, PNK = Pink, BLU = Blue, GRY = Gray, HAZ = Hazel, MUL = Multicolored, XXX = Unknown)`
##### **Example** : `MUL`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 25. Height 
##### **Data Field Column Name** : `height`
##### **Data Field Type** : `int`
##### **Description** : `individual's height, recorded in three digits, with the first digit indicating feet and the second and third digits indicating inches`
##### **Example** : `507`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 26. Weight
##### **Data Field Column Name** : `weight`
##### **Data Field Type** : `int`
##### **Description** : `Individual's weight, in pounds`
##### **Example** : `165`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 27. Street Address
##### **Data Field Column Name** : `street_address`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Residential street address of the individual`
##### **Example** : `123 MAIN ST`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 28. City
##### **Data Field Column Name** : `city`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `City in which in the individual resides`
##### **Example** : `PLEASANTVILLE`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 29. State
##### **Data Field Column Name** : `state`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `State in which the individual resides`
##### **Example** : `MD`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 30. Postal Code
##### **Data Field Column Name** : `postal_code`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Postal code of the individual's residential street address`
##### **Example** : `12334`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 31. County
##### **Data Field Column Name** : `county`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `County in which the individual resides`
##### **Example** : `DOVE COUNTY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 32. Country
##### **Data Field Column Name** : `country`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Country in which the individual resides`
##### **Example** : `USA`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 33. Birth Place
##### **Data Field Column Name** : `birth_place`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Individual's place of birth`
##### **Example** : `INDIANAPOLIS, IN`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 34. Booking Number
##### **Data Field Column Name** : `booking_number`
##### **Data Field Type** : `varchar`
##### **Description** : `Booking number (if an additional number is used beyond the internal database id) and should be unique to each row`
##### **Example** : `04CR02948`
##### **Required by Upload System** : `~ - at least 1`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 35. Charge Date
##### **Data Field Column Name** : `charge_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date the charge was applied (YYYY-MM-DDTHH:MM:SS+TZ)`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 36. Charge Position
##### **Data Field Column Name** : `charge_position`
##### **Data Field Type** : `int`
##### **Description** : `Position of the charge in the list of charges for a case or arrest.`
##### **Example** : `1`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 37. Statute
##### **Data Field Column Name** : `statute`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Statute charge was filed as`
##### **Example** : `57-203/19A(2)`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 38. Charge Description
##### **Data Field Column Name** : `charge_desc`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Description of statute`
##### **Example** : `AGGRAVATED ASSAULT - SPECIAL VICTIM`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 39. Charge Type
##### **Data Field Column Name** : `charge_type`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Whether the charge is a Felony (F), Misdemeanor (M), Civil (C), Traffic (T), Infraction (I), or Other (O)`
##### **Example** : `F`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 40. Offense Category
##### **Data Field Column Name** : `offense_category`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The category of the offense (e.g., PERSON, SEXUAL, PROPERTY, WEAPONS, DRUG)`
##### **Example** : `PERSON`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 41. Charge Class
##### **Data Field Column Name** : `charge_class`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The class/severity of the offense (e.g., a Class IV felony would be entered as 4, and a Class B misdemeanor would be entered as B)`
##### **Example** : `4`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 42. Bond Amount
##### **Data Field Column Name** : `bond_amount`
##### **Data Field Type** : `numeric`
##### **Description** : `The amount of bond assigned for the charge, in dollars`
##### **Example** : `200`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 43. Source
##### **Data Field Column Name** : `source_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the data source, such as the court office providing the data`
##### **Example** : `DOVE COUNTY JAIL`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 44. Date Created
##### **Data Field Column Name** : `created_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 45. Date Updated
##### **Data Field Column Name** : `updated_date`
##### **Data Field Type** : `timestamp with timezone`
##### **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`