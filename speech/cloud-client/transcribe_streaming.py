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

"""Google Cloud Speech API sample application using the streaming API.

Example usage:
    python transcribe_streaming.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    speech_client = speech.Client()

    with io.open(stream_file, 'rb') as audio_file:
        audio_sample = speech_client.sample(
            stream=audio_file,
            encoding=speech.encoding.Encoding.LINEAR16,
            sample_rate_hertz=16000)
        alternatives = audio_sample.streaming_recognize('en-US')

        for alternative in alternatives:
            print('Finished: {}'.format(alternative.is_final))
            print('Stability: {}'.format(alternative.stability))
            print('Transcript: {}'.format(alternative.confidence))
            print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    args = parser.parse_args()
    transcribe_streaming(args.stream)
