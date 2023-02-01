#!/usr/bin/env python

# Copyright 2020-2022 Google LLC
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

# Detects intent and returns a synthesized Text-to-Speech (TTS) response

# [START dialogflow_cx_v3_detect_intent_synthesize_tts_response_async]
import uuid

from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import audio_config
from google.cloud.dialogflowcx_v3.types import session


def run_sample():
    # TODO(developer): Update these values when running the function
    project_id = "YOUR-PROJECT-ID"
    location = "YOUR-LOCATION-ID"
    agent_id = "YOUR-AGENT-ID"
    text = "YOUR-TEXT"
    audio_encoding = "YOUR-AUDIO-ENCODING"
    language_code = "YOUR-LANGUAGE-CODE"
    output_file = "YOUR-OUTPUT-FILE"

    detect_intent_synthesize_tts_response(
        project_id,
        location,
        agent_id,
        text,
        audio_encoding,
        language_code,
        output_file,
    )


def detect_intent_synthesize_tts_response(
    project_id,
    location,
    agent_id,
    text,
    audio_encoding,
    language_code,
    output_file,
):
    """Returns the result of detect intent with synthesized response."""
    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())

    # Constructs the audio query request
    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )
    text_input = session.TextInput(text=text)
    query_input = session.QueryInput(text=text_input, language_code=language_code)
    synthesize_speech_config = audio_config.SynthesizeSpeechConfig(
        speaking_rate=1.25,
        pitch=10.0,
    )
    output_audio_config = audio_config.OutputAudioConfig(
        synthesize_speech_config=synthesize_speech_config,
        audio_encoding=audio_config.OutputAudioEncoding[audio_encoding],
    )
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
        output_audio_config=output_audio_config,
    )

    response = session_client.detect_intent(request=request)
    print(
        "Speaking Rate: "
        f"{response.output_audio_config.synthesize_speech_config.speaking_rate}"
    )
    print("Pitch: " f"{response.output_audio_config.synthesize_speech_config.pitch}")
    with open(output_file, "wb") as fout:
        fout.write(response.output_audio)
    print(f"Audio content written to file: {output_file}")


# [END dialogflow_cx_v3_detect_intent_synthesize_tts_response_async]


if __name__ == "__main__":
    run_sample()
