# Homelessness Service Stays Schema

### 1. Internal Person ID
##### **Data Field Column Name** : `internal_person_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database identification number associated with the individual`
##### **Example** : `A023918475`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 2. Secondary Person ID
##### **Data Field Column Name** : `secondary_person_id`
##### **Data Field Type** : `varchar`
##### **Description** : `A secondary internal identification number associatiod with the individual, if one exists`
##### **Example** : `1234-643`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 3. Internal Event ID
##### **Data Field Column Name** : `internal_event_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database identification number associated with the event`
##### **Example** : `248457`
##### **Required by Upload System** : `YES`
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
##### **Example** : `MS.`
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


### 10. Name Data Quality
##### **Data Field Column Name** : `name_data_quality`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The quality of the data provided about the name. Values: FULL NAME REPORTED; PARTIAL, STREET NAME, OR CODE NAME REPORTED; CLIENT DOESN'T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `FULL NAME REPORTED`
##### **Required by Upload System** : `YES`
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


### 12. Date of Birth Type
##### **Data Field Column Name** : `dob_type`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The quality or type of information collected about the individual's date of birth (FULL DOB REPORTED, APPROXIMATE OR PARTIAL DOB REPORTED, CLIENT DOESN'T KNOW, CLIENT REFUSED, DATA NOT COLLECTED)`
##### **Example** : `APPROXIMATE OR PARTIAL DOB REPORTED`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 13. SSN
##### **Data Field Column Name** : `ssn`
##### **Data Field Type** : `char(9)`
##### **Description** : `Social security number of the individual; 9 characters; if a partial SSN is provided, fill the remaining characters with X`
##### **Example** : `XXXXX1234`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 14. Hash SSN
##### **Data Field Column Name** : `ssn_hash`
##### **Data Field Type** : `text`
##### **Description** : `Hashed social security number of the individual.`
##### **Example** : `f7c3bc1d808e04732adf679965ccc34ca7ae3441`
##### **Required by Upload System** : `** either SSN or hashed SSN are required but not both`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 15. Hash SSN Bigrams
##### **Data Field Column Name** : `ssn_bigrams`
##### **Data Field Type** : `text`
##### **Description** : `Hashed bigrams of the individuals social security number. This should be a list of 10 hashed values separated by commas.`
##### **Example** : `7b52009b64fd0a2a49e6d8a939753077792b0554,d435a6cdd786300dff204ee7c2ef942d3e9034e2,f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59,fb644351560d8296fe6da332236b1f8d61b2828a,54ceb91256e8190e474aa752a6e0650a2df5ba37,4d89d294cd4ca9f2ca57dc24a53ffb3ef5303122,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f,eb4ac3033e8ab3591e0fcefa8c26ce3fd36d5a0f`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 16. SSN Data Quality
##### **Data Field Column Name** : `ssn_data_quality`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The quality of the data provided about the SSN. Values: FULL SSN REPORTED; APPROXIMATE OR PARTIAL SSN REPORTED; CLIENT DOESN'T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `APPROXIMATE OR PARTIAL SSN REPORTED`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 17. DMV Number
##### **Data Field Column Name** : `dmv_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number on state-issued DMV ID`
##### **Example** : `S123-4567-7890`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 18. DMV State
##### **Data Field Column Name** : `dmv_state`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `State in which the DMV ID was issued`
##### **Example** : `IL`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 19. Name of Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The name of an additional state or federal ID collected`
##### **Example** : `CANADIAN SOCIAL INSURANCE NUMBER`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 20. Additional State or Federal ID
##### **Data Field Column Name** : `additional_id_number`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Any other state or federal identification number associated with the individual (e.g., FBI identification number, Canadian Social Insurance Number)`
##### **Example** : `A12B3256`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 21. Race/Ethnicity
##### **Data Field Column Name** : `race`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `Combined race and ethnicity of the individual (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Client doesn't know, R = Client refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### **Example** : `B`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 22. Secondary Race/Ethnicity
##### **Data Field Column Name** : `secondary_race`
##### **Data Field Type** : `char(1)-uppercase`
##### **Description** : `If the data system records race as primary and secondary values, use this field for the secondar value. (If race values are not designated as primary and secondary, or if more than two are recorded, they can all be given in the primary race field as a comma-separated list.) (W = White, B = Black or African American, A = Asian, I = American Indian or Alaskan Native, P = Native Hawaiian or Other Pacific Islander, H = Hispanic or Latino, O = Other, D = Client doesn't know, R = Client refused, N = Data not collected); if ethnicity is recorded in a separate field, do not use H code`
##### **Example** : `W`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 23. Ethnicity
##### **Data Field Column Name** : `ethnicity`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Ethnicity, if recorded separately (HISPANIC, NOT HISPANIC, CLIENT DOESN'T KNOW, CLIENT REFUSED, DATA NOT COLLECTED)`
##### **Example** : `HISPANIC`
##### **Required by Upload System** : `NO`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 24. Sex/Gender
##### **Data Field Column Name** : `sex`
##### **Data Field Type** : `char(2)-uppercase`
##### **Description** : `Sex or gender of the individual (F = Female, M = Male, MT = Transgender Female to Male, FT = Transgender Male to Female, O = Doesn't Identify as Male, Female, or Transgender, D = Client doesn't know, R = Client Refused,  N = Data not collected)`
##### **Example** : `F`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 25. Street Address
##### **Data Field Column Name** : `street_address`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Last permanent residential street address of the individual`
##### **Example** : `123 MAIN ST`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 26. City
##### **Data Field Column Name** : `city`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `City in which the individual resided at their last permanent address`
##### **Example** : `PLEASANTVILLE`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 27. State
##### **Data Field Column Name** : `state`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `State in which the individual resided at their last permanent address`
##### **Example** : `MD`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 28. Postal Code
##### **Data Field Column Name** : `postal_code`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Postal code of the individual's last permanent residential street address`
##### **Example** : `12334`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 29. County
##### **Data Field Column Name** : `county`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `County in which the individual resided at their last permanent address`
##### **Example** : `DOVE COUNTY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 30. Country
##### **Data Field Column Name** : `country`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Country in which the individual resided at their last permanent street address`
##### **Example** : `USA`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 31. Address Data Quality
##### **Data Field Column Name** : `address_data_quality`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Quality of the information recorded about the individual's last permanent address (FULL ADDRESS REPORTED, INCOMPLETE OR ESTIMATED ADDRESS REPORTED, FULL OR PARTIAL ZIP CODE REPORTED, CLIENT DOESN'T KNOW, CLIENT REFUSED, DATA NOT COLLECTED)`
##### **Example** : `FULL ADDRESS REPORTED`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 32. Veteran Status
##### **Data Field Column Name** : `veteran_status`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Whether the individual is a veteran (NO, YES, CLIENT DOESN'T KNOW, CLIENT REFUSED, DATA NOT COLLECTED`
##### **Example** : `NO`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 33. Disabling Condition
##### **Data Field Column Name** : `disabling_condition`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Whether the individual has a disabling condition that affects their ability to live independently (NO, YES, CLIENT DOESN'T KNOW, CLIENT REFUSED, DATA NOT COLLECTED`
##### **Example** : `NO`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 34. Project Start Date
##### **Data Field Column Name** : `project_start_date`
##### **Data Field Type** : `date`
##### **Description** : `Time the person enrolled in the program (YYYY-MM-DD)`
##### **Example** : `7/17/04`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 35. Project Exit Date
##### **Data Field Column Name** : `project_exit_date`
##### **Data Field Type** : `date`
##### **Description** : `Time the person's enrollment in the program ended (YYYY-MM-DD)`
##### **Example** : `10/19/06`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 36. Program Name
##### **Data Field Column Name** : `program_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the program or agency`
##### **Example** : `SAFE HAVEN SHELTER`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 37. Program Type
##### **Data Field Column Name** : `program_type`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Type of program (e.g., SUPPORTIVE HOUSING, EMERGENCY SHELTER)`
##### **Example** : `EMERGENCY SHELTER`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 38. Federal Program
##### **Data Field Column Name** : `federal_program`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Federal program funding source (e.g., RHSP, COC)`
##### **Example** : `RHSP`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 39. Destination
##### **Data Field Column Name** : `destination`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Individual's destination on leaving the program (DECEASED; EMERGENCY SHELTER, INCLUDING HOTEL OR MOTEL PAID FOR WITH EMERGENCY SHELTER VOUCHER; FOSTER CARE HOME OR FOSTER CARE GROUP HOME; HOSPITAL OR OTHER RESIDENTIAL NON-PSYCHIATRIC MEDICAL FACILITY; HOTEL OR MOTEL PAID FOR WITHOUT EMERGENCY SHELTER VOUCHER; JAIL, PRISON OR JUVENILE DETENTION FACILITY; LONG-TERM CARE FACILITY OR NURSING HOME; MOVED FROM ONE HOPWA FUNDED PROJECT TO HOPWA PH; MOVED FROM ONE HOPWA FUNDED PROJECT TO HOPWA TH; OWNED BY CLIENT, NO ONGOING HOUSING SUBSIDY; OWNED BY CLIENT, WITH ONGOING HOUSING SUBSIDY; PERMANENT HOUSING (OTHER THAN RRH) FOR FORMERLY HOMELESS PERSONS; PLACE NOT MEANT FOR HABITATION (E.G., A VEHICLE, AN ABANDONED BUILDING, BUS/TRAIN/SUBWAY STATION/AIRPORT OR ANYWHERE OUTSIDE); PSYCHIATRIC HOSPITAL OR OTHER PSYCHIATRIC FACILITY; RENTAL BY CLIENT, NO ONGOING HOUSING SUBSIDY; RENTAL BY CLIENT, WITH RRH OR EQUIVALENT SUBSIDY; RENTAL BY CLIENT, WITH VASH HOUSING SUBSIDY; RENTAL BY CLIENT, WITH GPD TIP HOUSING SUBSIDY; RENTAL BY CLIENT, WITH OTHER ONGOING HOUSING SUBSIDY; RESIDENTIAL PROJECT OR HALFWAY HOUSE WITH NO HOMELESS CRITERIA; SAFE HAVEN; STAYING OR LIVING WITH FAMILY, PERMANENT TENURE; STAYING OR LIVING WITH FAMILY, TEMPORARY TENURE (E.G. ROOM, APARTMENT OR HOUSE); STAYING OR LIVING WITH FRIENDS, PERMANENT TENURE; STAYING OR LIVING WITH FRIENDS, TEMPORARY TENURE (E.G. ROOM APARTMENT OR HOUSE); SUBSTANCE ABUSE TREATMENT FACILITY OR DETOX CENTER; TRANSITIONAL HOUSING FOR HOMELESS PERSONS (INCLUDING HOMELESS YOUTH); OTHER; NO EXIT INTERVIEW COMPLETED; CLIENT DOESN?T KNOW; CLIENT REFUSED; DATA NOT COLLECTED)`
##### **Example** : `RENTAL BY CLIENT, WITH OTHER ONGOING HOUSING SUBSIDY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 40. Household ID
##### **Data Field Column Name** : `household_id`
##### **Data Field Type** : `varchar`
##### **Description** : `Internal database ID for the individual's household`
##### **Example** : `243859`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 41. Relationship to Head of Household
##### **Data Field Column Name** : `household_relationship`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Individual's relationship to the head of the household Values: SELF; HEAD OF HOUSEHOLD?S CHILD; HEAD OF HOUSEHOLD?S SPOUSE OR PARTNER; HEAD OF HOUSEHOLD?S OTHER RELATION MEMBER (OTHER RELATION TO HEAD OF HOUSEHOLD); OTHER: NON-RELATION MEMBER`
##### **Example** : `HEAD OF HOUSEHOLD?S CHILD`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 42. Housing Move-in Date
##### **Data Field Column Name** : `move_in_date`
##### **Data Field Type** : `date`
##### **Description** : `When a household moves into permanent housing (YYYY-MM-DD)`
##### **Example** : `2/1/15`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 43. Living Situation: Type of Residence
##### **Data Field Column Name** : `living_situation_type`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `The type of residence the individual was staying in before entering the program. Values: PLACE NOT MEANT FOR HABITATION; EMERGENCY SHELTER, INCLUDING HOTEL OR MOTEL PAID FOR WITH EMERGENCY SHELTER VOUCHER; SAFE HAVEN; INTERIM HOUSING; FOSTER CARE HOME OR FOSTER CARE GROUP HOME; HOSPITAL OR OTHER RESIDENTIAL NON-PSYCHIATRIC MEDICAL FACILITY; JAIL, PRISON OR JUVENILE DETENTION FACILITY; LONG-TERM CARE FACILITY OR NURSING HOME; PSYCHIATRIC HOSPITAL OR OTHER PSYCHIATRIC FACILITY; SUBSTANCE ABUSE TREATMENT FACILITY OR DETOX CENTER; HOTEL OR MOTEL PAID FOR WITHOUT EMERGENCY SHELTER VOUCHER; OWNED BY CLIENT, NO ONGOING HOUSING SUBSIDY; OWNED BY CLIENT, WITH ONGOING HOUSING SUBSIDY; PERMANENT HOUSING (OTHER THAN RRH) FOR FORMERLY HOMELESS PERSONS; RENTAL BY CLIENT, NO ONGOING HOUSING SUBSIDY; RENTAL BY CLIENT, WITH VASH SUBSIDY; RENTAL BY CLIENT, WITH GPD TIP SUBSIDY; RENTAL BY CLIENT, WITH OTHER HOUSING SUBSIDY (INCLUDING RRH); RESIDENTIAL PROJECT OR HALFWAY HOUSE WITH NO HOMELESS CRITERIA; STAYING OR LIVING IN A FAMILY MEMBER?S ROOM, APARTMENT OR HOUSE; STAYING OR LIVING IN A FRIEND?S ROOM, APARTMENT OR HOUSE; TRANSITIONAL HOUSING FOR HOMELESS PERSONS (INCLUDING HOMELESS YOUTH); OTHER; CLIENT DOESN?T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `CLIENT DOESN'T KNOW`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 44. Living Situation: Length of Stay
##### **Data Field Column Name** : `living_situation_length`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `How long the individual stayed in their previous living situation. Values: ONE NIGHT OR LESS; TWO TO SIX NIGHTS; ONE WEEK OR MORE, BUT LESS THAN ONE MONTH; ONE MONTH OR MORE, BUT LESS THAN 90 DAYS; 90 DAYS OR MORE, BUT LESS THAN ONE YEAR; ONE YEAR OR LONGER; CLIENT DOESN?T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `90 DAYS OR MORE, BUT LESS THAN ONE YEAR`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 45. Living Situation: Date Homelessness Started
##### **Data Field Column Name** : `living_situation_start_date`
##### **Data Field Type** : `date`
##### **Description** : `Approximate date homelessness started for the individual (YYYY-MM-DD)`
##### **Example** : `12/1/14`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 46. Living Situation: Number of Times on Street
##### **Data Field Column Name** : `times_on_street`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Number of times the client has been on the streets, in ES, or SH in the past three years including date of program entry. Values: ONE TIME; TWO TIMES; THREE TIMES; FOUR OR MORE TIMES; CLIENT DOESN?T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `THREE TIMES`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 47. Living Situation: Number of Months Homeless
##### **Data Field Column Name** : `months_homeless`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Total number of months homeless on the street, in ES, or SH in the past three years. Values: ONE MONTH (THIS TIME IS THE FIRST MONTH); 2; 3; 4; 5; 6; 7; 8; 9; 10; 11; 12; MORE THAN 12 MONTHS; CLIENT DOESN?T KNOW; CLIENT REFUSED; DATA NOT COLLECTED`
##### **Example** : `MORE THAN 12 MONTHS`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 48. Client Location Start Date
##### **Data Field Column Name** : `client_location_start_date`
##### **Data Field Type** : `date`
##### **Description** : `Date client started a stay at location (YYYY-MM-DD)`
##### **Example** : `7/17/04`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `NO`


### 49. Client Location End Date
##### **Data Field Column Name** : `client_location_end_date`
##### **Data Field Type** : `date`
##### **Description** : `Date client ended a stay at location (YYYY-MM-DD)`
##### **Example** : `7/18/04`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 50. Client Location
##### **Data Field Column Name** : `client_location`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `HUD assigned Continuum of Care code for the client?s location`
##### **Example** : ``
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 51. Source
##### **Data Field Column Name** : `source_name`
##### **Data Field Type** : `text-uppercase`
##### **Description** : `Name of the data source, such as the office or service provider uploading the data`
##### **Example** : `HOMELESS ALLIANCE OF DOVE COUNTY`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `YES`
##### **Nullable** : `YES`


### 52. Date Created
##### **Data Field Column Name** : `created_date`
##### **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### **Description** : `Date the entry was created in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2004-07-17T01:23:45+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`


### 53. Date Updated
##### **Data Field Column Name** : `updated_date`
##### **Data Field Type** : `timestamp or timestamp with timezone (if available)`
##### **Description** : `Date the entry was last updated in the database (typically an internal database timestamp, (YYYY-MM-DDTHH:MM:SS+TZ))`
##### **Example** : `2006-10-19T13:45:06+05`
##### **Required by Upload System** : `YES`
##### **Required for Good Match** : `NO`
##### **Nullable** : `YES`