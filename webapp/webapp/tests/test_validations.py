from webapp import tasks
from unittest import TestCase

# HMIS FILES
HMIS_GOOD = 'sample_data/uploader_input/hmis_service_stays/good.csv'
HMIS_PARTIAL_DOB_XES = 'sample_data/uploader_input/hmis_service_stays/partial-dob-xes.csv'
HMIS_PARTIAL_DOB_BLANKS = 'sample_data/uploader_input/hmis_service_stays/partial-dob-blanks.csv'
HMIS_NAME_DATA_QUALITY = 'sample_data/uploader_input/hmis_service_stays/name-data-quality.csv'
HMIS_DMV_STATE = 'sample_data/uploader_input/hmis_service_stays/dmv-state.csv'
HMIS_PROJECT_DATES = 'sample_data/uploader_input/hmis_service_stays/project-dates.csv'
HMIS_COMMA_DELIMITER = 'sample_data/uploader_input/hmis_service_stays/comma-delimited.csv'
HMIS_BAD_DELIMITER = 'sample_data/uploader_input/hmis_service_stays/bad-delimiter.csv'

# BOOKINGS FILES
BOOKINGS_FILE_BOOKING_NUM = 'sample_data/uploader_input/jail_bookings/no-event-id.csv'
BOOKINGS_FILE_NO_IDS = 'sample_data/uploader_input/jail_bookings/no-ids.csv'
BOOKINGS_FILE_ONLY_NUMS = 'sample_data/uploader_input/jail_bookings/only-nums.csv'
BOOKINGS_FILE_NO_PERSON_ID = 'sample_data/uploader_input/jail_bookings/no-person-id.csv'
BOOKINGS_FILE_SSN = 'sample_data/uploader_input/jail_bookings/ssn.csv'
BOOKINGS_FILE_HASHED_SSN = 'sample_data/uploader_input/jail_bookings/hashed-ssn.csv'
BOOKINGS_FILE_BAD_HAIR_COLOR = 'sample_data/uploader_input/jail_bookings/bad-hair-color.csv'
BOOKINGS_FILE_MULTI_RACE = 'sample_data/uploader_input/jail_bookings/multi-race.csv'

assert_raises = TestCase().assertRaises


def fill_and_validate(event_type, filename):
    return tasks.validate_file(event_type, tasks.add_missing_fields(event_type, filename))


def assert_report_errors(
    report,
    expected_error_count,
    error_count_invalid_msg='This file should be interpreted as correct',
    expected_code='',
    expected_substring=''
):
    assert report['error-count'] == expected_error_count,\
        error_count_invalid_msg + ", but instead found following errors: \n\n" +\
        '\n'.join([e['message'] for e in report['tables'][0]['errors']])
    for error in report['tables'][0]['errors']:
        assert error['code'] == expected_code
        assert expected_substring in error['message']


def test_booking_number_is_fine():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_BOOKING_NUM)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_some_booking_id_is_needed():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_NO_IDS)
    assert_report_errors(
        report=report,
        expected_error_count=8,
        error_count_invalid_msg='Either internal event id or booking number is needed',
        expected_code='one-of-group-constraint',
        expected_substring="booking_number"
    )


def test_booking_number_and_inmate_number():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_ONLY_NUMS)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_no_person_id():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_NO_PERSON_ID)
    assert_report_errors(
        report=report,
        expected_error_count=8,
        error_count_invalid_msg='Either internal person id or inmate number should be needed',
        expected_code='one-of-group-constraint',
        expected_substring="'inmate_number', 'internal_person_id'"
    )


def test_has_full_ssn():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_SSN)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_has_ssn_hash():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_HASHED_SSN)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_hair_color():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_BAD_HAIR_COLOR)
    assert_report_errors(
        report=report,
        expected_error_count=1,
        error_count_invalid_msg='All but one row should have hair color check out',
        expected_code='enum-maybe-list-constraint',
        expected_substring="BROWN"
    )

def test_multi_race():
    report = fill_and_validate('jail_bookings', BOOKINGS_FILE_MULTI_RACE)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


# HMIS TESTS
def test_hmis_good_file():
    report = fill_and_validate('hmis_service_stays', HMIS_GOOD)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_hmis_partial_dob_with_xs():
    # should pass, we expect partial dates of birth to be filled in with Xs
    report = fill_and_validate('hmis_service_stays', HMIS_PARTIAL_DOB_XES)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_hmis_partial_dob_with_blanks():
    # should fail, we expect partial dates of birth to be filled in with Xs
    report = fill_and_validate('hmis_service_stays', HMIS_PARTIAL_DOB_BLANKS)
    assert_report_errors(
        report=report,
        expected_error_count=2,
        error_count_invalid_msg='Two rows should have invalid DOBs',
        expected_code='partial-dob',
        expected_substring="is not in format YYYY-MM-DD"
    )


def test_hmis_name_data_quality():
    # all are fine, including blanks, except CLIENT DOES NOT KNOW in two fields
    report = fill_and_validate('hmis_service_stays', HMIS_NAME_DATA_QUALITY)
    assert_report_errors(
        report=report,
        expected_error_count=2,
        error_count_invalid_msg='Two rows should have bad name-data-qualities',
        expected_code='enumerable-constraint',
        expected_substring="CLIENT DOES NOT KNOW"
    )


def test_dmv_state():
    report = fill_and_validate('hmis_service_stays', HMIS_DMV_STATE)
    assert_report_errors(
        report=report,
        expected_error_count=2,
        error_count_invalid_msg='Two rows should have bad name-data-qualities',
        expected_code='maximum-length-constraint',
        expected_substring="2"
    )


def test_project_dates():
    report = fill_and_validate('hmis_service_stays', HMIS_PROJECT_DATES)
    assert_report_errors(
        report=report,
        expected_error_count=2,
        error_count_invalid_msg='Blank dates should be fine but not misformatted ones',
        expected_code='type-or-format-error',
        expected_substring="10:10:10"
    )


def test_comma_delimiter():
    report = fill_and_validate('hmis_service_stays', HMIS_COMMA_DELIMITER)
    assert_report_errors(
        report=report,
        expected_error_count=0,
    )


def test_tab_delimiter():
    with assert_raises(ValueError):
        fill_and_validate('hmis_service_stays', HMIS_BAD_DELIMITER)
