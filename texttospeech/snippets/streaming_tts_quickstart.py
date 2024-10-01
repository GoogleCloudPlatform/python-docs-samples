#!/usr/bin/env python
# Copyright 2024 Google LLC
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
#

"""Google Cloud Text-To-Speech API streaming sample application .

Example usage:
    python streaming_tts_quickstart.py
"""


def run_streaming_tts_quickstart():
    """Synthesizes speech from a stream of input text.
    """
    from google.cloud import texttospeech
    import itertools

    client = texttospeech.TextToSpeechClient()

    # Set the config for your stream. The first request must contain your config, and then each subsequent request must contain text.
    streaming_config = texttospeech.StreamingSynthesizeConfig(voice=texttospeech.VoiceSelectionParams(name="en-US-Journey-D", language_code="en-US"))

    config_request = texttospeech.StreamingSynthesizeRequest(streaming_config=streaming_config)

    # Placeholder request generator. Consider using Gemini or another LLM with output streaming as a generator instead.
    def request_generator():
        for i in range(5):
            yield texttospeech.StreamingSynthesizeRequest(input="Test sentence. ")

    streaming_responses = client.streaming_synthesize(itertools.chain([config_request], request_generator()))
    for response in streaming_responses:
        # Just print the audio size. Replace with your logic to play audio. Note that audio_content is headerless LINEAR16 audio with a sample rate of 24000
        print("Audio content size in bytes is: " + len(response.audio_content))


if __name__ == "__main__":
    run_streaming_tts_quickstart()
