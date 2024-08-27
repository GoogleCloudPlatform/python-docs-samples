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


# [START dlp_deidentify_dictionary_replacement]
from typing import List

import google.cloud.dlp


def deindentify_with_dictionary_replacement(
    project: str,
    input_str: str,
    info_types: List[str],
    word_list: List[str],
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
    string by replacing each piece of detected sensitive data with a value
    that Cloud DLP randomly selects from a list of words that you provide.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        info_types: A list of strings representing infoTypes to look for.
        word_list: List of words or phrases to search for in the data.
    """

    # Instantiate a client
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct list of info types
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct deidentify configuration dictionary
    deidentify_config = {
        "info_type_transformations": {
            "transformations": [
                {
                    "info_types": info_types,
                    "primitive_transformation": {
                        "replace_dictionary_config": {"word_list": {"words": word_list}}
                    },
                }
            ]
        }
    }

    # Construct the `item`
    item = {"value": input_str}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API
    response = dlp.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": deidentify_config,
            "inspect_config": {"info_types": info_types},
            "item": item,
        }
    )

    # Print out the results.
    print(f"De-identified Content: {response.item.value}")


# [END dlp_deidentify_dictionary_replacement]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "input_str",
        help="The string to de-identify.",
    )
    parser.add_argument(
        "word_list", help="List of words or phrases to search for in the data."
    )

    args = parser.parse_args()

    deindentify_with_dictionary_replacement(
        args.project,
        args.input_str,
        args.info_types,
        args.word_list,
    )
