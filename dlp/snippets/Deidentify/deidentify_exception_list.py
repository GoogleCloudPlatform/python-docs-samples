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

"""Uses of the Data Loss Prevention API for deidentifying sensitive data."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_exception_list]
from typing import List

import google.cloud.dlp


def deidentify_with_exception_list(
    project: str, content_string: str, info_types: List[str], exception_list: List[str]
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
      string but ignore matches against custom list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to deidentify (will be treated as text).
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        exception_list: The list of strings to ignore matches on.

    Returns:
          None; the response from the API is printed to the terminal.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct a list of infoTypes for DLP to locate in `content_string`. See
    # https://cloud.google.com/dlp/docs/concepts-infotypes for more information
    # about supported infoTypes.

    info_types = [{"name": info_type} for info_type in info_types]

    # Construct a rule set that will only match on info_type
    # if the matched text is not in the exception list.
    rule_set = [
        {
            "info_types": info_types,
            "rules": [
                {
                    "exclusion_rule": {
                        "dictionary": {"word_list": {"words": exception_list}},
                        "matching_type": google.cloud.dlp_v2.MatchingType.MATCHING_TYPE_FULL_MATCH,
                    }
                }
            ],
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "info_types": info_types,
        "rule_set": rule_set,
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {"primitive_transformation": {"replace_with_info_type_config": {}}}
            ]
        }
    }

    # Construct the `item`.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print out the results.
    print(response.item.value)


# [END dlp_deidentify_exception_list]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "content_string",
        help="The string to de-identify.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "exception_list",
        help="The list of strings to ignore matches against.",
    )

    args = parser.parse_args()

    deidentify_with_exception_list(
        args.project,
        args.content_string,
        args.info_types,
        args.exception_list,
    )
