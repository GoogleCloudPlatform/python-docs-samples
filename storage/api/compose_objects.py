# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
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
# [START all]
"""Command-line sample application for composing objects using the Cloud
Storage API.

Before running, authenticate with the Google Cloud SDK by running:
    $ gcloud auth login

Create a least two sample files:
    $ echo "File 1" > file1.txt
    $ echo "File 2" > file2.txt

Example invocation:
    $ python compose_objects.py my-bucket destination.txt file1.txt file2.txt

Usage:
    $ python compose_objects.py <your-bucket> <destination-file-name> \
<source-1> [... <source-n>]

You can also get help on all the command-line flags the program understands
by running:
    $ python compose-sample.py --help

"""

import argparse
import json
import sys

from apiclient import discovery
from oauth2client.client import GoogleCredentials

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('bucket')
parser.add_argument('destination', help='Destination file name')
parser.add_argument('sources', nargs='+', help='Source files to compose')


def main(argv):
    # Parse the command-line flags.
    args = parser.parse_args(argv[1:])

    # Get the application default credentials. When running locally, these are
    # available after running `gcloud auth login`. When running on compute
    # engine, these are available from the environment.
    credentials = GoogleCredentials.get_application_default()

    # Construct the service object for the interacting with the Cloud Storage
    # API.
    service = discovery.build('storage', 'v1', credentials=credentials)

    # Upload the source files.
    for filename in args.sources:
        req = service.objects().insert(
            media_body=filename,
            name=filename,
            bucket=args.bucket)
        resp = req.execute()
        print('> Uploaded source file {}'.format(filename))
        print(json.dumps(resp, indent=2))

    # Construct a request to compose the source files into the destination.
    compose_req_body = {
        'sourceObjects': [{'name': filename} for filename in args.sources],
        'destination': {
            'contentType': 'text/plain',    # required
        }
    }
    req = service.objects().compose(
        destinationBucket=args.bucket,
        destinationObject=args.destination,
        body=compose_req_body)
    resp = req.execute()
    print('> Composed files into {}'.format(args.destination))
    print(json.dumps(resp, indent=2))

    # Download and print the composed object.
    req = service.objects().get_media(
        bucket=args.bucket,
        object=args.destination)

    res = req.execute()
    print('> Composed file contents:')
    print(res)


if __name__ == '__main__':
    main(sys.argv)
# [END all]
