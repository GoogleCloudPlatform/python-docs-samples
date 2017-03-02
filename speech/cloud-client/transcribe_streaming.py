#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample application for transcribing audio streams

Example usage:
    python transcribe_stream resources/audio.raw
 
sources:
 * https://googlecloudplatform.github.io/google-cloud-python/stable/speech-usage.html#streaming-recognition

"""

# [START import_libraries]
import logging
from google.cloud import speech
# [END import_libraries]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SAMPLE_RATE=16000
speech_client = speech.Client()

def transcribe_stream(stream):
    logging.debug('{} is closed: {}'.format(str(stream), stream.closed))

    sample = speech_client.sample(stream=stream,
                                    encoding=speech.Encoding.LINEAR16,
                                    sample_rate=SAMPLE_RATE)
    results = list(sample.streaming_recognize())
    print('results len:{}'.format(len(results)))
    for result in results:
        for alternative in result.alternatives:
            print(str(alternative.confidence)+' '+str(alternative.transcript))

def main(args):
    with open(args.filename, 'rb') as stream:
        transcribe_stream( stream )

def parse_args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename', type=str)
    args = p.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)

