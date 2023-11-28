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
import json

# [START dlp_inspect_table]
from typing import List, Optional

import google.cloud.dlp


def inspect_table(
    project: str,
    data: str,
    info_types: List[str],
    custom_dictionaries: List[str] = None,
    custom_regexes: List[str] = None,
    min_likelihood: Optional[str] = None,
    max_findings: Optional[int] = None,
    include_quote: bool = True,
) -> None:
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        data: Json string representing table data.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        None; the response from the API is printed to the terminal.
    Example:
        data = {
            "header":[
                "email",
                "phone number"
            ],
            "rows":[
                [
                    "robertfrost@xyz.com",
                    "4232342345"
                ],
                [
                    "johndoe@pqr.com",
                    "4253458383"
                ]
            ]
        }

        >> $ python inspect_content.py table \
        '{"header": ["email", "phone number"],
        "rows": [["robertfrost@xyz.com", "4232342345"],
        ["johndoe@pqr.com", "4253458383"]]}'
        >>  Quote: robertfrost@xyz.com
            Info type: EMAIL_ADDRESS
            Likelihood: 4
            Quote: johndoe@pqr.com
            Info type: EMAIL_ADDRESS
            Likelihood: 4
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [
        {
            "info_type": {"name": f"CUSTOM_DICTIONARY_{i}"},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": f"CUSTOM_REGEX_{i}"},
            "regex": {"pattern": custom_regex},
        }
        for i, custom_regex in enumerate(custom_regexes)
    ]
    custom_info_types = dictionaries + regexes

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "custom_info_types": custom_info_types,
        "min_likelihood": min_likelihood,
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct the `table`. For more details on the table schema, please see
    # https://cloud.google.com/dlp/docs/reference/rest/v2/ContentItem#Table
    headers = [{"name": val} for val in data["header"]]
    rows = []
    for row in data["rows"]:
        rows.append({"values": [{"string_value": cell_val} for cell_val in row]})

    table = {}
    table["headers"] = headers
    table["rows"] = rows
    item = {"table": table}
    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
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


# [END dlp_inspect_table]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "data", help="Json string representing a table.", type=json.loads
    )
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser.add_argument(
        "--custom_dictionaries",
        action="append",
        help="Strings representing comma-delimited lists of dictionary words"
        " to search for as custom info types. Each string is a comma "
        "delimited list of words representing a distinct dictionary.",
        default=None,
    )
    parser.add_argument(
        "--custom_regexes",
        action="append",
        help="Strings representing regex patterns to search for as custom "
        " info types.",
        default=None,
    )
    parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
    )
    parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser.add_argument(
        "--include_quote",
        type=bool,
        help="A boolean for whether to display a quote of the detected "
        "information in the results.",
        default=True,
    )
    args = parser.parse_args()

    inspect_table(
        args.project,
        args.data,
        args.info_types,
        custom_dictionaries=args.custom_dictionaries,
        custom_regexes=args.custom_regexes,
        min_likelihood=args.min_likelihood,
        max_findings=args.max_findings,
        include_quote=args.include_quote,
    )
