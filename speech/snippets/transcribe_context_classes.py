# Copyright 2020 Google LLC
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


def transcribe_context_classes(storage_uri):
    """Provides "hints" to the speech recognizer to
    favor specific classes of words in the results."""
    # [START speech_context_classes]
    from google.cloud import speech

    client = speech.SpeechClient()

    # storage_uri = 'gs://YOUR_BUCKET_ID/path/to/your/file.wav'
    audio = speech.RecognitionAudio(uri=storage_uri)

    # SpeechContext: to configure your speech_context see:
    # https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1#speechcontext
    # Full list of supported phrases (class tokens) here:
    # https://cloud.google.com/speech-to-text/docs/class-tokens
    speech_context = speech.SpeechContext(phrases=["$TIME"])

    # RecognitionConfig: to configure your encoding and sample_rate_hertz, see:
    # https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1#recognitionconfig
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        speech_contexts=[speech_context],
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))
    # [END speech_context_classes]
