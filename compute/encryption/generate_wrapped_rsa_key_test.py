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
import uuid

import googleapiclient.discovery

import generate_wrapped_rsa_key

PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']


def test_main():
    generate_wrapped_rsa_key.main(None)


def test_create_disk():
    compute = googleapiclient.discovery.build('compute', 'beta')

    # Generate the key.
    key_bytes = os.urandom(32)
    google_public_key = generate_wrapped_rsa_key.get_google_public_cert_key()
    wrapped_rsa_key = generate_wrapped_rsa_key.wrap_rsa_key(
        google_public_key, key_bytes)
    disk_name = f'new-encrypted-disk-{uuid.uuid4().hex}'

    try:
        # Create the disk, if the encryption key is invalid, this will raise.
        compute.disks().insert(
            project=PROJECT,
            zone='us-central1-f',
            body={
                'name': disk_name,
                'diskEncryptionKey': {
                    'rsaEncryptedKey': wrapped_rsa_key.decode('utf-8')
                }
            }).execute()
    finally:
        # Delete the disk.
        compute.disks().delete(
            project=PROJECT,
            zone='us-central1-f',
            disk=disk_name).execute()
