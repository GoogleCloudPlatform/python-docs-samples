# Copyright 2023 Google LLC
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

"""Command-line sample app demonstrating customer-supplied encryption keys.

This sample demonstrates uploading an object while supplying an encryption key,
retrieving that object's contents, and finally rotating that key to a new
value.

This sample is used on this page:

    https://cloud.google.com/storage/docs/json_api/v1/json-api-python-samples

For more information, see the README.md under /storage.
"""

import argparse
import filecmp
import tempfile

import googleapiclient.discovery
import googleapiclient.http


# You can (and should) generate your own encryption key. Here's a good way to
# accomplish this with Python:
#   python -c \
#     'import base64; import os; print(base64.encodestring(os.urandom(32)))'
# Although these keys are provided here for simplicity, please remember that it
# is a bad idea to store your encryption keys in your source code.
ENCRYPTION_KEY = '4RzDI0TeWa9M/nAvYH05qbCskPaSU/CFV5HeCxk0IUA='

# You can use openssl to quickly calculate the hash of any key.
# Try running this:
#   openssl base64 -d <<< ENCRYPTION_KEY | openssl dgst -sha256 -binary \
#     | openssl base64
KEY_HASH = 'aanjNC2nwso8e2FqcWILC3/Tt1YumvIwEj34kr6PRpI='

ANOTHER_ENCRYPTION_KEY = 'oevtavYZC+TfGtV86kJBKTeytXAm1s2r3xIqam+QPKM='
ANOTHER_KEY_HASH = '/gd0N3k3MK0SEDxnUiaswl0FFv6+5PHpo+5KD5SBCeA='


def create_service() -> googleapiclient.discovery.Resource:
    """Creates the service object for calling the Cloud Storage API."""
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # You can browse other available api services and versions here:
    #     https://developers.google.com/api-client-library/python/apis/
    return googleapiclient.discovery.build('storage', 'v1')


def upload_object(
        bucket: str,
        filename: str,
        encryption_key: str,
        key_hash: str,
) -> googleapiclient.http.HttpRequest:
    """Uploads an object, specifying a custom encryption key.
    
    Args:
        bucket: The name of the bucket to upload to.
        filename: The name of the file to upload.
        encryption_key: The encryption key to use for the upload.
        key_hash: The hash of the encryption key
    
    Returns:
        The http request object.
    """
    service = create_service()

    with open(filename, 'rb') as f:
        request = service.objects().insert(
            bucket=bucket, name=filename,
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            media_body=googleapiclient.http.MediaIoBaseUpload(
                f, 'application/octet-stream'))
        request.headers['x-goog-encryption-algorithm'] = 'AES256'
        request.headers['x-goog-encryption-key'] = encryption_key
        request.headers['x-goog-encryption-key-sha256'] = key_hash

        resp = request.execute()

    return resp


def download_object(
        bucket: str,
        obj: str,
        out_file: str,
        encryption_key: str,
        key_hash: str,
) -> googleapiclient.http.HttpRequest:
    """Downloads an object protected by a custom encryption key.

    Args:
        bucket: The name of the bucket to download from.
        obj: The name of the object to download.
        filename: The name of the file to download to.
        encryption_key: The encryption key to use for the download
        key_hash: The hash of the encryption key

    Returns:
        The http request object.
    """
    service = create_service()

    request = service.objects().get_media(bucket=bucket, object=obj)
    request.headers['x-goog-encryption-algorithm'] = 'AES256'
    request.headers['x-goog-encryption-key'] = encryption_key
    request.headers['x-goog-encryption-key-sha256'] = key_hash

    # Unfortunately, http.MediaIoBaseDownload overwrites HTTP headers,
    # and so it cannot be used here. Instead, we shall download as a
    # single request.
    out_file.write(request.execute())


def rotate_key(
        bucket: str,
        obj: str,
        current_encryption_key: str,
        current_key_hash: str,
        new_encryption_key: str,
        new_key_hash: str,
) -> googleapiclient.http.HttpRequest:
    """Changes the encryption key used to store an existing object.

    Args:
        bucket: The name of the bucket to upload to.
        obj: The name of the object to upload.
        current_encryption_key: The current encryption key to use for the upload.
        current_key_hash: The current hash of the encryption key
        new_encryption_key: The new encryption key to use for the upload.
        new_key_hash: The new hash of the encryption key

    Returns:
        The http request object.
    """
    service = create_service()

    request = service.objects().rewrite(
            sourceBucket=bucket, sourceObject=obj,
            destinationBucket=bucket, destinationObject=obj,
            body={})

    # For very large objects, calls to rewrite may not complete on the first
    # call and may need to be resumed.
    while True:
        request.headers.update({
            'x-goog-copy-source-encryption-algorithm': 'AES256',
            'x-goog-copy-source-encryption-key': current_encryption_key,
            'x-goog-copy-source-encryption-key-sha256': current_key_hash,
            'x-goog-encryption-algorithm': 'AES256',
            'x-goog-encryption-key': new_encryption_key,
            'x-goog-encryption-key-sha256': new_key_hash})

        rewrite_response = request.execute()

        if rewrite_response['done']:
            break

        print('Continuing rewrite call...')
        request = service.objects().rewrite(
                source_bucket=bucket, source_object=obj,
                destination_bucket=bucket, destination_object=obj,
                rewriteToken=rewrite_response['rewriteToken'])
        rewrite_response.execute()


def main(
        bucket: str,
        filename: str,
) -> None:
    """Main method to upload and download objects.

    Args:
        bucket: The name of the bucket to upload to.
        filename: The name of the file to upload.

    Returns:
        None.
    """
    print(f'Uploading object gs://{bucket}/{filename}')
    upload_object(bucket, filename, ENCRYPTION_KEY, KEY_HASH)
    print('Downloading it back')
    with tempfile.NamedTemporaryFile(mode='w+b') as tmpfile:
        download_object(bucket, filename, tmpfile, ENCRYPTION_KEY, KEY_HASH)
        tmpfile.seek(0)
        assert filecmp.cmp(filename, tmpfile.name), \
            'Downloaded file has different content from the original file.'
    print('Rotating its key')
    rotate_key(bucket, filename, ENCRYPTION_KEY, KEY_HASH,
               ANOTHER_ENCRYPTION_KEY, ANOTHER_KEY_HASH)
    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket', help='Your Cloud Storage bucket.')
    parser.add_argument('filename', help='A file to upload and download.')

    args = parser.parse_args()

    main(args.bucket, args.filename)
