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

# [START dlp_redact_image_all_text]
import google.cloud.dlp


def redact_image_all_text(
    project: str,
    filename: str,
    output_filename: str,
) -> None:
    """Uses the Data Loss Prevention API to redact all text in an image.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the image_redaction_configs, indicating to DLP that all text in
    # the input image should be redacted.
    image_redaction_configs = [{"redact_all_text": True}]

    # Construct the byte_item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": google.cloud.dlp_v2.FileType.IMAGE, "data": f.read()}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.redact_image(
        request={
            "parent": parent,
            "image_redaction_configs": image_redaction_configs,
            "byte_item": byte_item,
        }
    )

    # Write out the results.
    with open(output_filename, mode="wb") as f:
        f.write(response.redacted_image)

    print(
        "Wrote {byte_count} to {filename}".format(
            byte_count=len(response.redacted_image), filename=output_filename
        )
    )


# [END dlp_redact_image_all_text]


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

    redact_image_all_text(
        args.project,
        args.filename,
        args.output_filename,
    )
