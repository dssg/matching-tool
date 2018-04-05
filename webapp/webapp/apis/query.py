import pandas as pd
from webapp import db, app
from collections import OrderedDict

def get_table_data(filtered_bookings, filtered_hmis, unique_ids):
    table_data = []
    for unique_id in unique_ids:
        if unique_id in list(filtered_bookings.matched_id):
            last_jail_contact = filtered_bookings[filtered_bookings.matched_id == unique_id].jail_entry_date.sort_values(ascending=False).iloc[0].strftime('%Y-%m-%d')
            cumu_jail_days = filtered_bookings[filtered_bookings.matched_id == unique_id].days.sum()
            first_name = filtered_bookings[filtered_bookings.matched_id == unique_id].first_name.unique()[0]
            last_name = filtered_bookings[filtered_bookings.matched_id == unique_id].last_name.unique()[0]
        else:
            last_jail_contact = None
            cumu_jail_days = 0

        if unique_id in list(filtered_hmis.matched_id):
            last_hmis_contact = filtered_hmis[filtered_hmis.matched_id == unique_id].client_location_start_date.sort_values(ascending=False).iloc[0].strftime('%Y-%m-%d')
            cumu_homeless_days = filtered_hmis[filtered_hmis.matched_id == unique_id].days.sum()
            first_name = filtered_hmis[filtered_hmis.matched_id == unique_id].first_name.unique()[0]
            last_name = filtered_hmis[filtered_hmis.matched_id == unique_id].last_name.unique()[0]
        else:
            last_hmis_contact = None
            cumu_homeless_days = 0

        jail_contact = len(filtered_bookings[filtered_bookings.matched_id == unique_id])
        homeless_contact = len(filtered_hmis[filtered_hmis.matched_id == unique_id])

        person_data = OrderedDict({
            "matched_id": int(unique_id),
            "booking_id": ','.join(map(str,list(filtered_bookings[filtered_bookings.matched_id == unique_id].internal_event_id))),
            "hmis_id": ','.join(map(str,list(filtered_hmis[filtered_hmis.matched_id == unique_id].internal_person_id))),
            "first_name": first_name,
            "last_name": last_name,
            "last_jail_contact": last_jail_contact,
            "last_hmis_contact": last_hmis_contact,
            "jail_contact": int(jail_contact),
            "hmis_contact": int(homeless_contact),
            "total_contact": int(jail_contact + homeless_contact),
            "cumu_jail_days": int(cumu_jail_days),
            "cumu_hmis_days": int(cumu_homeless_days)
        })
        table_data.append(person_data)
    return table_data


def get_duration_bar_chart_data(data, shared_ids, data_name):
    intersection_data = data[data.matched_id.isin(shared_ids)]
    days_distribution = get_days_distribution(data)
    days_distribution_intersection = get_days_distribution(intersection_data)

    return [
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[0])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[0])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[1])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[1])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[2])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[2])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[3])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[3])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[4])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[4])/len(intersection_data.matched_id.unique())*100
            }
        ]
    ]


def get_contact_bar_chart_data(data, shared_ids, data_name):
    intersection_data = data[data.matched_id.isin(shared_ids)]
    contacts_distribution = get_contacts_distribution(data)
    contacts_distribution_intersection = get_contacts_distribution(intersection_data)

    return [
        [
            {
                "x": data_name,
                "y": int(contacts_distribution.iloc[0])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(contacts_distribution_intersection.iloc[0])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(contacts_distribution.iloc[1])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(contacts_distribution_intersection.iloc[1])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(contacts_distribution.iloc[2])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(contacts_distribution_intersection.iloc[2])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(contacts_distribution.iloc[3])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(contacts_distribution_intersection.iloc[3])/len(intersection_data.matched_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(contacts_distribution.iloc[4])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(contacts_distribution_intersection.iloc[4])/len(intersection_data.matched_id.unique())*100
            }
        ]
    ]


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

def get_records_by_time(start_time, end_time):
    query = """
    SELECT *,
    DATE_PART('day', {exit}::timestamp - {start}::timestamp) as days
    FROM matched."{table_name}"
    EXCEPT
    SELECT *,
    DATE_PART('day', {exit}::timestamp - {start}::timestamp) as days
    FROM matched."{table_name}"
    WHERE
        ({start} < %(start_time)s AND {exit} < %(start_time)s) OR
        ({start} > %(end_time)s AND {exit} > %(end_time)s)
    """

    filtered_hmis = pd.read_sql(
        query.format(
            table_name="hmis_service_stays",
            start="client_location_start_date",
            exit="client_location_end_date"),
        con=db.engine,
        params={
            "start_time": start_time,
            "end_time": end_time
    })


    filtered_bookings = pd.read_sql(
        query.format(
            table_name="jail_bookings",
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

    table_data = get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.matched_id.unique())+list(filtered_hmis.matched_id.unique()))))


    filters = {
        "controlledDate": end_time,
        "startDate": start_time,
        "endDate": end_time,
        "service": "jail_hmis",
        "flag_homeless_in_jail": True,
        "flag_veteran": False,
        "flag_disability": False,
        "flag_mental_illness": False,
        "setStatus": "All"
    }

    venn_diagram_data = [
        {
            "sets": [
                "Jail"
            ],
            "size": len(filtered_bookings.matched_id.unique())
        },
        {
            "sets": [
                "Homeless"
            ],
            "size": len(filtered_hmis.matched_id.unique())
        },
        {
            "sets": [
                "Jail",
                "Homeless"
            ],
            "size": len(shared_ids)
        }
    ]
    # Handle the case that empty query results in ZeroDivisionError
    try:
        filtered_data = {
            "jailDurationBarData": get_duration_bar_chart_data(filtered_bookings, shared_ids, 'Jail'),
            "homelessDurationBarData": get_duration_bar_chart_data(filtered_hmis, shared_ids, 'Homeless'),
            "jailContactBarData": get_contact_bar_chart_data(filtered_bookings, shared_ids, 'Jail'),
            "homelessContactBarData": get_contact_bar_chart_data(filtered_hmis, shared_ids, 'Homeless'),
            "tableData": get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.matched_id.unique())+list(filtered_hmis.matched_id.unique()))))
        }
    except:
        filtered_data = {
            "jailDurationBarData": None,
            "homelessDurationBarData": None,
            "jailContactBarData": None,
            "homelessContactBarData": None,
            "tableData": get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.matched_id.unique())+list(filtered_hmis.matched_id.unique()))))
        }
    return {
        "filters": filters,
        "vennDiagramData": venn_diagram_data,
        "filteredData": filtered_data
    }


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
