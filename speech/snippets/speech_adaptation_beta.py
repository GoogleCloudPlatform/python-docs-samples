# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DO NOT EDIT! This is a generated sample ("Request",  "speech_adaptation_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Speech Adaptation (Cloud Storage)
#   description: Transcribe a short audio file with speech adaptation.

from google.cloud import speech_v1p1beta1


def sample_recognize() -> speech_v1p1beta1.RecognizeResponse:
    """
    Transcribe a short audio file with speech adaptation.
    """
    # [START speech_adaptation_beta]
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()
    # Replace with the URI of your audio file in Google Cloud Storage
    audio_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.mp3"
    # Define the audio source
    audio = {"uri": audio_uri}

    phrase = "Brooklyn Bridge"
    phrases = [phrase]

    # Hint Boost. This value increases the probability that a specific
    # phrase will be recognized over other similar sounding phrases.
    # The higher the boost, the higher the chance of false positive
    # recognition as well. Can accept wide range of positive values.
    # Most use cases are best served with values between 0 and 20.
    # Using a binary search approach may help you find the optimal value.
    boost = 20.0
    speech_contexts_element = {"phrases": phrases, "boost": boost}
    speech_contexts = [speech_contexts_element]

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats
    encoding = speech.RecognitionConfig.AudioEncoding.MP3
    config = speech.RecognitionConfig(
        {
            "speech_contexts": speech_contexts,
            "sample_rate_hertz": sample_rate_hertz,
            "language_code": language_code,
            "encoding": encoding,
        }
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")

    # [END speech_adaptation_beta]
    return response


if __name__ == "__main__":
    sample_recognize()
