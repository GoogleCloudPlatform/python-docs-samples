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

"""Sample app that uses the Data Loss Prevention API to inspect a string, a
local file or a file on Google Cloud Storage."""

from __future__ import print_function

import argparse


# [START inspect_string]
def inspect_string(item, info_types=None, min_likelihood=None,
                   max_findings=None, include_quote=True):
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        item: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API. If
            info_types is omitted, the API will use a limited default set.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
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

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'max_findings': max_findings,
        'include_quote': include_quote,
    }

    # Construct the items list (in this case, only one item, in string form).
    items = [{'type': 'text/plain', 'value': item}]

    # Call the API.
    response = dlp.inspect_content(inspect_config, items)

    # Print out the results.
    if response.results[0].findings:
        for finding in response.results[0].findings:
            try:
                print('Quote: {}'.format(finding.quote))
            except AttributeError:
                pass
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END inspect_string]


# [START inspect_file]
def inspect_file(filename, info_types=None, min_likelihood=None,
                 max_findings=None, include_quote=True, mime_type=None):
    """Uses the Data Loss Prevention API to analyze a file for protected data.
    Args:
        filename: The path to the file to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API. If
            info_types is omitted, the API will use a limited default set.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
        mime_type: The MIME type of the file. If not specified, the type is
            inferred via the Python standard library's mimetypes module.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    import mimetypes

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if info_types is not None:
        info_types = [{'name': info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'max_findings': max_findings,
        'include_quote': include_quote,
    }

    # If mime_type is not specified, guess it from the filename.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0] or 'application/octet-stream'

    # Construct the items list (in this case, only one item, containing the
    # file's byte data).
    with open(filename, mode='rb') as f:
        items = [{'type': mime_type, 'data': f.read()}]

    # Call the API.
    response = dlp.inspect_content(inspect_config, items)

    # Print out the results.
    if response.results[0].findings:
        for finding in response.results[0].findings:
            try:
                print('Quote: {}'.format(finding.quote))
            except AttributeError:
                pass
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END inspect_file]


# [START inspect_gcs_file]
def inspect_gcs_file(bucket, filename, info_types=None, min_likelihood=None,
                     max_findings=None):
    """Uses the Data Loss Prevention API to analyze a file on GCS.
    Args:
        bucket: The name of the GCS bucket containing the file, as a string.
        filename: The name of the file in the bucket, including the path, as a
            string; e.g. 'images/myfile.png'.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API. If
            info_types is omitted, the API will use a limited default set.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
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

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'max_findings': max_findings,
    }

    # Construct a cloud_storage_options dictionary with the file's URL.
    url = 'gs://{}/{}'.format(bucket, filename)
    storage_config = {
        'cloud_storage_options': {
            'file_set': {'url': url}
            }
        }

    operation = dlp.create_inspect_operation(inspect_config, storage_config,
                                             None)

    # Get the operation result name, which can be used to look up the full
    # results. This call blocks until the operation is complete; to avoid
    # blocking, use operation.add_done_callback(fn) instead.
    operation_result = operation.result()

    response = dlp.list_inspect_findings(operation_result.name)

    if response.result.findings:
        for finding in response.result.findings:
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END inspect_gcs_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='content', help='Select how to submit content to the API.')

    parser_string = subparsers.add_parser('string', help='Inspect a string.')
    parser_string.add_argument('item', help='The string to inspect.')
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
    parser_string.add_argument(
        '--max_findings', type=int,
        help='The maximum number of findings to report; 0 = no maximum.')
    parser_string.add_argument(
        '--include_quote', type=bool,
        help='A boolean for whether to display a quote of the detected '
             'information in the results.')

    parser_file = subparsers.add_parser('file', help='Inspect a local file.')
    parser_file.add_argument(
        'filename', help='The path to the file to inspect.')
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
        '--max_findings', type=int,
        help='The maximum number of findings to report; 0 = no maximum.')
    parser_file.add_argument(
        '--include_quote', type=bool,
        help='A boolean for whether to display a quote of the detected '
             'information in the results.')
    parser_file.add_argument(
        '--mime_type',
        help='The MIME type of the file. If not specified, the type is '
             'inferred via the Python standard library\'s mimetypes module.')

    parser_gcs = subparsers.add_parser(
        'gcs', help='Inspect files on Google Cloud Storage.')
    parser_gcs.add_argument(
        'bucket', help='The name of the GCS bucket containing the file.')
    parser_gcs.add_argument(
        'filename',
        help='The name of the file in the bucket, including the path, e.g. '
        '"images/myfile.png". Wildcards are permitted.')
    parser_gcs.add_argument(
        '--info_types', action='append',
        help='Strings representing info types to look for. A full list of '
             'info categories and types is available from the API. Examples '
             'include "US_MALE_NAME", "US_FEMALE_NAME", "EMAIL_ADDRESS", '
             '"CANADA_SOCIAL_INSURANCE_NUMBER", "JAPAN_PASSPORT". If omitted, '
             'the API will use a limited default set. Specify this flag '
             'multiple times to specify multiple info types.')
    parser_gcs.add_argument(
        '--min_likelihood',
        choices=['LIKELIHOOD_UNSPECIFIED', 'VERY_UNLIKELY', 'UNLIKELY',
                 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'],
        help='A string representing the minimum likelihood threshold that '
             'constitutes a match.')
    parser_gcs.add_argument(
        '--max_findings', type=int,
        help='The maximum number of findings to report; 0 = no maximum.')

    args = parser.parse_args()

    if args.content == 'string':
        inspect_string(
            args.item, info_types=args.info_types,
            min_likelihood=args.min_likelihood,
            include_quote=args.include_quote)
    elif args.content == 'file':
        inspect_file(
            args.filename, info_types=args.info_types,
            min_likelihood=args.min_likelihood,
            include_quote=args.include_quote,
            mime_type=args.mime_type)
    elif args.content == 'gcs':
        inspect_gcs_file(
            args.bucket, args.filename, info_types=args.info_types,
            min_likelihood=args.min_likelihood)
