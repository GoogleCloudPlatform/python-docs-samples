#!/usr/bin/python
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
"""Sample that transcribes a FLAC audio file stored in Google Cloud Storage,
using GRPC."""

import argparse

from google.cloud.credentials import get_credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from grpc.beta import implementations

# Keep the request alive for this many seconds
DEADLINE_SECS = 10
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


def make_channel(host, port):
    """Creates an SSL channel with auth credentials from the environment."""
    # In order to make an https call, use an ssl channel with defaults
    ssl_channel = implementations.ssl_channel_credentials(None, None, None)

    # Grab application default credentials from the environment
    creds = get_credentials().create_scoped([SPEECH_SCOPE])
    # Add a plugin to inject the creds into the header
    auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token)
    auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds')

    # compose the two together for both ssl and google auth
    composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)

    return implementations.secure_channel(host, port, composite_channel)


def main(input_uri, encoding, sample_rate):
    service = cloud_speech.beta_create_Speech_stub(
            make_channel('speech.googleapis.com', 443))
    # The method and parameters can be inferred from the proto from which the
    # grpc client lib was generated. See:
    # https://github.com/googleapis/googleapis/blob/master/google/cloud/speech/v1beta1/cloud_speech.proto
    response = service.SyncRecognize(cloud_speech.SyncRecognizeRequest(
        config=cloud_speech.RecognitionConfig(
            # There are a bunch of config options you can specify. See
            # https://goo.gl/KPZn97 for the full list.
            encoding=encoding,  # one of LINEAR16, FLAC, MULAW, AMR, AMR_WB
            sample_rate=sample_rate,  # the rate in hertz
            # See
            # https://g.co/cloud/speech/docs/best-practices#language_support
            # for a list of supported languages.
            language_code='en-US',  # a BCP-47 language tag
        ),
        audio=cloud_speech.RecognitionAudio(
            uri=input_uri,
        )
    ), DEADLINE_SECS)
    # Print the recognition results.
    print(response.results)


def _gcs_uri(text):
    if not text.startswith('gs://'):
        raise ValueError(
            'Cloud Storage uri must be of the form gs://bucket/path/')
    return text


PROTO_URL = ('https://github.com/googleapis/googleapis/blob/master/'
             'google/cloud/speech/v1beta1/cloud_speech.proto')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_uri', type=_gcs_uri)
    parser.add_argument(
        '--encoding', default='FLAC', choices=[
            'LINEAR16', 'FLAC', 'MULAW', 'AMR', 'AMR_WB'],
        help='How the audio file is encoded. See {}#L67'.format(PROTO_URL))
    parser.add_argument('--sample_rate', type=int, default=16000)

    args = parser.parse_args()
    main(args.input_uri, args.encoding, args.sample_rate)
