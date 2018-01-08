# Copyright 2017 Google Inc.
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
a string or an image file."""

from __future__ import print_function

import argparse
import mimetypes


# [START redact_string]
def redact_string(item, replace_string, info_types=None, min_likelihood=None):
    """Uses the Data Loss Prevention API to redact protected data in a string.
    Args:
        item: The string to inspect.
        replace_string: The string to use to replace protected data; for
            instance, '***' or 'REDACTED'. An empty string is permitted.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API. If
            info_types is omitted, the API will use a limited default set.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if info_types is not None:
        info_types = [{'name': info_type} for info_type in info_types]

    # Prepare replace_configs, a list of dictionaries. Each dictionary contains
    # an info_type and the string to which that info_type will be redacted upon
    # detection. This sample uses the same "replace_string" for all info types,
    # though the API supports using different ones for each type.
    replace_configs = []

    if info_types is not None:
        for info_type in info_types:
            replace_configs.append(
                {'info_type': info_type,
                 'replace_with': replace_string})
    else:
        # If no info_type is specified, prepare a single dictionary with only a
        # replace_string as a catch-all.
        replace_configs.append({'replace_with': replace_string})

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    redact_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
    }

    # Construct the items list (in this case, only one item, in string form).
    items = [{'type': 'text/plain', 'value': item}]

    # Call the API.
    response = dlp.redact_content(redact_config, items, replace_configs)

    # Print out the results.
    print(response.items[0].value)
# [END redact_string]


# [START redact_image]
def redact_image(filename, output_filename,
                 info_types=None, min_likelihood=None, mime_type=None):
    """Uses the Data Loss Prevention API to redact protected data in an image.
    Args:
        filename: The path to the file to inspect.
        output_filename: The path to which the redacted image will be written.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API. If
            info_types is omitted, the API will use a limited default set.
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
    dlp = google.cloud.dlp.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted). The info_types are not submitted
    # directly in this example, but are used in the construction of
    # image_redaction_configs.
    if info_types is not None:
        info_types = [{'name': info_type} for info_type in info_types]

    # Prepare image_redaction_configs, a list of dictionaries. Each dictionary
    # contains an info_type and optionally the color used for the replacement.
    # The color is omitted in this sample, so the default (black) will be used.
    image_redaction_configs = []

    if info_types is not None:
        for info_type in info_types:
            image_redaction_configs.append({'info_type': info_type})

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    redact_config = {
        'min_likelihood': min_likelihood,
    }

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0] or 'application/octet-stream'

    # Construct the items list (in this case, only one item, containing the
    # image file's byte data).
    with open(filename, mode='rb') as f:
        items = [{'type': mime_type, 'data': f.read()}]

    # Call the API.
    response = dlp.redact_content(
        redact_config, items, None,
        image_redaction_configs=image_redaction_configs)

    # Write out the results.
    with open(output_filename, mode='wb') as f:
        f.write(response.items[0].data)
    print("Wrote {byte_count} to {filename}".format(
        byte_count=len(response.items[0].data), filename=output_filename))
# [END redact_string]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='content', help='Select how to submit content to the API.')

    parser_string = subparsers.add_parser('string', help='Inspect a string.')
    parser_string.add_argument('item', help='The string to inspect.')
    parser_string.add_argument(
        'replace_string',
        help='The string to use to replace protected data; for instance, '
             '"***" or "REDACTED".')
    parser_string.add_argument(
        '--info_types', action='append',
        help='Strings representing info types to look for. A full list of '
             'info categories and types is available from the API. Examples '
             'include "US_MALE_NAME", "US_FEMALE_NAME", "EMAIL_ADDRESS", '
             '"CANADA_SOCIAL_INSURANCE_NUMBER", "JAPAN_PASSPORT". If omitted, '
             'the API will use a limited default set. Specify this flag '
             'multiple times to specify multiple info types.')
    parser_string.add_argument(
        '--min_likelihood',
        choices=['LIKELIHOOD_UNSPECIFIED', 'VERY_UNLIKELY', 'UNLIKELY',
                 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'],
        help='A string representing the minimum likelihood threshold that '
             'constitutes a match.')

    parser_file = subparsers.add_parser('image', help='Inspect an image file.')
    parser_file.add_argument(
        'filename', help='The path to the file to inspect.')
    parser_file.add_argument(
        'output_filename',
        help='The path to which the redacted image will be written.')
    parser_file.add_argument(
        '--info_types', action='append',
        help='Strings representing info types to look for. A full list of '
             'info categories and types is available from the API. Examples '
             'include "US_MALE_NAME", "US_FEMALE_NAME", "EMAIL_ADDRESS", '
             '"CANADA_SOCIAL_INSURANCE_NUMBER", "JAPAN_PASSPORT". If omitted, '
             'the API will use a limited default set. Specify this flag '
             'multiple times to specify multiple info types.')
    parser_file.add_argument(
        '--min_likelihood',
        choices=['LIKELIHOOD_UNSPECIFIED', 'VERY_UNLIKELY', 'UNLIKELY',
                 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'],
        help='A string representing the minimum likelihood threshold that '
             'constitutes a match.')
    parser_file.add_argument(
        '--mime_type',
        help='The MIME type of the file. If not specified, the type is '
             'inferred via the Python standard library\'s mimetypes module.')

    args = parser.parse_args()

    if args.content == 'string':
        redact_string(
            args.item, args.replace_string, info_types=args.info_types,
            min_likelihood=args.min_likelihood)
    elif args.content == 'image':
        redact_image(
            args.filename, args.output_filename, info_types=args.info_types,
            min_likelihood=args.min_likelihood, mime_type=args.mime_type)
