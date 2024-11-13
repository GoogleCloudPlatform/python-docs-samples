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

# [START dlp_deidentify_simple_word_list]
import google.cloud.dlp


def deidentify_with_simple_word_list(
    project: str,
    input_str: str,
    custom_info_type_name: str,
    word_list: list[str],
) -> None:
    """Uses the Data Loss Prevention API to de-identify sensitive data in a
      string by matching against custom word list.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_str: The string to deidentify (will be treated as text).
        custom_info_type_name: The name of the custom info type to use.
        word_list: The list of strings to match against.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare custom_info_types by parsing word lists
    word_list = {"words": word_list}
    custom_info_types = [
        {
            "info_type": {"name": custom_info_type_name},
            "dictionary": {"word_list": word_list},
        }
    ]

    # Construct the configuration dictionary
    inspect_config = {
        "custom_info_types": custom_info_types,
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
    item = {"value": input_str}

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

    print(f"De-identified Content: {response.item.value}")


# [END dlp_deidentify_simple_word_list]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "input_str",
        help="The string to deidentify.",
    )
    parser.add_argument(
        "custom_info_type_name",
        help="The name of the custom info type to use.",
    )
    parser.add_argument(
        "word_list",
        help="The list of strings to match against.",
    )

    args = parser.parse_args()

    deidentify_with_simple_word_list(
        args.project,
        args.input_str,
        args.custom_info_type_name,
        args.word_list,
    )
