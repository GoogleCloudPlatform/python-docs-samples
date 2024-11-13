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

# [START dlp_inspect_string_without_overlap]
import google.cloud.dlp


def inspect_string_without_overlap(project: str, content_string: str) -> None:
    """Matches EMAIL_ADDRESS and DOMAIN_NAME, but DOMAIN_NAME is omitted
    if it overlaps with EMAIL_ADDRESS

    Uses the Data Loss Prevention API to omit matches of one infotype
    that overlap with another.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.
    info_types_to_locate = [{"name": "DOMAIN_NAME"}, {"name": "EMAIL_ADDRESS"}]

    # Define a custom info type to exclude email addresses
    custom_info_types = [
        {
            "info_type": {"name": "EMAIL_ADDRESS"},
            "exclusion_type": google.cloud.dlp_v2.CustomInfoType.ExclusionType.EXCLUSION_TYPE_EXCLUDE,
        }
    ]

    # Construct a rule set that will exclude DOMAIN_NAME matches
    # that overlap with EMAIL_ADDRESS matches
    rule_set = [
        {
            "info_types": [{"name": "DOMAIN_NAME"}],
            "rules": [
                {
                    "exclusion_rule": {
                        "exclude_info_types": {
                            "info_types": [{"name": "EMAIL_ADDRESS"}]
                        },
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_PARTIAL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": info_types_to_locate,
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


# [END dlp_inspect_string_without_overlap]
