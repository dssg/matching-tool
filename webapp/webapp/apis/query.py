import pandas as pd
from webapp import db


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
        homeless_contact = len(filtered_bookings[filtered_bookings.matched_id == unique_id])

        person_data = {
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
        }
        table_data.append(person_data)
    return table_data


def get_bar_chart_data(data, shared_ids, data_name):
    intersection_data = data[data.matched_id.isin(shared_ids)]
    days_distribution = get_days_distribution(data)
    days_distribution_intersection = get_days_distribution(intersection_data)

    return [
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[4])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[4])/len(intersection_data.matched_id.unique())*100
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
                "y": int(days_distribution.iloc[0])/len(data.matched_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[0])/len(intersection_data.matched_id.unique())*100
            }
        ]
    ]

def get_days_distribution(data):
    return pd.cut(
        data.groupby('matched_id').days.sum(),
        [0, 1, 2, 10, 90, 1000],
        right=False
    ).value_counts()

def get_records_by_time(start_time, end_time, duration=1):
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

    table_data = get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.matched_id.unique())+list(filtered_hmis.matched_id.unique()))))

    filters = {
        "controlledDate": end_time,
        "duration": duration,
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
            "jailBarData": get_bar_chart_data(filtered_bookings, shared_ids, 'Jail'),
            "homelessBarData": get_bar_chart_data(filtered_hmis, shared_ids, 'Homeless'),
            "tableData": get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.matched_id.unique())+list(filtered_hmis.matched_id.unique()))))
        }
    except:
        filtered_data = {
            "jailBarData": None,
            "homelessBarData": None,
            "tableData": None
        }
    return {
        "filters": filters,
        "vennDiagramData": venn_diagram_data,
        "filteredData": filtered_data
    }
