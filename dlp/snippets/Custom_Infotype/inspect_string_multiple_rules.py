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

# [START dlp_inspect_string_multiple_rules]
import google.cloud.dlp


def inspect_string_multiple_rules(project: str, content_string: str) -> None:
    """Uses the Data Loss Prevention API to modify likelihood for matches on
       PERSON_NAME combining multiple hotword and exclusion rules.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct hotword rules
    patient_rule = {
        "hotword_regex": {"pattern": "patient"},
        "proximity": {"window_before": 10},
        "likelihood_adjustment": {
            "fixed_likelihood": google.cloud.dlp_v2.Likelihood.VERY_LIKELY
        },
    }
    doctor_rule = {
        "hotword_regex": {"pattern": "doctor"},
        "proximity": {"window_before": 10},
        "likelihood_adjustment": {
            "fixed_likelihood": google.cloud.dlp_v2.Likelihood.UNLIKELY
        },
    }

    # Construct exclusion rules
    quasimodo_rule = {
        "dictionary": {"word_list": {"words": ["quasimodo"]}},
        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_PARTIAL_MATCH,
    }
    redacted_rule = {
        "regex": {"pattern": "REDACTED"},
        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_PARTIAL_MATCH,
    }

    # Construct the rule set, combining the above rules
    rule_set = [
        {
            "info_types": [{"name": "PERSON_NAME"}],
            "rules": [
                {"hotword_rule": patient_rule},
                {"hotword_rule": doctor_rule},
                {"exclusion_rule": quasimodo_rule},
                {"exclusion_rule": redacted_rule},
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": [{"name": "PERSON_NAME"}],
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


# [END dlp_inspect_string_multiple_rules]
