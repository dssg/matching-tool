# Schemas 

### Internal Person ID
#### **Data Field Column Name** : `internal_person_id`
#### **Data Field Type** : `varchar`
#### **Description** : `Internal database identification number associated with the individual`
#### **Required by Upload System** : `* - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Internal Event ID
#### **Data Field Column Name** : `internal_event_id`
#### **Data Field Type** : `varchar`
#### **Description** : `Internal database unique primary key for booking table`
#### **Required by Upload System** : `~ - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Internal Charge ID
#### **Data Field Column Name** : `internal_charge_id`
#### **Data Field Type** : `varchar`
#### **Description** : `Internal database identification number for the charge/statute (if exists)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Inmate Number
#### **Data Field Column Name** : `inmate_number`
#### **Data Field Type** : `varchar`
#### **Description** : `County or Jurisdiction identifier for inmates (if different from Internal ID)`
#### **Required by Upload System** : `* - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Full Name
#### **Data Field Column Name** : `full_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name of the individual; formatted in the order it would be spoken`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Prefix
#### **Data Field Column Name** : `prefix`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Prefix for an individual's name`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### First Name
#### **Data Field Column Name** : `first_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `First name of the individual`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Middle Name
#### **Data Field Column Name** : `middle_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Middle name or middle initial of the individual`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Last Name
#### **Data Field Column Name** : `last_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Last name of the individual`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Suffix
#### **Data Field Column Name** : `suffix`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Suffix of the individual's name`
#### **Required by Upload System** : `* either full name or name parts required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Birthdate
#### **Data Field Column Name** : `dob`
#### **Data Field Type** : `date`
#### **Description** : `Date of birth for the individual (YYYY-MM-DD); fill in any missing digits with Xs`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### SSN
#### **Data Field Column Name** : `ssn`
#### **Data Field Type** : `char(9)`
#### **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
#### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Hash SSN
#### **Data Field Column Name** : `ssn_hash`
#### **Data Field Type** : `text`
#### **Description** : `Hashed social security number of the individual.`
#### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Hash SSN Bigrams
#### **Data Field Column Name** : `ssn_bigrams`
#### **Data Field Type** : `text`
#### **Description** : `Hashed bigrams of the individuals social security number. This should be a list of 10 hashed values separated by commas.`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Fingerprint ID
#### **Data Field Column Name** : `fingerprint_id`
#### **Data Field Type** : `varchar`
#### **Description** : `Internal ID number based on the individual's fingerprint, if different from internal id or inmate number`
#### **Required by Upload System** : `* - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### DMV Number
#### **Data Field Column Name** : `dmv_number`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Number on state-issued DMV ID`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### DMV State
#### **Data Field Column Name** : `dmv_state`
#### **Data Field Type** : `char(2)-uppercase`
#### **Description** : `State in which the DMV ID was issued`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Name of Additional State or Federal ID
#### **Data Field Column Name** : `additional_id_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `The name of an additional state or federal ID collected`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Additional State or Federal ID
#### **Data Field Column Name** : `additional_id_number`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `The number collected from an additional state or federal ID named above (e.g., FBI identification number)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Race/Ethnicity
#### **Data Field Column Name** : `race`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Inmate doesn't know, R = Inmate refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Ethnicity
#### **Data Field Column Name** : `ethnicity`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, INMATE DOESN'T KNOW, INMATE REFUSED, DATA NOT COLLECTED)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Sex/Gender
#### **Data Field Column Name** : `sex`
#### **Data Field Type** : `char(2)-uppercase`
#### **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Inmate doesn't know, R = Inmate Refused, N = Data not collected)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Hair Color
#### **Data Field Column Name** : `hair_color`
#### **Data Field Type** : `char(3)-uppercase`
#### **Description** : `Color of the individual's hair (BLD = Bald, BLK = Black, BLN = Blond or Strawberry, BLU = Blue, BRO = Brown, GRY = Gray or Partially Gray, GRN = Green, ONG = Orange, PNK = Pink, PLE = Purple, RED = Red or Auburn, SDY = Sandy, WHI = White, XXX = Unknown or Completely Bald)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Eye Color
#### **Data Field Column Name** : `eye_color`
#### **Data Field Type** : `char(3)-uppercase`
#### **Description** : `Color of the individual's eyes (BLK = Black, BRO = Brown, GRN = Green, MAR = Maroon, PNK = Pink, BLU = Blue, GRY = Gray, HAZ = Hazel, MUL = Multicolored, XXX = Unknown)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Height 
#### **Data Field Column Name** : `height`
#### **Data Field Type** : `int`
#### **Description** : `individual's height, recorded in three digits, with the first digit indicating feet and the second and third digits indicating inches`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Weight
#### **Data Field Column Name** : `weight`
#### **Data Field Type** : `int`
#### **Description** : `Individual's weight, in pounds`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Street Address
#### **Data Field Column Name** : `street_address`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Residential street address of the individual`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### City
#### **Data Field Column Name** : `city`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `City in which in the individual resides`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### State
#### **Data Field Column Name** : `state`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `State in which the individual resides`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Postal Code
#### **Data Field Column Name** : `postal_code`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Postal code of the individual's residential street address`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### County
#### **Data Field Column Name** : `county`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `County in which the individual resides`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Country
#### **Data Field Column Name** : `country`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Country in which the individual resides`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Birth Place
#### **Data Field Column Name** : `birth_place`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Individual's place of birth`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Booking Number
#### **Data Field Column Name** : `booking_number`
#### **Data Field Type** : `varchar`
#### **Description** : `Booking number (if an additional number is used beyond the internal database id) and should be unique to each row`
#### **Required by Upload System** : `~ - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Charge Date
#### **Data Field Column Name** : `charge_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Date the charge was applied (YYYY-MM-DDTHH:MM:SS+TZ)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Charge Position
#### **Data Field Column Name** : `charge_position`
#### **Data Field Type** : `int`
#### **Description** : `Position of the charge in the list of charges for a case or arrest.`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Statute
#### **Data Field Column Name** : `statute`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Statute charge was filed as`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Charge Description
#### **Data Field Column Name** : `charge_desc`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Description of statute`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Charge Type
#### **Data Field Column Name** : `charge_type`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `Whether the charge is a Felony (F), Misdemeanor (M), Civil (C), Traffic (T), Infraction (I), or Other (O)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Offense Category
#### **Data Field Column Name** : `offense_category`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `The category of the offense (e.g., PERSON, SEXUAL, PROPERTY, WEAPONS, DRUG)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Charge Class
#### **Data Field Column Name** : `charge_class`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `The class/severity of the offense (e.g., a Class IV felony would be entered as 4, and a Class B misdemeanor would be entered as B)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Bond Amount
#### **Data Field Column Name** : `bond_amount`
#### **Data Field Type** : `numeric`
#### **Description** : `The amount of bond assigned for the charge, in dollars`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Source
#### **Data Field Column Name** : `source_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name of the data source, such as the court office providing the data`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `YES`
#### **Nullable** : `YES`


### Date Created
#### **Data Field Column Name** : `created_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Date Updated
#### **Data Field Column Name** : `updated_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`