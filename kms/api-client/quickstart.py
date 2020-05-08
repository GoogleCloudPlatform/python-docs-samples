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

import os


def run_quickstart():
    # [START kms_quickstart]
    # Imports the Google APIs client library
    from google.cloud import kms_v1

    # Your Google Cloud Platform project ID
    project_id = 'YOUR_PROJECT_ID'
    # [END kms_quickstart]
    project_id = os.environ['GCLOUD_PROJECT']
    # [START kms_quickstart]

    # Lists keys in the "global" location.
    location = 'global'

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the location associated with the key rings.
    parent = client.location_path(project_id, location)

    # Lists key rings
    response = client.list_key_rings(parent)
    response_list = list(response)

    if len(response_list) > 0:
        print('Key rings:')
        for key_ring in response_list:
            print(key_ring.name)
    else:
        print('No key rings found.')
    # [END kms_quickstart]


if __name__ == '__main__':
    run_quickstart()
