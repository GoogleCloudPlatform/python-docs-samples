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

"""Sample app that uses the Data Loss Prevent API to inspect a string, a
local file or a file on Google Cloud Storage."""

from __future__ import print_function

import argparse

# [START redact_string]
def redact_string(item, replace_string, info_types=None, min_likelihood=None):
    """Uses the Data Loss Prevention API to redact protected data in a string.
    Args:
        item: The string to inspect.
        replace_string: The string to use to replace protected data; for
            instance, '***' or 'REDACTED'. An empty string is permitted.
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
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Prepare info_type by converting the list of strings into a list of
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
