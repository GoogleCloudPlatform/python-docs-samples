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

# [START dlp_inspect_string_custom_hotword]
import google.cloud.dlp


def inspect_string_w_custom_hotword(
    project: str, content_string: str, custom_hotword: str = "patient"
) -> None:
    """Uses the Data Loss Prevention API increase likelihood for matches on
       PERSON_NAME if the user specified custom hot-word is present. Only
       includes findings with the increased likelihood by setting a minimum
       likelihood threshold of VERY_LIKELY.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        custom_hotword: The custom hot-word used for likelihood boosting.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a rule set with caller provided hotword, with a likelihood
    # boost to VERY_LIKELY when the hotword are present within the 50 character-
    # window preceding the PII finding.
    hotword_rule = {
        "hotword_regex": {"pattern": custom_hotword},
        "likelihood_adjustment": {
            "fixed_likelihood": google.cloud.dlp_v2.Likelihood.VERY_LIKELY
        },
        "proximity": {"window_before": 50},
    }

    rule_set = [
        {
            "info_types": [{"name": "PERSON_NAME"}],
            "rules": [{"hotword_rule": hotword_rule}],
        }
    ]

    # Construct the configuration dictionary with the custom regex info type.
    inspect_config = {
        "rule_set": rule_set,
        "min_likelihood": google.cloud.dlp_v2.Likelihood.VERY_LIKELY,
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


# [END dlp_inspect_string_custom_hotword]
