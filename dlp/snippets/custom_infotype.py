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


# [START dlp_inspect_string_with_exclusion_regex]
import google.cloud.dlp  # noqa: F811, E402


def inspect_string_with_exclusion_regex(
    project: str, content_string: str, exclusion_regex: str = ".+@example.com"
) -> None:
    """Inspects the provided text, avoiding matches specified in the exclusion regex

    Uses the Data Loss Prevention API to omit matches on EMAIL_ADDRESS if they match
    the specified exclusion regex.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        exclusion_regex: The regular expression to exclude matches on

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.
    info_types_to_locate = [{"name": "EMAIL_ADDRESS"}]

    # Construct a rule set that will only match on EMAIL_ADDRESS
    # if the specified regex doesn't also match.
    rule_set = [
        {
            "info_types": info_types_to_locate,
            "rules": [
                {
                    "exclusion_rule": {
                        "regex": {"pattern": exclusion_regex},
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_FULL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": info_types_to_locate,
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


# [END dlp_inspect_string_with_exclusion_regex]


# [START dlp_inspect_string_with_exclusion_dict_substring]
from typing import List  # noqa: F811, E402, I100

import google.cloud.dlp  # noqa: F811, E402


def inspect_string_with_exclusion_dict_substring(
    project: str, content_string: str, exclusion_list: List[str] = ["TEST"]
) -> None:
    """Inspects the provided text, avoiding matches that contain excluded tokens

    Uses the Data Loss Prevention API to omit matches if they include tokens
    in the specified exclusion list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        exclusion_list: The list of strings to ignore partial matches on

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.
    info_types_to_locate = [{"name": "EMAIL_ADDRESS"}, {"name": "DOMAIN_NAME"}]

    # Construct a rule set that will only match if the match text does not
    # contains tokens from the exclusion list.
    rule_set = [
        {
            "info_types": info_types_to_locate,
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
        "info_types": info_types_to_locate,
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


# [END dlp_inspect_string_with_exclusion_dict_substring]


# [START dlp_inspect_string_custom_omit_overlap]
import google.cloud.dlp  # noqa: F811, E402


def inspect_string_custom_omit_overlap(project: str, content_string: str) -> None:
    """Matches PERSON_NAME and a custom detector,
    but if they overlap only matches the custom detector

    Uses the Data Loss Prevention API to omit matches on a built-in detector
    if they overlap with matches from a custom detector

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a custom regex detector for names
    custom_info_types = [
        {
            "info_type": {"name": "VIP_DETECTOR"},
            "regex": {"pattern": "Larry Page|Sergey Brin"},
            "exclusion_type": google.cloud.dlp_v2.CustomInfoType.ExclusionType.EXCLUSION_TYPE_EXCLUDE,
        }
    ]

    # Construct a rule set that will exclude PERSON_NAME matches
    # that overlap with VIP_DETECTOR matches
    rule_set = [
        {
            "info_types": [{"name": "PERSON_NAME"}],
            "rules": [
                {
                    "exclusion_rule": {
                        "exclude_info_types": {
                            "info_types": [{"name": "VIP_DETECTOR"}]
                        },
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_FULL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": [{"name": "PERSON_NAME"}],
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


# [END dlp_inspect_string_custom_omit_overlap]

# [START dlp_inspect_string_omit_overlap]
import google.cloud.dlp  # noqa: F811, E402


def inspect_string_omit_overlap(
    project: str,
    content_string: str,
) -> None:
    """Matches PERSON_NAME and EMAIL_ADDRESS, but not both.

    Uses the Data Loss Prevention API omit matches on PERSON_NAME if the
    EMAIL_ADDRESS detector also matches.

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
    info_types_to_locate = [{"name": "PERSON_NAME"}, {"name": "EMAIL_ADDRESS"}]

    # Construct the configuration dictionary that will only match on PERSON_NAME
    # if the EMAIL_ADDRESS doesn't also match. This configuration helps reduce
    # the total number of findings when there is a large overlap between different
    # infoTypes.
    inspect_config = {
        "info_types": info_types_to_locate,
        "rule_set": [
            {
                "info_types": [{"name": "PERSON_NAME"}],
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
        ],
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


# [END dlp_inspect_string_omit_overlap]


# [START dlp_inspect_string_without_overlap]
import google.cloud.dlp  # noqa: F811, E402


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


# [START dlp_inspect_string_multiple_rules]
import google.cloud.dlp  # noqa: F811, E402


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
