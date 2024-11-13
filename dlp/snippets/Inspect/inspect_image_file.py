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

# [START dlp_inspect_image_file]
import google.cloud.dlp


def inspect_image_file(
    project: str,
    filename: str,
    include_quote: bool = True,
) -> None:
    """Uses the Data Loss Prevention API to analyze strings for
    protected data in image file.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    """
    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = ["PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD_NUMBER"]
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration for the Inspect request.
    inspect_config = {
        "info_types": info_types,
        "include_quote": include_quote,
    }

    # Construct the byte_item, containing the image file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": "IMAGE", "data": f.read()}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call the API.
    response = dlp.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": {"byte_item": byte_item},
        }
    )

    # Parse the response and process results.
    if response.result.findings:
        for finding in response.result.findings:
            print(f"Quote: {finding.quote}")
            print(f"Info type: {finding.info_type.name}")
            print(f"Likelihood: {finding.likelihood}")
    else:
        print("No findings.")


# [END dlp_inspect_image_file]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument("filename", help="The path to the file to inspect.")
    parser.add_argument(
        "--include_quote",
        help="A Boolean for whether to display a quote of the detected"
        "information in the results.",
        default=True,
    )
    args = parser.parse_args()

    inspect_image_file(
        args.project,
        args.filename,
        include_quote=args.include_quote,
    )
