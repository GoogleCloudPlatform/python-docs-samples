#!/usr/bin/env python

# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command-line sample app demonstrating customer-supplied encryption keys.

This sample demonstrates uploading an object while supplying an encryption key,
and retrieving that object's contents using gcloud API.  The sample uses
the default credential and project.  To review their values, run this command:
    $ gcloud info

This sample is used on this page:
    https://cloud.google.com/storage/docs/encryption#customer-supplied

For more information, see the README.md under /storage.
"""

import argparse
import base64
import filecmp
import os
import tempfile

from gcloud import storage

# An AES256 encryption key.  It must be exactly 256 bits (32 bytes).  You can
# (and should) generate your own encryption key.  os.urandom(32) is a good way
# to accomplish this with Python.
#
# Although these keys are provided here for simplicity, please remember
# that it is a bad idea to store your encryption keys in your source code.
ENCRYPTION_KEY = os.urandom(32)


def upload_object(storage_client, bucket_name, filename, object_name,
                  encryption_key):
    """Uploads an object, specifying a custom encryption key.

    Args:
        storage_client: gcloud client to access cloud storage
        bucket_name: name of the destination bucket
        filename: name of file to be uploaded
        object_name: name of resulting object
        encryption_key: encryption key to encrypt the object,
                        either 32 raw bytes or a string of 32 bytes.
    """
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(filename, encryption_key=encryption_key)


def download_object(storage_client, bucket_name, object_name, filename,
                    encryption_key):
    """Downloads an object protected by a custom encryption key.

    Args:
        storage_client: gcloud client to access cloud storage
        bucket_name: name of the source bucket
        object_name: name of the object to be downloaded
        filename: name of the resulting file
        encryption_key: the encryption key that the object is encrypted by,
                        either 32 raw bytes or a string of 32 bytes.
    """
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(filename, encryption_key=encryption_key)


def main(bucket, filename):
    storage_client = storage.Client()
    print('Uploading object gs://{}/{} using encryption key (base64 formatted)'
          ' {}'.format(bucket, filename, base64.encodestring(ENCRYPTION_KEY)))
    upload_object(storage_client, bucket, filename, filename, ENCRYPTION_KEY)
    print('Downloading it back')
    with tempfile.NamedTemporaryFile(mode='w+b') as tmpfile:
        download_object(
            storage_client,
            bucket,
            object_name=filename,
            filename=tmpfile.name,
            encryption_key=ENCRYPTION_KEY)
        assert filecmp.cmp(filename, tmpfile.name), (
            'Downloaded file has different content from the original file.')
    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket', help='Your Cloud Storage bucket.')
    parser.add_argument('filename', help='A file to upload and download.')

    args = parser.parse_args()

    main(args.bucket, args.filename)
