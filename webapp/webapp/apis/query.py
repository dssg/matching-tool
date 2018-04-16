import logging
import pandas as pd
from webapp import db, app
from webapp.utils import generate_matched_table_name, table_exists
from collections import OrderedDict
from webapp.logger import logger
import numpy as np


def get_histogram_bar_chart_data(data, distribution_function, shared_ids, data_name):
    intersection_data = data[data.matched_id.isin(shared_ids)]
    distribution, groups = distribution_function(data)
    distribution_intersection, _ = distribution_function(intersection_data, groups)
    bins = []
    logger.info(data_name)
    #logger.info(distribution)
    logger.info(distribution_intersection)
    logger.info(len(data.matched_id.unique()))
    for bin_index in range(len(distribution)):
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
        except:
            all_status = {
                "x": "Jail & Homeless",
                "y": 0
            }
        bins.append((of_status, all_status))
    return [bins, list(distribution.index)]


def window(iterable, size=2):
    i = iter(iterable)
    win = []
    for e in range(0, size):
        win.append(next(i))
    yield win
    for e in i:
        win = win[1:] + [e]
        yield win


def get_contact_dist(data, bins=None):
    data = data.groupby('matched_id').matched_id.count().as_matrix()
    data = data.astype(int)
    one_contact = list(data).count(1)
    rest = np.delete(data, np.argwhere(data==1))
    if one_contact == len(data):
        df_hist = pd.DataFrame({'contacts': [one_contact]}, index=['1 contact'])
        logger.info("all ones!")
        return df_hist, 1

    if bins is not None:
        num, groups = np.histogram(rest, bins)
    else:
        num, groups = np.histogram(rest, 'auto')
        if len(groups) > 4:
            bins = 4
            num, groups = np.histogram(rest, bins)
    hist = [one_contact] + list(num)
    index = [pd.Interval(1, 2, 'left')] + [pd.Interval(int(b[0]), int(b[1])+1, 'left') for b in list(window(list(groups), 2))]
    df_hist = pd.DataFrame({'contacts': hist}, index=contacts_interval_to_text(index))
    logger.info(num)
    logger.info(groups)
    logger.info(index)
    logger.info(df_hist)
    return df_hist, groups


def get_days_distribution(data, groups=None):
    dist = pd.cut(
            data.groupby('matched_id').days.sum(),
            [0, 1, 2, 10, 90, 1000],
            right=False
        ).value_counts(sort=False)
    dist = pd.DataFrame({'days': dist.as_matrix()}, index=days_interval_to_text(dist.index))
    return dist, []


def contacts_interval_to_text(interval_list):
    result = ['1 contact']
    for c, i in enumerate(interval_list[1:], 1):
        if c == 1:
            if i.right == 3:
                result.append(f"2 contacts")
            else:
                result.append(f"{i.left}-{i.right - 1 if i.open_right else i.right} contacts")
        else:
            if i.left + 1 == i.right - 1:
                result.append(f"{i.left + 1} contacts")
            else:
                result.append(f"{i.left + 1}-{i.right - 1 if i.open_right else i.right} contacts")
    return result


def days_interval_to_text(interval_list):
    result = ['< 1 day', '1 day']
    for i in interval_list[2:-1]:
        result.append(f"{i.left}-{i.right - 1 if i.open_right else i.right} days")

    result = result + ['90+ days']
    return result


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
    matched_hmis_table = generate_matched_table_name(jurisdiction, 'hmis_service_stays')
    matched_bookings_table = generate_matched_table_name(jurisdiction, 'jail_bookings')
    hmis_exists = table_exists(matched_hmis_table, db.engine)
    bookings_exists = table_exists(matched_bookings_table, db.engine)
    if not hmis_exists:
        raise ValueError('HMIS matched table {} does not exist. Please try again later.'.format(matched_hmis_table))
    if not bookings_exists:
        raise ValueError('Bookings matched table {} does not exist. Please try again later.'.format(matched_bookings_table))
    columns = [
        ("matched_id", 'matched_id'),
        ("coalesce(hmis_summary.first_name, jail_summary.first_name)", 'first_name'),
        ("coalesce(hmis_summary.last_name, jail_summary.last_name)", 'last_name'),
        ("hmis_summary.hmis_id", 'hmis_id'),
        ("hmis_summary.hmis_contact", 'hmis_contact'),
        ("hmis_summary.last_hmis_contact", 'last_hmis_contact'),
        ("hmis_summary.cumu_hmis_days", 'cumu_hmis_days'),
        ("jail_summary.jail_id", 'jail_id'),
        ("jail_summary.jail_contact", 'jail_contact'),
        ("jail_summary.last_jail_contact", 'last_jail_contact'),
        ("jail_summary.cumu_jail_days", 'cumu_jail_days'),
        ("coalesce(hmis_summary.hmis_contact, 0) + coalesce(jail_summary.jail_contact, 0)", 'total_contact'),
    ]
    if not any(order_column for expression, alias in columns):
        raise ValueError('Given order column expression does not match any alias in query. Exiting to avoid SQL injection attacks')
    base_query = """WITH hmis_summary AS (
        SELECT
            matched_id,
            string_agg(distinct internal_person_id::text, ',') as hmis_id,
            sum(
                case when client_location_end_date is not null 
                    then date_part('day', client_location_end_date::timestamp - client_location_start_date::timestamp) \
                    else date_part('day', updated_ts::timestamp - client_location_start_date::timestamp) 
                end
            )::int as cumu_hmis_days,
            count(*) AS hmis_contact,
            to_char(max(client_location_start_date::timestamp), 'YYYY-MM-DD') as last_hmis_contact,
            max(first_name) as first_name,
            max(last_name) as last_name
        FROM (
            SELECT
               *
            FROM {hmis_table}
            WHERE
                not (client_location_start_date < %(start_date)s AND client_location_end_date < %(start_date)s) and
                not (client_location_start_date > %(end_date)s AND client_location_end_date > %(end_date)s)
        ) AS hmis
        GROUP BY matched_id
    ), jail_summary AS (
        SELECT
            matched_id,
            string_agg(distinct coalesce(internal_person_id, inmate_number)::text, ',') as jail_id,
            sum(
                case when jail_exit_date is not null 
                    then date_part('day', jail_exit_date::timestamp - jail_entry_date::timestamp) \
                    else date_part('day', updated_ts::timestamp - jail_entry_date::timestamp) 
                end
            )::int as cumu_jail_days,
            count(*) AS jail_contact,
            to_char(max(jail_entry_date::timestamp), 'YYYY-MM-DD') as last_jail_contact,
            max(first_name) as first_name,
            max(last_name) as last_name
        FROM (
            SELECT
               *
            FROM {booking_table}
            WHERE
                not (jail_entry_date < %(start_date)s AND jail_exit_date < %(start_date)s) and
                not (jail_entry_date > %(end_date)s AND jail_exit_date > %(end_date)s)
        ) AS jail
        GROUP BY matched_id
    )
    SELECT
    {columns}
    FROM hmis_summary
    FULL OUTER JOIN jail_summary USING(matched_id)
    """.format(
        hmis_table=matched_hmis_table,
        booking_table=matched_bookings_table,
        columns=",\n".join("{} as {}".format(expression, alias) for expression, alias in columns),
    )


    logging.info('Querying table records')
    if order not in {'asc', 'desc'}:
        raise ValueError('Given order direction is not valid. Exiting to avoid SQL injection attacks')
    if not isinstance(limit, int) and not limit.isdigit() and limit != 'ALL':
        raise ValueError('Given limit is not valid. Existing to avoid SQL injection attacks')
    filter_by_status = {
        'Jail': 'jail_summary.matched_id is not null',
        'HMIS': 'hmis_summary.matched_id is not null',
        'Intersection': 'hmis_summary.matched_id = jail_summary.matched_id'
    }
    status_filter = filter_by_status.get(set_status, 'true')
    rows_to_show = [dict(row) for row in db.engine.execute("""
        {}
        where {}
        order by {} {}
        limit {} offset %(offset)s""".format(
            base_query,
            status_filter,
            order_column,
            order,
            limit
        ),
        start_date=start_time,
        end_date=end_time,
        offset=offset,
    )]
    query = """
    SELECT
    *,
    DATE_PART('day', {exit}::timestamp - {start}::timestamp) as days
    FROM {table_name}
    WHERE
        not ({start} < %(start_time)s AND {exit} < %(start_time)s) and
        not ({start} > %(end_time)s AND {exit} > %(end_time)s)
    """
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
    logging.info('Done querying table records')
    logging.info('Querying venn diagram stats')
    venn_diagram_stats = next(db.engine.execute('''select
        count(distinct(hmis.matched_id)) as hmis_size,
        count(distinct(bookings.matched_id)) as bookings_size,
        count(distinct(case when hmis.matched_id = bookings.matched_id then hmis.matched_id else null end)) as shared_size,
        count(distinct(matched_id))
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
    filtered_data = retrieve_bar_data(matched_hmis_table, matched_bookings_table, start_time, end_time)
    logging.info('Done retrieving bar data from database')
    filtered_data['tableData'] = rows_to_show
    return {
        "vennDiagramData": venn_diagram_data,
        "totalTableRows": counts_by_status.get(set_status, venn_diagram_stats[3]),
        "filteredData": filtered_data
    }


def retrieve_bar_data(matched_hmis_table, matched_bookings_table, start_time, end_time):
    query = """
    SELECT
    *,
    DATE_PART('day', {exit}::timestamp - {start}::timestamp) as days
    FROM {table_name}
    WHERE
        not ({start} < %(start_time)s AND {exit} < %(start_time)s) and
        not ({start} > %(end_time)s AND {exit} > %(end_time)s)
    """
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
        logger.warning("No matched between two services")

    # Handle the case that empty query results in ZeroDivisionError
    bar_data = {
        "jailDurationBarData": get_histogram_bar_chart_data(filtered_bookings, get_days_distribution, shared_ids, 'Jail'),
        "homelessDurationBarData": get_histogram_bar_chart_data(filtered_hmis, get_days_distribution, shared_ids, 'Homeless'),
        "jailContactBarData": get_histogram_bar_chart_data(filtered_bookings, get_contact_dist, shared_ids, 'Jail'),
        "homelessContactBarData": get_histogram_bar_chart_data(filtered_hmis, get_contact_dist, shared_ids, 'Homeless'),
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
