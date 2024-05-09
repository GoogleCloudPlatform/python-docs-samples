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

# [START dlp_redact_image_listed_infotypes]
import mimetypes
from typing import List, Optional

import google.cloud.dlp


def redact_image_listed_info_types(
    project: str,
    filename: str,
    output_filename: str,
    info_types: List[str],
    min_likelihood: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> None:
    """Uses the Data Loss Prevention API to redact protected data in an image.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.
            A full list of info type categories can be fetched from the API.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        mime_type: The MIME type of the file. If not specified, the type is
            inferred via the Python standard library's mimetypes module.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare image_redaction_configs, a list of dictionaries. Each dictionary
    # contains an info_type and optionally the color used for the replacement.
    # The color is omitted in this sample, so the default (black) will be used.
    image_redaction_configs = []
    if info_types is not None:
        for info_type in info_types:
            image_redaction_configs.append({"info_type": info_type})

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {"min_likelihood": min_likelihood, "info_types": info_types}

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0] or "application/octet-stream"

    # Select the content type index from the list of supported types.
    # https://github.com/googleapis/googleapis/blob/master/google/privacy/dlp/v2/dlp.proto / message ByteContentItem
    supported_content_types = {
        None: 0,  # "Unspecified" or BYTES_TYPE_UNSPECIFIED
        "image/jpeg": 1,  # IMAGE_JPEG
        "image/bmp": 2,  # IMAGE_BMP
        "image/png": 3,  # IMAGE_PNG
        "image/svg": 4,  # IMAGE_SVG - Adjusted to "image/svg+xml" for correct MIME type
        "text/plain": 5,  # TEXT_UTF8
        # Note: No specific MIME type for general "image", mapping to IMAGE for any image type not specified
        "image": 6,  # IMAGE - Any image type
        "application/msword": 7,  # WORD_DOCUMENT
        "application/pdf": 8,  # PDF
        "application/powerpoint": 9,  # POWERPOINT_DOCUMENT
        "application/msexcel": 10,  # EXCEL_DOCUMENT
        "application/avro": 11,  # AVRO
        "text/csv": 12,  # CSV
        "text/tsv": 13,  # TSV
    }
    content_type_index = supported_content_types.get(mime_type, 0)

    # Construct the byte_item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": content_type_index, "data": f.read()}

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
    print(f"Wrote {len(response.redacted_image)} to {output_filename}")


# [END dlp_redact_image_listed_infotypes]


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
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "--min_likelihood",
        help="A string representing the minimum likelihood threshold"
        "that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED', "
        "'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.",
        default=None,
    )
    parser.add_argument(
        "--mime_type",
        help="The MIME type of the file. If not specified, the type is "
        "inferred via the Python standard library's mimetypes module.",
        default=None,
    )

    args = parser.parse_args()

    redact_image_listed_info_types(
        args.project,
        args.filename,
        args.output_filename,
        args.info_types,
        min_likelihood=args.min_likelihood,
        mime_type=args.mime_type,
    )
