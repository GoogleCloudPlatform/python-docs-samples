# Copyright 2020 Google Inc.
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


# [START dlp_omit_name_if_also_email]
def omit_name_if_also_email(
    project,
    content_string,
):
    """Marches PERSON_NAME and EMAIL_ADDRESS, but not both.

    Uses the Data Loss Prevention API omit matches on PERSON_NAME if the
    EMAIL_ADDRESS detector also matches.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.
    info_types_to_locate = [{"name": "PERSON_NAME"}, {"name": "EMAIL_ADDRESS"}]

    # Construct the configuration dictionary that will only match on PERSON_NAME
    # if the EMAIL_ADDRESS doesn't also match. This configuration helps reduce
    # the total number of findings when there is a large overlap between different
    # infoTypes.
    inspect_config = {
        "info_types":
            info_types_to_locate,
        "rule_set": [{
            "info_types": [{
                "name": "PERSON_NAME"
            }],
            "rules": [{
                "exclusion_rule": {
                    "exclude_info_types": {
                        "info_types": [{
                            "name": "EMAIL_ADDRESS"
                        }]
                    },
                    "matching_type": "MATCHING_TYPE_PARTIAL_MATCH"
                }
            }]
        }]
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.inspect_content(parent, inspect_config, item)

    return [f.info_type.name for f in response.result.findings]


# [END dlp_omit_name_if_also_email]


# [START inspect_with_person_name_w_custom_hotword]
def inspect_with_person_name_w_custom_hotword(
    project,
    content_string,
    custom_hotword="patient"
):
    """Uses the Data Loss Prevention API increase likelihood for matches on
       PERSON_NAME if the user specified custom hotword is present. Only
       includes findings with the increased likelihood by setting a minimum
       likelihood threshold of VERY_LIKELY.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        custom_hotword: The custom hotword used for likelihood boosting.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a rule set with caller provided hotword, with a likelihood
    # boost to VERY_LIKELY when the hotword are present within the 50 character-
    # window preceding the PII finding.
    hotword_rule = {
        "hotword_regex": {"pattern": custom_hotword},
        "likelihood_adjustment": {"fixed_likelihood": "VERY_LIKELY"},
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
        "min_likelihood": "VERY_LIKELY",
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.inspect_content(parent, inspect_config, item)

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

# [END inspect_with_person_name_w_custom_hotword]


# [START dlp_inspect_with_medical_record_number_custom_regex_detector]
def inspect_with_medical_record_number_custom_regex_detector(
    project,
    content_string,
):
    """Uses the Data Loss Prevention API to analyze string with medical record
       number custom regex detector
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a custom regex detector info type called "C_MRN",
    # with ###-#-##### pattern, where each # represents a digit from 1 to 9.
    # The detector has a detection likelihood of POSSIBLE.
    custom_info_types = [
        {
            "info_type": {"name": "C_MRN"},
            "regex": {"pattern": "[1-9]{3}-[1-9]{1}-[1-9]{5}"},
            "likelihood": "POSSIBLE",
        }
    ]

    # Construct the configuration dictionary with the custom regex info type.
    inspect_config = {
        "custom_info_types": custom_info_types,
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.inspect_content(parent, inspect_config, item)

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

# [END dlp_inspect_with_medical_record_number_custom_regex_detector]


# [START dlp_inspect_with_medical_record_number_w_custom_hotwords]
def inspect_with_medical_record_number_w_custom_hotwords(
    project,
    content_string,
):
    """Uses the Data Loss Prevention API to analyze string with medical record
       number custom regex detector, with custom hotwords rules to boost finding
       certainty under some circumstances.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a custom regex detector info type called "C_MRN",
    # with ###-#-##### pattern, where each # represents a digit from 1 to 9.
    # The detector has a detection likelihood of POSSIBLE.
    custom_info_types = [
        {
            "info_type": {"name": "C_MRN"},
            "regex": {"pattern": "[1-9]{3}-[1-9]{1}-[1-9]{5}"},
            "likelihood": "POSSIBLE",
        }
    ]

    # Construct a rule set with hotwords "mrn" and "medical", with a likelohood
    # boost to VERY_LIKELY when hotwords are present within the 10 character-
    # window preceding the PII finding.
    hotword_rule = {
        "hotword_regex": {
            "pattern": "(?i)(mrn|medical)(?-i)"
        },
        "likelihood_adjustment": {
            "fixed_likelihood": "VERY_LIKELY"
        },
        "proximity": {
            "window_before": 10
        }
    }

    rule_set = [
        {
            "info_types": [{"name": "C_MRN"}],
            "rules": [{"hotword_rule": hotword_rule}],
        }
    ]

    # Construct the configuration dictionary with the custom regex info type.
    inspect_config = {
        "custom_info_types": custom_info_types,
        "rule_set": rule_set,
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = dlp.project_path(project)

    # Call the API.
    response = dlp.inspect_content(parent, inspect_config, item)

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

# [END dlp_inspect_with_medical_record_number_w_custom_hotwords]
