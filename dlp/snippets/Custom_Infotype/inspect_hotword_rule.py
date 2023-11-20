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

# [START dlp_inspect_hotword_rule]
import google.cloud.dlp


def inspect_data_w_custom_hotwords(
    project: str,
    content_string: str,
) -> None:
    """Uses the Data Loss Prevention API to analyze string with medical record
       number custom regex detector, with custom hotwords rules to boost finding
       certainty under some circumstances.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a custom regex detector info type called "C_MRN",
    # with ###-#-##### pattern, where each # represents a digit from 1 to 9.
    # The detector has a detection likelihood of POSSIBLE.
    custom_info_types = [
        {
            "info_type": {"name": "C_MRN"},
            "regex": {"pattern": "[1-9]{3}-[1-9]{1}-[1-9]{5}"},
            "likelihood": google.cloud.dlp_v2.Likelihood.POSSIBLE,
        }
    ]

    # Construct a rule set with hotwords "mrn" and "medical", with a likelohood
    # boost to VERY_LIKELY when hotwords are present within the 10 character-
    # window preceding the PII finding.
    hotword_rule = {
        "hotword_regex": {"pattern": "(?i)(mrn|medical)(?-i)"},
        "likelihood_adjustment": {
            "fixed_likelihood": google.cloud.dlp_v2.Likelihood.VERY_LIKELY
        },
        "proximity": {"window_before": 10},
    }

    rule_set = [
        {"info_types": [{"name": "C_MRN"}], "rules": [{"hotword_rule": hotword_rule}]}
    ]

    # Construct the configuration dictionary with the custom regex info type.
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


# [END dlp_inspect_hotword_rule]
