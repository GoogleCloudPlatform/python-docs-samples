# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Uses of the Data Loss Prevention API for deidentifying sensitive data."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_time_extract]
import csv
from datetime import datetime
from typing import List

import google.cloud.dlp


def deidentify_with_time_extract(
    project: str,
    date_fields: List[str],
    input_csv_file: str,
    output_csv_file: str,
) -> None:
    """Uses the Data Loss Prevention API to deidentify dates in a CSV file through
     time part extraction.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        date_fields: A list of (date) fields in CSV file to de-identify
            through time extraction. Example: ['birth_date', 'register_date'].
            Date values in format: mm/DD/YYYY are considered as part of this
            sample.
        input_csv_file: The path to the CSV file to deidentify. The first row
            of the file must specify column names, and all other rows must
            contain valid values.
        output_csv_file: The output file path to save the time extracted data.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert date field list to Protobuf type.
    def map_fields(field):
        return {"name": field}

    if date_fields:
        date_fields = map(map_fields, date_fields)
    else:
        date_fields = []

    csv_lines = []
    with open(input_csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csv_lines.append(row)

    #  Helper function for converting CSV rows to Protobuf types
    def map_headers(header):
        return {"name": header}

    def map_data(value):
        try:
            date = datetime.strptime(value, "%m/%d/%Y")
            return {
                "date_value": {"year": date.year, "month": date.month, "day": date.day}
            }
        except ValueError:
            return {"string_value": value}

    def map_rows(row):
        return {"values": map(map_data, row)}

    # Using the helper functions, convert CSV rows to protobuf-compatible
    # dictionaries.
    csv_headers = map(map_headers, csv_lines[0])
    csv_rows = map(map_rows, csv_lines[1:])

    # Construct the table dictionary.
    table = {"headers": csv_headers, "rows": csv_rows}

    # Construct the `item` for table to de-identify.
    item = {"table": table}

    # Construct deidentify configuration dictionary.
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "time_part_config": {"part_to_extract": "YEAR"}
                    },
                    "fields": date_fields,
                }
            ]
        }
    }

    # Write to CSV helper methods.
    def write_header(header):
        return header.name

    def write_data(data):
        return data.string_value or "{}/{}/{}".format(
            data.date_value.month,
            data.date_value.day,
            data.date_value.year,
        )

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    # Print the result.
    print(f"Table after de-identification: {response.item.table}")

    # Write results to CSV file.
    with open(output_csv_file, "w") as csvfile:
        write_file = csv.writer(csvfile, delimiter=",")
        write_file.writerow(map(write_header, response.item.table.headers))
        for row in response.item.table.rows:
            write_file.writerow(map(write_data, row.values))

    # Print status.
    print(f"Successfully saved date-extracted output to {output_csv_file}")


# [END dlp_deidentify_time_extract]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "input_csv_file",
        help="The path to the CSV file to deidentify. The first row of the "
        "file must specify column names, and all other rows must contain "
        "valid values.",
    )
    parser.add_argument(
        "date_fields",
        nargs="+",
        help="The list of date fields in the CSV file to de-identify. Example: "
        "['birth_date', 'register_date']",
    )
    parser.add_argument(
        "output_csv_file", help="The path to save the time-extracted data."
    )

    args = parser.parse_args()

    deidentify_with_time_extract(
        args.project,
        date_fields=args.date_fields,
        input_csv_file=args.input_csv_file,
        output_csv_file=args.output_csv_file,
    )
