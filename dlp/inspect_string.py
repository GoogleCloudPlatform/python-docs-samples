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

from __future__ import print_function


# [START inspect_string]
def inspect_string(item, info_types=None, min_likelihood=None,
                   max_findings=None, include_quote=True):
    """Uses the Data Loss Prevention API to analyze a string for protected data.
    Args:
        item: The string to inspect.
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


if __name__ == '__main__':
    inspect_string("I'm Gary and my email is gary@example.com", ["EMAIL_ADDRESS", "US_MALE_NAME", "US_FEMALE_NAME"])
    # DO NOT SUBMIT