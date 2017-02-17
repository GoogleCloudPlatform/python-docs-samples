#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Google Cloud Speech API sample application using the REST API for async
batch processing.

Example usage: python transcribe.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import base64
import json
import time

import googleapiclient.discovery
# [END import_libraries]


# [START authenticating]


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    return googleapiclient.discovery.build('speech', 'v1beta1')
# [END authenticating]


def main(speech_file):
    """Transcribe the given audio file asynchronously.

    Args:
        speech_file: the name of the audio file.
    """
    # [START construct_request]
    with open(speech_file, 'rb') as speech:
        # Base64 encode the binary audio file for inclusion in the request.
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().asyncrecognize(
        body={
            'config': {
                # There are a bunch of config options you can specify. See
                # https://goo.gl/KPZn97 for the full list.
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                # See http://g.co/cloud/speech/docs/languages for a list of
                # supported languages.
                'languageCode': 'en-US',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    # [END construct_request]
    # [START send_request]
    response = service_request.execute()
    print(json.dumps(response))
    # [END send_request]

    name = response['name']
    # Construct a GetOperation request.
    service_request = service.operations().get(name=name)

    while True:
        # Give the server a few seconds to process.
        print('Waiting for server processing...')
        time.sleep(1)
        # Get the long running operation with response.
        response = service_request.execute()

        if 'done' in response and response['done']:
            break

    # First print the raw json response
    print(json.dumps(response['response'], indent=2))

    # Now print the actual transcriptions
    for result in response['response'].get('results', []):
        print('Result:')
        for alternative in result['alternatives']:
            print(u'  Alternative: {}'.format(alternative['transcript']))


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(args.speech_file)
    # [END run_application]
