import logging
import pandas as pd
from webapp import db, app
from webapp.utils import generate_matched_table_name, table_exists
from collections import OrderedDict

logging.basicConfig(
    format='%(asctime)s %(process)d %(levelname)s: %(message)s',
    level=logging.INFO
)

def get_histogram_bar_chart_data(data, distribution_function, shared_ids, data_name):
    intersection_data = data[data.matched_id.isin(shared_ids)]
    distribution = distribution_function(data)
    distribution_intersection = distribution_function(intersection_data)

    bins = []
    for bin_index in range(0, 5):
        try:
            of_status = {
                "x": data_name,
                "y": int(distribution.iloc[bin_index])/len(data.matched_id.unique())*100
            }
        except ZeroDivisionError:
            of_status = {
                "x": data_name,
                "y": 0
            }
        try:
            all_status = {
                "x": "Jail & Homeless",
                "y": int(distribution_intersection.iloc[bin_index])/len(intersection_data.matched_id.unique())*100
            }
        except ZeroDivisionError:
            all_status = {
                "x": "Jail & Homeless",
                "y": 0
            }
        bins.append((of_status, all_status))
    return bins


def get_days_distribution(data):
    return pd.cut(
        data.groupby('matched_id').days.sum(),
        [0, 1, 2, 10, 90, 1000],
        right=False
    ).value_counts(sort=False)

def get_contacts_distribution(data):
    contact = data.groupby('matched_id').matched_id.count()
    return pd.cut(
        contact,
        bins=[1, 2, 10, 100, 500, 1000],
        right=False
    ).value_counts(sort=False)

def get_records_by_time(
    start_time,
    end_time,
    jurisdiction,
    limit,
    offset,
    order_column,
    order,
    set_status
):
    query = """
    SELECT
    *,
    DATE_PART('day', {exit}::timestamp - {start}::timestamp) as days
    FROM {table_name}
    WHERE
        not ({start} < %(start_time)s AND {exit} < %(start_time)s) and
        not ({start} > %(end_time)s AND {exit} > %(end_time)s)
    """
    matched_hmis_table = generate_matched_table_name(jurisdiction, 'hmis_service_stays')
    matched_bookings_table = generate_matched_table_name(jurisdiction, 'jail_bookings')
    hmis_exists = table_exists(matched_hmis_table, db.engine)
    bookings_exists = table_exists(matched_bookings_table, db.engine)
    if not hmis_exists:
        raise ValueError('HMIS matched table {} does not exist. Please try again later.'.format(matched_hmis_table))
    if not bookings_exists:
        raise ValueError('Bookings matched table {} does not exist. Please try again later.'.format(matched_bookings_table))

    hmis_query = query.format(
        table_name=matched_hmis_table,
        start="client_location_start_date",
        exit="client_location_end_date"
    )
    bookings_query = query.format(
        table_name=matched_bookings_table,
        start="jail_entry_date",
        exit="jail_exit_date"
    )
    logging.info('Querying table records')
    columns = [
        ("md5(matched_id)", 'matched_id'),
        ("string_agg(coalesce(bookings.internal_person_id, bookings.inmate_number)::text, ',')", 'booking_id'),
        ("string_agg(hmis.internal_person_id::text, ',')", 'hmis_id'),
        ("coalesce(max(bookings.first_name), max(hmis.first_name))", 'first_name'),
        ("coalesce(max(bookings.last_name), max(hmis.last_name))", 'last_name'),
        ("to_char(max(jail_entry_date::timestamp), 'YYYY-MM-DD')", 'last_jail_contact'),
        ("to_char(max(client_location_start_date::timestamp), 'YYYY-MM-DD')", 'last_hmis_contact'),
        ("count(bookings.internal_event_id)",  'jail_contact'),
        ("count(hmis.internal_event_id)", 'hmis_contact'),
        ("coalesce(sum(date_part('day', client_location_end_date::timestamp - client_location_start_date::timestamp)), 0)::int", 'cumu_hmis_days'),
        ("coalesce(sum(date_part('day', jail_exit_date::timestamp - jail_entry_date::timestamp)), 0)::int", 'cumu_jail_days'),
        ("count(bookings.internal_event_id) + count(hmis.internal_event_id)", 'total_contact'),
    ]
    if not any(order_column for expression, alias in columns):
        raise ValueError('Given order column expression does not match any alias in query. Exiting to avoid SQL injection attacks')
    if order not in {'asc', 'desc'}:
        raise ValueError('Given order direction is not valid. Exiting to avoid SQL injection attacks')
    if not isinstance(limit, int) and not limit.isdigit() and limit != 'ALL':
        raise ValueError('Given limit is not valid. Existing to avoid SQL injection attacks')
    filter_by_status = {
        'Jail': 'bookings.matched_id is not null',
        'HMIS': 'hmis.matched_id is not null',
        'Intersection': 'hmis.matched_id = bookings.hashed_id'
    }
    status_filter = filter_by_status.get(set_status, 'true')
    rows_to_show = [dict(row) for row in db.engine.execute("""
        select
        {}
        from
        ({}) hmis
        full outer join ({}) bookings using (matched_id)
        where {}
        group by matched_id
        order by {} {}
        limit {} offset %(offset)s""".format(
            ",\n".join("{} as {}".format(expression, alias) for expression, alias in columns),
            hmis_query,
            bookings_query,
            status_filter,
            order_column,
            order,
            limit
        ),
        start_time=start_time,
        end_time=end_time,
        offset=offset,
    )]
    logging.info('Done querying table records')
    logging.info('Querying venn diagram stats')
    venn_diagram_stats = next(db.engine.execute('''select
        count(distinct(hmis.matched_id)) as hmis_size,
        count(distinct(bookings.matched_id)) as bookings_size,
        count(distinct(case when hmis.matched_id = bookings.hashed_id then hmis.hashed_id else null end)) as shared_size,
        count(*)
        from ({}) hmis
        full outer join ({}) bookings using (matched_id)
    '''.format(hmis_query, bookings_query),
                                start_time=start_time,
                                end_time=end_time))
    counts_by_status = {
        'HMIS': venn_diagram_stats[0],
        'Jail': venn_diagram_stats[1],
        'Intersection': venn_diagram_stats[2]
    }

    logging.info('Done querying venn diagram stats')

    venn_diagram_data = [
        {
            "sets": [
                "Jail"
            ],
            "size": venn_diagram_stats[1]
        },
        {
            "sets": [
                "Homeless"
            ],
            "size": venn_diagram_stats[0]
        },
        {
            "sets": [
                "Jail",
                "Homeless"
            ],
            "size": venn_diagram_stats[2]
        }
    ]
    logging.info('Retrieving bar data from database')
    filtered_data = retrieve_bar_data(query, matched_hmis_table, matched_bookings_table, start_time, end_time)
    logging.info('Done retrieving bar data from database')
    filtered_data['tableData'] = rows_to_show
    return {
        "vennDiagramData": venn_diagram_data,
        "totalTableRows": counts_by_status.get(set_status, venn_diagram_stats[3]),
        "filteredData": filtered_data
    }

def retrieve_bar_data(query, matched_hmis_table, matched_bookings_table, start_time, end_time):
    filtered_hmis = pd.read_sql(
        query.format(
            table_name=matched_hmis_table,
            start="client_location_start_date",
            exit="client_location_end_date"),
        con=db.engine,
        params={
            "start_time": start_time,
            "end_time": end_time
    })


    filtered_bookings = pd.read_sql(
        query.format(
            table_name=matched_bookings_table,
            start="jail_entry_date",
            exit="jail_exit_date"),
        con=db.engine,
        params={
            "start_time": start_time,
            "end_time": end_time
    })
    shared_ids = filtered_hmis[filtered_hmis.matched_id.isin(filtered_bookings.matched_id)].matched_id.unique()

    if len(shared_ids) == 0:
        app.logger.warning("No matched between two services")

    # Handle the case that empty query results in ZeroDivisionError
    bar_data = {
        "jailDurationBarData": get_histogram_bar_chart_data(filtered_bookings, get_days_distribution, shared_ids, 'Jail'),
        "homelessDurationBarData": get_histogram_bar_chart_data(filtered_hmis, get_days_distribution, shared_ids, 'Homeless'),
        "jailContactBarData": get_histogram_bar_chart_data(filtered_bookings, get_contacts_distribution, shared_ids, 'Jail'),
        "homelessContactBarData": get_histogram_bar_chart_data(filtered_hmis, get_contacts_distribution, shared_ids, 'Homeless'),
    }

    return bar_data


def get_task_uplaod_id(n):
    query = """
    SELECT *
    FROM (
        SELECT row_number() over (ORDER By upload_timestamp DESC) as rownumber, *
        FROM upload_log
    ) as foo
    where rownumber = %(n)s
    """
    df = pd.read_sql(
        query,
        con=db.engine,
        params={"n": n}
    )
    return df


def get_history():
    query = """
    SELECT
        upload_log.id as upload_id,
        upload_log.jurisdiction_slug,
        upload_log.event_type_slug,
        upload_log.user_id,
        upload_log.given_filename,
        upload_log.upload_timestamp,
        upload_log.num_rows,
        upload_log.file_size,
        upload_log.file_hash,
        upload_log.s3_upload_path,
        match_log.id as match_id,
        match_log.match_start_timestamp,
        match_log.match_complete_timestamp,
        to_char(match_log.runtime, 'HH24:MI:SS') as runtime
    FROM match_log
    LEFT JOIN upload_log ON upload_log.id = match_log.upload_id
    ORDER BY match_complete_timestamp ASC
    """
    df = pd.read_sql(
        query,
        con=db.engine
    )
    return df
