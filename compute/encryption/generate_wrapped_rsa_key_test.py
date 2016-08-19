# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import generate_wrapped_rsa_key


def test_main():
    generate_wrapped_rsa_key.main(None)


def test_create_disk(cloud_config):
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'beta', credentials=credentials)

    # Generate the key.
    key_bytes = os.urandom(32)
    google_public_key = generate_wrapped_rsa_key.get_google_public_cert_key()
    wrapped_rsa_key = generate_wrapped_rsa_key.wrap_rsa_key(
        google_public_key, key_bytes)

    # Create the disk, if the encryption key is invalid, this will raise.
    compute.disks().insert(
        project=cloud_config.project,
        zone='us-central1-f',
        body={
            'name': 'new-encrypted-disk',
            'diskEncryptionKey': {
                'rsaEncryptedKey': wrapped_rsa_key.decode('utf-8')
            }
        }).execute()

    # Delete the disk.
    compute.disks().delete(
        project=cloud_config.project,
        zone='us-central1-f',
        disk='new-encrypted-disk').execute()
