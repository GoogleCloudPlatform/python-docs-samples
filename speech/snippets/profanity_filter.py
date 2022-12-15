# Copyright 2020 Google LLC
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

""" Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""


# [START speech_recognize_with_profanity_filter_gcs]
def sync_recognize_with_profanity_filter_gcs(gcs_uri):

    from google.cloud import speech

    client = speech.SpeechClient()

    audio = {"uri": gcs_uri}

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        profanity_filter=True,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))


# [END speech_recognize_with_profanity_filter_gcs]

sync_recognize_with_profanity_filter_gcs(
    "gs://cloud-samples-tests/speech/brooklyn.flac"
)
