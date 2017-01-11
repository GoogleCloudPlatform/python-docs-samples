#!/usr/bin/env python

# Copyright 2017 Google, Inc
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


def run_quickstart():
    # [START kms_quickstart]
    # Imports the Google APIs client library
    from googleapiclient import discovery

    # Your Google Cloud Platform project ID
    project_id = 'YOUR_PROJECT_ID'

    # The "global" zone lists all keys. It can be a specific zone if desired.
    zone = 'global'

    # Instantiates a client
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the location associated with the KeyRings
    parent = 'projects/{}/locations/{}'.format(project_id, zone)

    # Lists key rings
    request = kms_client.projects().locations().keyRings().list(parent=parent)
    response = request.execute()

    if 'key_rings' in response and len(response['key_rings']):
        print('Key rings:')
        for key_ring in response['key_rings']:
            print(key_ring['name'])
    else:
        print('No key rings found.')
    # [END kms_quickstart]


if __name__ == '__main__':
    run_quickstart()
