#!/usr/bin/env python

# Copyright 2020, Google LLC
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

import argparse


# [START speech_transcribe_onprem]
def transcribe_onprem(local_file_path, api_endpoint):
    """
    Transcribe a short audio file using synchronous speech recognition on-prem

    Args:
      local_file_path: The path to local audio file, e.g. /path/audio.wav
      api_endpoint: Endpoint to call for speech recognition, e.g. 0.0.0.0:10000
    """
    from google.cloud import speech_v1p1beta1
    from google.cloud.speech_v1p1beta1 import enums
    import grpc
    import io

    # api_endpoint = '0.0.0.0:10000'
    # local_file_path = '../resources/two_channel_16k.raw'

    # Create a gRPC channel to your server
    channel = grpc.insecure_channel(target=api_endpoint)

    client = speech_v1p1beta1.SpeechClient(channel=channel)

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "encoding": encoding,
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
# [END speech_transcribe_onprem]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--file_path",
        required=True,
        help="Path to local audio file to be recognized, e.g. /path/audio.wav",
    )
    parser.add_argument(
        "--api_endpoint",
        required=True,
        help="Endpoint to call for speech recognition, e.g. 0.0.0.0:10000",
    )

    args = parser.parse_args()
    transcribe_onprem(
        local_file_path=args.file_path, api_endpoint=args.api_endpoint
    )
