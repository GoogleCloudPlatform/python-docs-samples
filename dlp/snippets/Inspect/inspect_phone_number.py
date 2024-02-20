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

# [START dlp_inspect_phone_number]
import google.cloud.dlp


def inspect_phone_number(
    project: str,
    content_string: str,
) -> None:
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect phone number from.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": "PHONE_NUMBER"}]

    # Construct the configuration dictionary.
    inspect_config = {
        "info_types": info_types,
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


# [END dlp_inspect_phone_number]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "content_string",
        help="The string to inspect phone number from.",
    )
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    args = parser.parse_args()

    inspect_phone_number(args.project, args.content_string)
