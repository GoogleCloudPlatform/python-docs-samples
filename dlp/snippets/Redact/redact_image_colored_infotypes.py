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

"""Sample app that uses the Data Loss Prevent API to redact the contents of
an image file."""


import argparse

# [START dlp_redact_image_colored_infotypes]
import google.cloud.dlp


def redact_image_with_colored_info_types(
    project: str,
    filename: str,
    output_filename: str,
) -> None:
    """Uses the Data Loss Prevention API to redact protected data in an image by
    color coding the infoTypes.
       Args:
           project: The Google Cloud project id to use as a parent resource.
           filename: The path of the image file to inspect.
           output_filename: The path to which the redacted image will be written.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare image_redaction_configs, a list of dictionaries. Each dictionary
    # contains an infoType and the color used for the replacement.

    ssn_redaction_config = {
        "info_type": {"name": "US_SOCIAL_SECURITY_NUMBER"},
        "redaction_color": {
            "red": 0.3,
            "green": 0.1,
            "blue": 0.6,
        },
    }

    email_redaction_config = {
        "info_type": {"name": "EMAIL_ADDRESS"},
        "redaction_color": {
            "red": 0.5,
            "green": 0.5,
            "blue": 1.0,
        },
    }

    phone_redaction_config = {
        "info_type": {"name": "PHONE_NUMBER"},
        "redaction_color": {
            "red": 1.0,
            "green": 0.0,
            "blue": 0.6,
        },
    }

    image_redaction_configs = [
        ssn_redaction_config,
        email_redaction_config,
        phone_redaction_config,
    ]

    # Construct the configuration dictionary.
    inspect_config = {"info_types": [_i["info_type"] for _i in image_redaction_configs]}

    # Construct the byte_item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": "IMAGE", "data": f.read()}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.redact_image(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "image_redaction_configs": image_redaction_configs,
            "byte_item": byte_item,
        }
    )

    # Write out the results.
    with open(output_filename, mode="wb") as f:
        f.write(response.redacted_image)

    byte_count = len(response.redacted_image)
    print(f"Wrote {byte_count} to {output_filename}")


# [END dlp_redact_image_colored_infotypes]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument("filename", help="The path to the file to inspect.")
    parser.add_argument(
        "output_filename",
        help="The path to which the redacted image will be written.",
    )

    args = parser.parse_args()

    redact_image_with_colored_info_types(
        args.project,
        args.filename,
        args.output_filename,
    )
