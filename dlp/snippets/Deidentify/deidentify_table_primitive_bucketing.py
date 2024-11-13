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

# [START dlp_deidentify_table_primitive_bucketing]
import google.cloud.dlp


def deidentify_table_primitive_bucketing(
    project: str,
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in
    a table by replacing them with generalized bucket labels.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Dictionary representing table to de-identify.
    # The table can also be taken as input to the function.
    table_to_deid = {
        "header": ["age", "patient", "happiness_score"],
        "rows": [
            ["101", "Charles Dickens", "95"],
            ["22", "Jane Austen", "21"],
            ["90", "Mark Twain", "75"],
        ],
    }

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_to_deid["header"]]
    rows = []
    for row in table_to_deid["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct the `item` for table to de-identify.
    item = {"table": table}

    # Construct generalised bucket configuration.
    buckets_config = [
        {
            "min_": {"integer_value": 0},
            "max_": {"integer_value": 25},
            "replacement_value": {"string_value": "Low"},
        },
        {
            "min_": {"integer_value": 25},
            "max_": {"integer_value": 75},
            "replacement_value": {"string_value": "Medium"},
        },
        {
            "min_": {"integer_value": 75},
            "max_": {"integer_value": 100},
            "replacement_value": {"string_value": "High"},
        },
    ]

    # Construct de-identify configuration that groups values in a table field and replace those with bucket labels.
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "fields": [{"name": "happiness_score"}],
                    "primitive_transformation": {
                        "bucketing_config": {"buckets": buckets_config}
                    },
                }
            ]
        }
    }

    # Call the API to deidentify table data through primitive bucketing.
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
        }
    )

    # Print the results.
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_primitive_bucketing]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )

    args = parser.parse_args()

    deidentify_table_primitive_bucketing(args.project)
