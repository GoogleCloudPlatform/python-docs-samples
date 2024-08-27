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

# [START dlp_inspect_augment_infotypes]
from typing import List

import google.cloud.dlp


def inspect_string_augment_infotype(
    project: str,
    input_str: str,
    info_type: str,
    word_list: List[str],
) -> None:
    """Uses the Data Loss Prevention API to augment built-in infoType
    detector and inspect the content string with augmented infoType.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to inspect using augmented infoType
            (will be treated as text).
        info_type: A string representing built-in infoType to augment.
            A full list of infoType categories can be fetched from the API.
        word_list: List of words or phrases to be added to extend the behaviour
            of built-in infoType.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the custom infoTypes dictionary with declaration of a built-in detector.
    custom_info_types = [
        {
            "info_type": {"name": info_type},
            "dictionary": {"word_list": {"words": word_list}},
        }
    ]

    # Construct inspect configuration dictionary with the custom info type.
    inspect_config = {
        "custom_info_types": custom_info_types,
        "include_quote": True,
    }

    # Construct the `item` to be inspected.
    item = {"value": input_str}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    # Print out the results.
    if response.result.findings:
        for finding in response.result.findings:
            print(f"Quote: {finding.quote}")
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood} \n")
    else:
        print("No findings.")


# [END dlp_inspect_augment_infotypes]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument("input_str", help="The string to inspect.")
    parser.add_argument(
        "--info_type",
        help="A String representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "--word_list",
        help="List of words or phrases to be added to extend the behaviour "
        "of built-in infoType.",
    )
    args = parser.parse_args()

    inspect_string_augment_infotype(
        args.project,
        args.input_str,
        args.info_type,
        args.word_list,
    )
