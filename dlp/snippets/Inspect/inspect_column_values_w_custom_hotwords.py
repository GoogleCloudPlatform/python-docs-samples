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

"""Sample app that uses the Data Loss Prevention API to inspect a string, a
local file or a file on Google Cloud Storage."""


import argparse

# [START dlp_inspect_column_values_w_custom_hotwords]
from typing import List

import google.cloud.dlp


def inspect_column_values_w_custom_hotwords(
    project: str,
    table_header: List[str],
    table_rows: List[List[str]],
    info_types: List[str],
    custom_hotword: str,
) -> None:
    """Uses the Data Loss Prevention API to inspect table data using built-in
    infoType detectors, excluding columns that match a custom hot-word.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        table_header: List of strings representing table field names.
        table_rows: List of rows representing table values.
        info_types: The infoType for which hot-word rule is applied.
        custom_hotword: The custom regular expression used for likelihood boosting.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in table_header]
    rows = []
    for row in table_rows:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})
    table = {"headers": headers, "rows": rows}

    # Construct the `item` for table to be inspected.
    item = {"table": table}

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct a rule set with caller provided hot-word, with a likelihood
    # boost to VERY_UNLIKELY when the hot-word are present
    hotword_rule = {
        "hotword_regex": {"pattern": custom_hotword},
        "likelihood_adjustment": {
            "fixed_likelihood": google.cloud.dlp_v2.Likelihood.VERY_UNLIKELY
        },
        "proximity": {"window_before": 1},
    }

    rule_set = [
        {
            "info_types": info_types,
            "rules": [{"hotword_rule": hotword_rule}],
        }
    ]

    # Construct the configuration dictionary, which defines the entire inspect content task.
    inspect_config = {
        "info_types": info_types,
        "rule_set": rule_set,
        "min_likelihood": google.cloud.dlp_v2.Likelihood.POSSIBLE,
        "include_quote": True,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API
    response = dlp.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            try:
                if finding.quote:
                    print(f"Quote: {finding.quote}")
            except AttributeError:
                pass
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood}")
    else:
        print("No findings.")


# [END dlp_inspect_column_values_w_custom_hotwords]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--table_header",
        help="List of strings representing table field names."
        "Example include '['Fake_Email_Address', 'Real_Email_Address]'. "
        "The method can be used to exclude matches from entire column"
        '"Fake_Email_Address".',
    )
    parser.add_argument(
        "--table_rows",
        help="List of rows representing table values."
        "Example: "
        '"[["example1@example.org", "test1@example.com],'
        '["example2@example.org", "test2@example.com]]"',
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "custom_hotword",
        help="The custom regular expression used for likelihood boosting.",
    )

    args = parser.parse_args()

    inspect_column_values_w_custom_hotwords(
        args.project,
        args.table_header,
        args.table_rows,
        args.info_types,
        args.custom_hotword,
    )
