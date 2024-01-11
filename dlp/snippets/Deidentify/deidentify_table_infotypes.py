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


# [START dlp_deidentify_table_infotypes]
from typing import Dict, List, Union

import google.cloud.dlp


def deidentify_table_replace_with_info_types(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    info_types: List[str],
    deid_content_list: List[str],
) -> None:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by replacing them with info type.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Json string representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        deid_content_list: A list of fields in table to de-identify

    Returns:
        None; the response from the API is printed to the terminal.

    Example:
    >> $ python deidentify_table_infotypes.py \
    '{
        "header": ["name", "email", "phone number"],
        "rows": [
            ["Robert Frost", "robertfrost@example.com", "4232342345"],
            ["John Doe", "johndoe@example.com", "4253458383"]
        ]
    }' \
    ["PERSON_NAME"] ["name"]
    >> '{
            "header": ["name", "email", "phone number"],
            "rows": [
                ["[PERSON_NAME]", "robertfrost@example.com", "4232342345"],
                ["[PERSON_NAME]", "johndoe@example.com", "4253458383"]
            ]
        }'
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_data["header"]]
    rows = []
    for row in table_data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {"headers": headers, "rows": rows}

    # Construct item
    item = {"table": table}

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct inspect configuration dictionary
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "info_type_transformations": {
                        "transformations": [
                            {
                                "primitive_transformation": {
                                    "replace_with_info_type_config": {}
                                }
                            }
                        ]
                    },
                    "fields": deid_content_list,
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "item": item,
            "inspect_config": inspect_config,
        }
    )

    # Print the result
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_infotypes]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "table_data",
        help="Json string representing a table.",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "deid_content_list",
        help="A list of fields in table to de-identify.",
    )

    args = parser.parse_args()

    deidentify_table_replace_with_info_types(
        args.project,
        args.table_data,
        args.info_types,
        args.deid_content_list,
    )
