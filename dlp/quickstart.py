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


def quickstart():
    """Demonstrates use of the Data Loss Prevention API client library."""

    # [START quickstart]
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # The string to inspect
    content = 'Robert Frost'

    # Construct the list of content items to inspect; in this case, only one.
    items = [{'type': 'text/plain', 'value': content}]

    # The info types to search for in the content.
    info_types = [{'name': 'US_MALE_NAME'}, {'name': 'US_FEMALE_NAME'}]

    # The minimum likelihood to constitute a match. Optional.
    min_likelihood = 'LIKELIHOOD_UNSPECIFIED'

    # The maximum number of findings to report (0 = server maximum). Optional.
    max_findings = 0

    # Whether to include the matching string in the results. Optional.
    include_quote = True

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'max_findings': max_findings,
        'include_quote': include_quote,
    }

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
    # [END quickstart]


if __name__ == '__main__':
    quickstart()
