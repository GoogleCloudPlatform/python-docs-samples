#!/usr/bin/env python

# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Application for uploading an object using the Cloud Storage API.

This sample is used on this page:

    https://cloud.google.com/storage/docs/json_api/v1/json-api-python-samples

For more information, see the README.md under /storage.
"""

import argparse
import json
import tempfile

import googleapiclient.discovery
import googleapiclient.http


def main(bucket, filename, readers=[], owners=[]):
    print('Uploading object..')
    resp = upload_object(bucket, filename, readers, owners)
    print(json.dumps(resp, indent=2))

    print('Fetching object..')
    with tempfile.TemporaryFile(mode='w+b') as tmpfile:
        get_object(bucket, filename, out_file=tmpfile)

    print('Deleting object..')
    resp = delete_object(bucket, filename)
    if resp:
        print(json.dumps(resp, indent=2))
    print('Done')


def create_service():
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # You can browse other available api services and versions here:
    #     http://g.co/dv/api-client-library/python/apis/
    return googleapiclient.discovery.build('storage', 'v1')


def upload_object(bucket, filename, readers, owners):
    service = create_service()

    # This is the request body as specified:
    # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
    body = {
        'name': filename,
    }

    # If specified, create the access control objects and add them to the
    # request body
    if readers or owners:
        body['acl'] = []

    for r in readers:
        body['acl'].append({
            'entity': 'user-%s' % r,
            'role': 'READER',
            'email': r
        })
    for o in owners:
        body['acl'].append({
            'entity': 'user-%s' % o,
            'role': 'OWNER',
            'email': o
        })

    # Now insert them into the specified bucket as a media insertion.
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert
    with open(filename, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket, body=body,
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            media_body=googleapiclient.http.MediaIoBaseUpload(
                f, 'application/octet-stream'))
        resp = req.execute()

    return resp


def get_object(bucket, filename, out_file):
    service = create_service()

    # Use get_media instead of get to get the actual contents of the object.
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
    req = service.objects().get_media(bucket=bucket, object=filename)

    downloader = googleapiclient.http.MediaIoBaseDownload(out_file, req)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    return out_file


def delete_object(bucket, filename):
    service = create_service()

    req = service.objects().delete(bucket=bucket, object=filename)
    resp = req.execute()

    return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='The name of the file to upload')
    parser.add_argument('bucket', help='Your Cloud Storage bucket.')
    parser.add_argument('--reader', action='append', default=[],
                        help='Your Cloud Storage bucket.')
    parser.add_argument('--owner', action='append', default=[],
                        help='Your Cloud Storage bucket.')

    args = parser.parse_args()

    main(args.bucket, args.filename, args.reader, args.owner)
