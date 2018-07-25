# Schemas - Data Fields

### Internal Person ID
#### **Data Field Column Name** : `internal_person_id`
#### **Data Field Type** : `varchar`
#### **Description** : `The primary internal database identification number associated with the individual. If there is also a secondary person ID, use this field for the highest quality id (i.e., the one most trusted to identify unique individuals)`
#### **Required by Upload System** : `* - at least 1`
#### **Required for Good Match** : `YES`
#### **Nullable** : `NO`


### Internal Event ID
#### **Data Field Column Name** : `internal_event_id`
#### **Data Field Type** : `varchar`
#### **Description** : `Internal database unique primary key for table`
#### **Required by Upload System** : `~ - at least 1`
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
#### **Description** : `Color of the individual's hair (BLD = Bald, BLK = Black, BLN = Blond or Strawberry, BLU = Blue, BRO = Brown, GRY = Gray or Partially Gray, GRN = Green, ONG = Orange, PNK = Pink, PLE = Purple, RED = Red or Auburn, SDY = Sandy, WHI = White, S/P = salt and pepper, BLE = bleached, OTH = other, XXX = Unknown or Completely Bald)`
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
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Jail system identifier for booking event, if different from internal event ID`
#### **Required by Upload System** : `~ - at least 1`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Jail Entry Date
#### **Data Field Column Name** : `jail_entry_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Date when the individual entered jail (YYYY-MM-DDTHH:MM:SS+TZ)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `NO`


### Jail Exit Date
#### **Data Field Column Name** : `jail_exit_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Date when the individual exited jail (YYYY-MM-DDTHH:MM:SS+TZ)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Homelessness Flag
#### **Data Field Column Name** : `homeless`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `Indicator identifying whether or not the individual was homeless (N=No, Y=Yes)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Mental Health Flag
#### **Data Field Column Name** : `mental_health`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `Indicator identifying whether or not the individual was identified as having mental health symptoms (N=No, Y=Yes)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Veteran Flag
#### **Data Field Column Name** : `veteran`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `Indicator identifying whether or not the individual was identified as a veteran (N=No, Y=Yes)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Special Initiative
#### **Data Field Column Name** : `special_initiative`
#### **Data Field Type** : `char(1)-uppercase`
#### **Description** : `This field can be used to flag whether someone was booked under a special initiative or program that may be useful in identifying or prioritizing clients for housing services. Values should be Y or N to indicate whether someone was arrested as part of a special initiative.`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Bond Amount
#### **Data Field Column Name** : `bond_amount`
#### **Data Field Type** : `int`
#### **Description** : `Dollar amount of bond set for this jail stay`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Arresting Agency
#### **Data Field Column Name** : `arresting_agency`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name of agency (e.g., police department) that arrested the individual`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Bed Number
#### **Data Field Column Name** : `bed`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Number of the bed in a multi-person cell where the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Cell Number
#### **Data Field Column Name** : `cell`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Number of the cell in which the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Block ID
#### **Data Field Column Name** : `block`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name or number of the housing block or pod where the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Building ID
#### **Data Field Column Name** : `building`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name or number of building where the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Annex ID
#### **Data Field Column Name** : `annex`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name or number of annex where the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Floor Number
#### **Data Field Column Name** : `floor`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name or number of the floor where the individual is housed`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Classification Code
#### **Data Field Column Name** : `classification`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Classification or security group code for the housing unit where the individual is located`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Detention Type
#### **Data Field Column Name** : `detention`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Type of detention or custody to which the person is assigned (e.g., PRETRIAL, SENTENCE, HOLD)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Location Type
#### **Data Field Column Name** : `location_type`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Housing type classification, if additional information is recorded or if location is not able to be formatted in the other fields (e.g., general population, high security, periodic imprisonment, electronic monitoring, medical needs, etc.)`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Location Date
#### **Data Field Column Name** : `location_date`
#### **Data Field Type** : `timestamp with timezone`
#### **Description** : `Time moved into a new location type; if location data are not provided, should be a copy of Jail Entry Date (YYYY-MM-DDTHH:MM:SS+TZ)`
#### **Required by Upload System** : `YES`
#### **Required for Good Match** : `NO`
#### **Nullable** : `NO`


### Case Number
#### **Data Field Column Name** : `case_number`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Case number or court docket associated with booking`
#### **Required by Upload System** : `NO`
#### **Required for Good Match** : `NO`
#### **Nullable** : `YES`


### Source
#### **Data Field Column Name** : `source_name`
#### **Data Field Type** : `text-uppercase`
#### **Description** : `Name of the data source, such as the specific jail`
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
