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

"""Uses of the Data Loss Prevention API for de-identifying sensitive data
contained in table."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_table_bucketing]
from typing import Dict, List, Union

import google.cloud.dlp
from google.cloud.dlp_v2 import types


def deidentify_table_bucketing(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    deid_content_list: List[str],
    bucket_size: int,
    bucketing_lower_bound: int,
    bucketing_upper_bound: int,
) -> types.dlp.Table:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
    table by replacing them with fixed size bucket ranges.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        deid_content_list: A list of fields in table to de-identify.
        bucket_size: Size of each bucket for fixed sized bucketing
            (except for minimum and maximum buckets). So if ``bucketing_lower_bound`` = 10,
            ``bucketing_upper_bound`` = 89, and ``bucket_size`` = 10, then the
            following buckets would be used: -10, 10-20, 20-30, 30-40,
            40-50, 50-60, 60-70, 70-80, 80-89, 89+.
       bucketing_lower_bound: Lower bound value of buckets.
       bucketing_upper_bound:  Upper bound value of buckets.

    Returns:
       De-identified table is returned;
       the response from the API is also printed to the terminal.

    Example:
    >> $ python deidentify_table_bucketing.py \
        '{"header": ["email", "phone number", "age"],
        "rows": [["robertfrost@example.com", "4232342345", "35"],
        ["johndoe@example.com", "4253458383", "68"]]}' \
        ["age"] 10 0 100
        >>  '{"header": ["email", "phone number", "age"],
            "rows": [["robertfrost@example.com", "4232342345", "30:40"],
            ["johndoe@example.com", "4253458383", "60:70"]]}'
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_data["header"]]
    rows = []
    for row in table_data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item`.
    item = {"table": table}

    # Construct fixed sized bucketing configuration
    fixed_size_bucketing_config = {
        "bucket_size": bucket_size,
        "lower_bound": {"integer_value": bucketing_lower_bound},
        "upper_bound": {"integer_value": bucketing_upper_bound},
    }

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct Deidentify Config
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": deid_content_list,
                    "primitive_transformation": {
                        "fixed_size_bucketing_config": fixed_size_bucketing_config
                    },
                }
            ]
        }
    }

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print the results.
    print(f"Table after de-identification: {response.item.table}")

    # Return the response.
    return response.item.table


# [END dlp_deidentify_table_bucketing]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--table_data",
        help="Json string representing table data",
    )
    parser.add_argument(
        "--deid_content_list", help="A list of fields in table to de-identify."
    )
    parser.add_argument(
        "--bucket_size",
        help="Size of each bucket for fixed sized bucketing.",
    )
    parser.add_argument(
        "--bucketing_lower_bound",
        help="Lower bound value of buckets.",
    )
    parser.add_argument(
        "--bucketing_upper_bound",
        help="Upper bound value of buckets.",
    )

    args = parser.parse_args()

    deidentify_table_bucketing(
        args.project,
        args.table_data,
        args.deid_content_list,
        args.bucket_size,
        args.bucketing_lower_bound,
        args.bucketing_upper_bound,
    )
