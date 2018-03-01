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

"""Sample app that queries the Data Loss Prevention API for supported
categories and info types."""

from __future__ import print_function

import argparse


# [START list_info_types]
def list_info_types(category, language_code='en-US'):
    """List types of sensitive information within a category.
    Args:
        category: The category of info types to list; e.g. 'PII'.
        language_code: The BCP-47 language code to use, e.g. 'en-US'.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Make the API call.
    response = dlp.list_info_types(category, language_code)

    # Print the results to the console.
    print('Info types in {category}:'.format(category=category))
    for info_type in response.info_types:
        print('{name}: {display_name}'.format(
            name=info_type.name, display_name=info_type.display_name))
# [END list_info_types]


# [START list_categories]
def list_categories(language_code='en-US'):
    """List root categories of sensitive information.
    Args:
        language_code: The BCP-47 language code to use, e.g. 'en-US'.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Make the API call.
    response = dlp.list_root_categories(language_code)

    # Print the results to the console.
    print('Categories:')
    for category in response.categories:
        print('{name}: {display_name}'.format(
            name=category.name, display_name=category.display_name))
# [END list_categories]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest='metadata', help='Select which type of metadata to view.')

    parser_categories = subparsers.add_parser(
        'categories', help='Fetch the list of info type categories.')
    parser_categories.add_argument(
        '--language_code',
        help='The BCP-47 language code to use, e.g. \'en-US\'.')

    parser_info_types = subparsers.add_parser(
        'info_types',
        help='Fetch the list of info types in a specified category.')
    parser_info_types.add_argument(
        'category', help='The category of info types to list; e.g. \'PII\'.')
    parser_info_types.add_argument(
        '--language_code',
        help='The BCP-47 language code to use, e.g. \'en-US\'.')

    args = parser.parse_args()

    if args.metadata == 'categories':
        list_categories(language_code=args.language_code)
    elif args.metadata == 'info_types':
        list_info_types(args.category, language_code=args.language_code)
