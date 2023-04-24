# Copyright 2013 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START all]
"""Command-line sample application for composing objects using the Cloud
Storage API.

This sample is used on this page:

    https://cloud.google.com/storage/docs/json_api/v1/json-api-python-samples

For more information, see the README.md under /storage.

To run, create a least two sample files:
    $ echo "File 1" > file1.txt
    $ echo "File 2" > file2.txt

Example invocation:
    $ python compose_objects.py my-bucket destination.txt file1.txt file2.txt

"""

import argparse
import json

import googleapiclient.discovery


def main(bucket, destination, sources):
    # Construct the service object for the interacting with the Cloud Storage
    # API.
    service = googleapiclient.discovery.build('storage', 'v1')

    # Upload the source files.
    for filename in sources:
        req = service.objects().insert(
            media_body=filename,
            name=filename,
            bucket=bucket)
        resp = req.execute()
        print(f'> Uploaded source file {filename}')
        print(json.dumps(resp, indent=2))

    # Construct a request to compose the source files into the destination.
    compose_req_body = {
        'sourceObjects': [{'name': filename} for filename in sources],
        'destination': {
            'contentType': 'text/plain',    # required
        }
    }

    req = service.objects().compose(
        destinationBucket=bucket,
        destinationObject=destination,
        body=compose_req_body)

    resp = req.execute()

    print(f'> Composed files into {destination}')
    print(json.dumps(resp, indent=2))

    # Download and print the composed object.
    req = service.objects().get_media(
        bucket=bucket,
        object=destination)

    res = req.execute()

    print('> Composed file contents:')
    print(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket', help='Your Cloud Storage bucket.')
    parser.add_argument('destination', help='Destination file name.')
    parser.add_argument('sources', nargs='+', help='Source files to compose.')

    args = parser.parse_args()

    main(args.bucket, args.destination, args.sources)
# [END all]
