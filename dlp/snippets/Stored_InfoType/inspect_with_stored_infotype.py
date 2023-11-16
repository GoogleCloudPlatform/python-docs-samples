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

"""Sample app that queries the Data Loss Prevention API for stored
infoTypes."""


import argparse


# [START dlp_inspect_with_stored_infotype]
import google.cloud.dlp


def inspect_with_stored_infotype(
    project: str,
    stored_info_type_id: str,
    content_string: str,
) -> None:
    """Uses the Data Loss Prevention API to inspect/scan content using stored
    infoType.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        stored_info_type_id: The identifier of stored infoType used to inspect.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert stored infoType id into full resource id
    stored_type_name = f"projects/{project}/storedInfoTypes/{stored_info_type_id}"

    # Construct a custom info type dictionary using stored infoType.
    custom_info_types = [
        {
            "info_type": {"name": "STORED_TYPE"},
            "stored_type": {
                "name": stored_type_name,
            },
        }
    ]

    # Construct the inspection configuration dictionary.
    inspect_config = {
        "custom_info_types": custom_info_types,
        "include_quote": True,
    }

    # Construct the `item` to be inspected using stored infoType.
    item = {"value": content_string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

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
            print(f"Likelihood: {finding.likelihood}")
    else:
        print("No findings.")


# [END dlp_inspect_with_stored_infotype]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "stored_info_type_id",
        help="The identifier for large custom dictionary.",
    )
    parser.add_argument(
        "content_string",
        help="The string to inspect.",
    )

    args = parser.parse_args()

    inspect_with_stored_infotype(
        args.project,
        args.stored_info_type_id,
        args.content_string,
    )
