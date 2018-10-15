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

# [START dlp_inspect_text_file]
# Import the Google Cloud Data Loss Prevention library
import google.cloud.dlp


def inspect_image_file(project_id='YOUR_PROJECT_ID',
                       filepath='path/to/image.png'):
    # Instantiate a client
    dlp = google.cloud.dlp.DlpServiceClient()

    # Get the bytes of the file
    with open(filepath, mode='rb') as f:
        file_bytes = f.read()

    # Construct request
    parent = dlp.project_path(project_id)
    item = {'byte_item': {'type': 'IMAGE', 'data': file_bytes}}
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

    # Run request
    response = dlp.inspect_content(parent, inspect_config, item)

    # Print the results
    if response.result.findings:
        for finding in response.result.findings:
            print('Quote: {}'.format(finding.quote))
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END dlp_inspect_text_file]


if __name__ == '__main__':
    inspect_image_file(project_id=sys.argv[1], filepath=sys.argv[2])
