# Copyright 2018 Google Inc.
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
import sys

# [START dlp_inspect_string]
# Import the Google Cloud Data Loss Prevention library
import google.cloud.dlp


def inspect_string(project_id='YOUR_PROJECT_ID'):
    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Construct the configuration
    inspect_config = {
        # The infoTypes of information to match
        'info_types': [
            {'name': 'PHONE_NUMBER'},
            {'name': 'EMAIL_ADDRESS'},
            {'name': 'CREDIT_CARD_NUMBER'},
        ],
        # Whether to include the matching string
        'include_quote': True,
    }

    # Construct the `item`
    item = {'value': 'My name is Gary Smith and my email is gary@example.com'}

    # Convert the project id into a full resource id
    parent = dlp.project_path(project_id)

    # Call the API
    response = dlp.inspect_content(parent, inspect_config, item)

    # Print out the results
    if response.result.findings:
        for finding in response.result.findings:
            print('Quote: {}'.format(finding.quote))
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END dlp_inspect_string]


if __name__ == '__main__':
    inspect_string(project_id=sys.argv[1])
