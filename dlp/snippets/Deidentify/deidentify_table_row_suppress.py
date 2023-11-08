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


# [START dlp_deidentify_table_row_suppress]
from typing import Dict, List, Union

import google.cloud.dlp


def deidentify_table_suppress_row(
    project: str,
    table_data: Dict[str, Union[List[str], List[List[str]]]],
    condition_field: str,
    condition_operator: str,
    condition_value: int,
) -> None:
    """ Uses the Data Loss Prevention API to de-identify sensitive data in a
      table by suppressing entire row/s based on a condition.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_data: Dictionary representing table data.
        condition_field: A table field within the record this condition is evaluated against.
        condition_operator: Operator used to compare the field or infoType to the value. One of:
            RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS,
            LESS_THAN_OR_EQUALS, EXISTS.
        condition_value: Value to compare against. [Mandatory, except for ``EXISTS`` tests.].

    Example:

    >> $ python deidentify_table_row_suppress.py \
    '{"header": ["email", "phone number", "age"],
    "rows": [["robertfrost@example.com", "4232342345", "35"],
    ["johndoe@example.com", "4253458383", "64"]]}' \
    "age" "GREATER_THAN" 50
    >> '{"header": ["email", "phone number", "age"],
        "rows": [["robertfrost@example.com", "4232342345", "35", "21"]]}'
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

    # Construct the `item` containing the table data.
    item = {"table": table}

    # Construct condition list.
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
            "record_suppressions": [
                {
                    "condition": {
                        "expressions": {"conditions": {"conditions": condition}}
                    }
                }
            ]
        }
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.deidentify_content(
        request={"parent": parent, "deidentify_config": deidentify_config, "item": item}
    )

    # Print the result.
    print(f"Table after de-identification: {response.item.table}")


# [END dlp_deidentify_table_row_suppress]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "table_data",
        help="Json string representing table data",
    )
    parser.add_argument(
        "--condition_field",
        help="A table Field within the record this condition is evaluated " "against.",
    )
    parser.add_argument(
        "--condition_operator",
        help="Operator used to compare the field or infoType to the value. "
        "One of: RELATIONAL_OPERATOR_UNSPECIFIED, EQUAL_TO, NOT_EQUAL_TO, "
        "GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUALS, LESS_THAN_OR_EQUALS, "
        "EXISTS.",
    )
    parser.add_argument(
        "--condition_value",
        help="Value to compare against. [Mandatory, except for ``EXISTS`` tests.].",
    )

    args = parser.parse_args()

    deidentify_table_suppress_row(
        args.project,
        args.table_data,
        condition_field=args.condition_field,
        condition_operator=args.condition_operator,
        condition_value=args.condition_value,
    )
