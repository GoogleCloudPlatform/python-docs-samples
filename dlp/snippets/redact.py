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

# [START dlp_redact_image]
import mimetypes

# [END dlp_redact_image]
import os

# [START dlp_redact_image]


def redact_image(
    project,
    filename,
    output_filename,
    info_types,
    min_likelihood=None,
    mime_type=None,
):
    """Uses the Data Loss Prevention API to redact protected data in an image.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.
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
    # Import the client library
    import google.cloud.dlp

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
    inspect_config = {
        "min_likelihood": min_likelihood,
        "info_types": info_types,
    }

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0] or "application/octet-stream"

    # Select the content type index from the list of supported types.
    supported_content_types = {
        None: 0,  # "Unspecified"
        "image/jpeg": 1,
        "image/bmp": 2,
        "image/png": 3,
        "image/svg": 4,
        "text/plain": 5,
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
    print(
        "Wrote {byte_count} to {filename}".format(
            byte_count=len(response.redacted_image), filename=output_filename
        )
    )


# [END dlp_redact_image]

# [START dlp_redact_image_all_text]


def redact_image_all_text(
    project,
    filename,
    output_filename,
):
    """Uses the Data Loss Prevention API to redact all text in an image.

    Args:
        project: The Google Cloud project id to use as a parent resource.
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.

    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

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


# [START dlp_redact_image_listed_infotypes]
def redact_image_listed_info_types(
    project,
    filename,
    output_filename,
    info_types,
    min_likelihood=None,
    mime_type=None
):
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

    # Import the client library
    import google.cloud.dlp

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
    inspect_config = {
        "min_likelihood": min_likelihood,
        "info_types": info_types
    }

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0] or "application/octet-stream"

    # Select the content type index from the list of supported types.
    supported_content_types = {
        None: 0,  # "Unspecified"
        "image/jpeg": 1,
        "image/bmp": 2,
        "image/png": 3,
        "image/svg": 4,
        "text/plain": 5,
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
    print(
        "Wrote {byte_count} to {filename}".format(
            byte_count=len(response.redacted_image), filename=output_filename
        )
    )


# [END dlp_redact_image_listed_infotypes]


# [START dlp_redact_image_all_infotypes]
def redact_image_all_info_types(
    project,
    filename,
    output_filename,
):
    """Uses the Data Loss Prevention API to redact protected data in an image.
       Args:
           project: The Google Cloud project id to use as a parent resource.
           filename: The path to the file to inspect.
           output_filename: The path to which the redacted image will be written.
               A full list of info type categories can be fetched from the API.
       Returns:
           None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the byte_item, containing the file's byte data.
    with open(filename, mode="rb") as f:
        byte_item = {"type_": google.cloud.dlp_v2.FileType.IMAGE, "data": f.read()}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.redact_image(
        request={
            "parent": parent,
            "byte_item": byte_item,
        }
    )

    # Write out the results.
    with open(output_filename, mode="wb") as f:
        f.write(response.redacted_image)
    print(f"Wrote {len(response.redacted_image)} to {output_filename}")


# [END dlp_redact_image_all_infotypes]


if __name__ == "__main__":
    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    common_args_parser = argparse.ArgumentParser(add_help=False)
    common_args_parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    common_args_parser.add_argument("filename", help="The path to the file to inspect.")
    common_args_parser.add_argument(
        "output_filename",
        help="The path to which the redacted image will be written.",
    )

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select which content should be redacted."
    )
    subparsers.required = True

    info_types_parser = subparsers.add_parser(
        "info_types",
        help="Redact specific infoTypes from an image.",
        parents=[common_args_parser],
    )
    info_types_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    info_types_parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
    )
    info_types_parser.add_argument(
        "--mime_type",
        help="The MIME type of the file. If not specified, the type is "
        "inferred via the Python standard library's mimetypes module.",
    )

    all_text_parser = subparsers.add_parser(
        "all_text",
        help="Redact all text from an image. The MIME type of the file is "
        "inferred via the Python standard library's mimetypes module.",
        parents=[common_args_parser],
    )

    listed_info_types_parser = subparsers.add_parser(
        "lister_info_types",
        help="Redact specific infoTypes from an image.",
        parents=[common_args_parser],
    )
    listed_info_types_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
    )
    listed_info_types_parser.add_argument(
        "--min_likelihood",
        help="A string representing the minimum likelihood threshold"
        "that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED', "
        "'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.",
        default=None,
    )
    info_types_parser.add_argument(
        "--mime_type",
        help="The MIME type of the file. If not specified, the type is "
        "inferred via the Python standard library's mimetypes module.",
        default=None,
    )

    all_info_types_parser = subparsers.add_parser(
        "all_info_types",
        help="Redact all infoTypes from an image.",
        parents=[common_args_parser],
    )

    args = parser.parse_args()

    if args.content == "info_types":
        redact_image(
            args.project,
            args.filename,
            args.output_filename,
            args.info_types,
            min_likelihood=args.min_likelihood,
            mime_type=args.mime_type,
        )
    elif args.content == "all_text":
        redact_image_all_text(
            args.project,
            args.filename,
            args.output_filename,
        )
    elif args.content == "lister_info_types":
        redact_image_listed_info_types(
            args.project,
            args.filename,
            args.output_filename,
            args.info_types,
            min_likelihood=args.min_likelihood,
            mime_type=args.mime_type,
        )
    elif args.content == "all_info_types":
        redact_image_all_info_types(
            args.project,
            args.filename,
            args.output_filename,
        )
