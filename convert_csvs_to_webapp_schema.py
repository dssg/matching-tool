import pandas as pd
import json
import pdb


def get_days_distribution(data):
    # pdb.set_trace()
    return pd.cut(
        data.groupby('match_id').days.sum(),
        [0, 1, 2, 10, 90, 1000],
        right=False
    ).value_counts()


def get_bar_chart_data(data, shared_ids, data_name):
    print(data_name)
    intersection_data = data[data.match_id.isin(shared_ids)]
    days_distribution = get_days_distribution(data)
    days_distribution_intersection = get_days_distribution(intersection_data)

    return [
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[4])/len(data.match_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[4])/len(intersection_data.match_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[3])/len(data.match_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[3])/len(intersection_data.match_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[2])/len(data.match_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[2])/len(intersection_data.match_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[1])/len(data.match_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[1])/len(intersection_data.match_id.unique())*100
            }
        ],
        [
            {
                "x": data_name,
                "y": int(days_distribution.iloc[0])/len(data.match_id.unique())*100
            },
            {
                "x": "Jail & Homeless",
                "y": int(days_distribution_intersection.iloc[0])/len(intersection_data.match_id.unique())*100
            }
        ]
    ]


def get_table_data(filtered_bookings, filtered_hmis, unique_ids):
    table_data = []
    for unique_id in unique_ids:
        if unique_id in list(filtered_bookings.match_id):
            last_jail_contact = filtered_bookings[filtered_bookings.match_id == unique_id].jail_entry_date.sort_values(ascending=False).iloc[0].strftime('%Y-%M-%d')
            cumu_jail_days = filtered_bookings[filtered_bookings.match_id == unique_id].days.sum()
            first_name = filtered_bookings[filtered_bookings.match_id == unique_id].first_name.unique()[0]
            last_name = filtered_bookings[filtered_bookings.match_id == unique_id].last_name.unique()[0]
        else:
            last_jail_contact = None
            cumu_jail_days = 0
        # pdb.set_trace()
        if unique_id in list(filtered_hmis.match_id):
            last_hmis_contact = filtered_hmis[filtered_hmis.match_id == unique_id].client_location_start_date.sort_values(ascending=False).iloc[0].strftime('%Y-%M-%d')
            cumu_homeless_days = filtered_hmis[filtered_hmis.match_id == unique_id].days.sum()
            first_name = filtered_hmis[filtered_hmis.match_id == unique_id].first_name.unique()[0]
            last_name = filtered_hmis[filtered_hmis.match_id == unique_id].last_name.unique()[0]
        else:
            last_hmis_contact = None
            cumu_homeless_days = 0

        jail_contact = len(filtered_bookings[filtered_bookings.match_id == unique_id])
        homeless_contact = len(filtered_bookings[filtered_bookings.match_id == unique_id])

        # pdb.set_trace()
        person_data = {
            "matched_id": int(unique_id),
            "booking_id": ','.join(map(str,list(filtered_bookings[filtered_bookings.match_id == unique_id].internal_event_id))),
            "hmis_id": ','.join(map(str,list(filtered_hmis[filtered_hmis.match_id == unique_id].internal_person_id))),
            "first_name": first_name,
            "last_name": last_name,
            "last_jail_contact": last_jail_contact,
            "last_hmis_contact": last_hmis_contact,
            "jail_contact": int(jail_contact),
            "homeless_contact": int(homeless_contact),
            "total_contact": int(jail_contact + homeless_contact),
            "cumu_jail_days": int(cumu_jail_days),
            "cumu_homeless_days": int(cumu_homeless_days)
        }
        table_data.append(person_data)
    return table_data

def get_schema(bookings, hmis, start_date, end_date, duration):
    filters = {
        "controlledDate": "2017-12-11",
        "duration": duration,
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "service": "jail_hmis",
        "flag_homeless_in_jail": True,
        "flag_veteran": False,
        "flag_disability": False,
        "flag_mental_illness": False,
        "setStatus": "All"
    }

    filtered_bookings = bookings[
        (
            (bookings.jail_entry_date >= start_date)
            & (bookings.jail_entry_date <= end_date)
        )
        | (
            (bookings.jail_exit_date >= start_date)
            & (bookings.jail_exit_date <= end_date)
        )
        | (
            (bookings.jail_entry_date <= start_date)
            & (bookings.jail_exit_date >= end_date)
        )
    ]

    filtered_hmis = hmis[
        (
            (hmis.client_location_start_date >= start_date)
            & (hmis.client_location_start_date <= end_date)
        )
        | (
            (hmis.client_location_end_date >= start_date)
            & (hmis.client_location_end_date <= end_date)
        )
        | (
            (hmis.client_location_start_date <= start_date)
            & (hmis.client_location_end_date >= end_date)
        )
    ]
    shared_ids = filtered_hmis[filtered_hmis.match_id.isin(filtered_bookings.match_id)].match_id.unique()
    venn_diagram_data = [
        {
            "sets": [
                "Jail"
            ],
            "size": len(filtered_bookings.match_id.unique())
        },
        {
            "sets": [
                "Homeless"
            ],
            "size": len(filtered_hmis.match_id.unique())
        },
        {
            "sets": [
                "Jail",
                "Homeless"
            ],
            "size": len(shared_ids)
        }
    ]
    # pdb.set_trace()
    filtered_data = {
        "jailBarData": get_bar_chart_data(filtered_bookings, shared_ids, 'Jail'),
        "homelessBarData": get_bar_chart_data(filtered_hmis, shared_ids, 'Homeless'),
        "tableData": get_table_data(filtered_bookings, filtered_hmis, list(set(list(filtered_bookings.match_id.unique())+list(filtered_hmis.match_id.unique()))))
    }

    return {
        "filters": filters,
        "vennDiagramData": venn_diagram_data,
        "filteredData": filtered_data
    }


def run():
    bookings = pd.read_csv('matched_bookings_data_20171207.csv')
    hmis = pd.read_csv('matched_hmis_data_20171207.csv')
    bookings['jail_entry_date'] = pd.to_datetime(bookings['jail_entry_date'])
    bookings['jail_exit_date'] = pd.to_datetime(bookings['jail_exit_date'])
    hmis['client_location_start_date'] = pd.to_datetime(hmis['client_location_start_date'])
    hmis['client_location_end_date'] = pd.to_datetime(hmis['client_location_end_date'])

    year_data = get_schema(bookings, hmis, pd.datetime(2016,12,11), pd.datetime(2017,12,11), '1Y')
    month_data = get_schema(bookings, hmis, pd.datetime(2017,11,1), pd.datetime(2017,11,30,23,59,59), '1M')

    with open('webapp_schema_1y.json', 'w') as outfile:
        json.dump(year_data, outfile)

    with open('webapp_schema_1m.json', 'w') as outfile:
        json.dump(month_data, outfile)


if __name__ == '__main__':
    run()
