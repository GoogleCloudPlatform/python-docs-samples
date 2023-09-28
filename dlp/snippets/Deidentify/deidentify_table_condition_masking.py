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
import base64

# [START dlp_deidentify_table_condition_masking]
from typing import Dict, List, Union  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402
from google.cloud.dlp_v2 import types  # noqa: F811, E402


def deidentify_table_condition_masking(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    deid_content_list: List[str],
    condition_field: str = None,
    condition_operator: str = None,
    condition_value: int = None,
    masking_character: str = None,
) -> types.dlp.Table:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by masking them based on a condition.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Json string representing table data.
        deid_content_list: A list of fields in table to de-identify.
        condition_field: A table Field within the record this condition is evaluated against.
        condition_operator: Operator used to compare the field or infoType to the value. One of:
            RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS,
            LESS_THAN_OR_EQUALS, EXISTS.
        condition_value: Value to compare against. [Mandatory, except for ``EXISTS`` tests.].
        masking_character: The character to mask matching sensitive data with.

    Returns:
        De-identified table is returned;
        the response from the API is also printed to the terminal.

    Example:
    >> $ python deid.py deid_table_condition_mask \
    '{"header": ["email", "phone number", "age", "happiness_score"],
    "rows": [["robertfrost@example.com", "4232342345", "35", "21"],
    ["johndoe@example.com", "4253458383", "64", "34"]]}' \
    ["happiness_score"] "age" "GREATER_THAN" 50
    >> '{"header": ["email", "phone number", "age", "happiness_score"],
        "rows": [["robertfrost@example.com", "4232342345", "35", "21"],
        ["johndoe@example.com", "4253458383", "64", "**"]]}'
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

    # Construct the `item`
    item = {"table": table}

    # Specify fields to be de-identified
    deid_content_list = [{"name": _i} for _i in deid_content_list]

    # Construct condition list
    condition = [
        {
            "field": {"name": condition_field},
            "operator": condition_operator,
            "value": {"integer_value": condition_value},
        }
    ]

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "record_transformations": {
            "field_transformations": [
                {
                    "primitive_transformation": {
                        "character_mask_config": {
                            "masking_character": masking_character
                        }
                    },
                    "fields": deid_content_list,
                    "condition": {
                        "expressions": {"conditions": {"conditions": condition}}
                    },
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print the result
    print(f"Table after de-identification: {response.item.table}")

    # Return the response
    return response.item.table


# [END dlp_deidentify_table_condition_masking]


