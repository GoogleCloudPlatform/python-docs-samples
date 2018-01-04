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

"""Sample app that uses the Data Loss Prevent API to inspect a file."""

from __future__ import print_function

import argparse


# [START inspect_file]
def inspect_file(filename, info_types=None, min_likelihood=None,
                 max_findings=None, include_quote=True, mime_type=None):
    """Uses the Data Loss Prevention API to analyze a file for protected data.
    Args:
        filename: The path to the file to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API with
            the .list_root_categories(language_code) client method, and a list
            of types in a category with .list_info_types(category,
            language_code). Examples include 'US_MALE_NAME', 'US_FEMALE_NAME',
            'EMAIL_ADDRESS', 'CANADA_SOCIAL_INSURANCE_NUMBER', 'JAPAN_PASSPORT'.
            If info_types is omitted, the API will use a limited default set.
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

    # Prepare info_type by converting the list of strings into a list of
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

    # Construct the items list by reading the file as a binary string.
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('filename', help='The path to the file to inspect.')
    parser.add_argument('--info_types', action='append',
        help='Strings representing info types to look for. A full list of info '
             'categories and types is available from the API. Examples '
             'include "US_MALE_NAME", "US_FEMALE_NAME", "EMAIL_ADDRESS", '
             '"CANADA_SOCIAL_INSURANCE_NUMBER", "JAPAN_PASSPORT". If omitted, '
             'the API will use a limited default set. Specify this flag '
             'multiple times to specify multiple info types.')
    parser.add_argument('--min_likelihood',
        choices=['LIKELIHOOD_UNSPECIFIED', 'VERY_UNLIKELY', 'UNLIKELY',
                 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'],
        help='A string representing the minimum likelihood threshold that '
             'constitutes a match.')
    parser.add_argument('--max_findings', type=int,
        help='The maximum number of findings to report; 0 = no maximum.')
    parser.add_argument('--include_quote', type=bool,
        help='A boolean for whether to display a quote of the detected '
             'information in the results.')
    parser.add_argument('--mime_type',
        help='The MIME type of the file. If not specified, the type is '
             'inferred via the Python standard library\'s mimetypes module.')

    args = parser.parse_args()

    inspect_file(
        args.filename, info_types=args.info_types,
        min_likelihood=args.min_likelihood, include_quote=args.include_quote,
        mime_type=args.mime_type)
