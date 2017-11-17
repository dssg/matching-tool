
import argparse
import json
import pandas as pd


def main(input_filename, output_filename):
    with open(input_filename) as f:
        schema = json.load(f)
    df = pd.DataFrame(schema['filteredData']['tableData'])
    df.to_csv(
        output_filename,
        index=False,
        columns=[
            'matched_id',
            'hmis_id',
            'booking_id',
            'first_name',
            'last_name',
            'cumu_homeless_days',
            'cumu_jail_days',
            'total_contact',
            'homeless_contact',
            'jail_contact',
            'last_hmis_contact',
            'last_jail_contact'
        ]
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_filename",
        type=str,
        help="what file do you want to convert?"
    )
    parser.add_argument(
        "-o",
        "--output_filename",
        type=str,
        help='how should i name the output?'
    )

    args = parser.parse_args()
    main(args.input_filename, args.output_filename)
