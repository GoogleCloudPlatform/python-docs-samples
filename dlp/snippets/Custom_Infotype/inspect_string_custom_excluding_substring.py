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
"""Custom infoType snippets.

This file contains sample code that uses the Data Loss Prevention API to create
custom infoType detectors to refine scan results.
"""

# [START dlp_inspect_string_custom_excluding_substring]
from typing import List

import google.cloud.dlp


def inspect_string_custom_excluding_substring(
    project: str, content_string: str, exclusion_list: List[str] = ["jimmy"]
) -> None:
    """Inspects the provided text with a custom detector, avoiding matches on specific tokens

    Uses the Data Loss Prevention API to omit matches on a custom detector
    if they include tokens in the specified exclusion list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        exclusion_list: The list of strings to ignore matches on

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a custom regex detector for names
    custom_info_types = [
        {
            "info_type": {"name": "CUSTOM_NAME_DETECTOR"},
            "regex": {"pattern": "[A-Z][a-z]{1,15}, [A-Z][a-z]{1,15}"},
        }
    ]

    # Construct a rule set that will only match if the match text does not
    # contains tokens from the exclusion list.
    rule_set = [
        {
            "info_types": [{"name": "CUSTOM_NAME_DETECTOR"}],
            "rules": [
                {
                    "exclusion_rule": {
                        "dictionary": {"word_list": {"words": exclusion_list}},
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_PARTIAL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "custom_info_types": custom_info_types,
        "rule_set": rule_set,
        "include_quote": True,
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            print(f"Quote: {finding.quote}")
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood}")
    else:
        print("No findings.")


# [END dlp_inspect_string_custom_excluding_substring]
