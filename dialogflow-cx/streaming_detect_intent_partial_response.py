# Copyright 2023 Google LLC
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


# [START dialogflow_cx_streaming_detect_intent_enable_partial_response]
import uuid

from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import audio_config
from google.cloud.dialogflowcx_v3.types import InputAudioConfig
from google.cloud.dialogflowcx_v3.types import session


def run_sample():
    """
    TODO(developer): Modify these variables before running the sample.
    """
    project_id = "YOUR-PROJECT-ID"
    location = "YOUR-LOCATION-ID"
    agent_id = "YOUR-AGENT-ID"
    audio_file_name = "YOUR-AUDIO-FILE-PATH"
    encoding = "AUDIO_ENCODING_LINEAR_16"
    sample_rate_hertz = 16000
    language_code = "en"

    streaming_detect_intent_partial_response(
        project_id,
        location,
        agent_id,
        audio_file_name,
        encoding,
        sample_rate_hertz,
        language_code,
    )


def streaming_detect_intent_partial_response(
    project_id,
    location,
    agent_id,
    audio_file_name,
    encoding,
    sample_rate_hertz,
    language_code,
):

    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())

    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )

    def request_generator():
        audio_encoding = audio_config.AudioEncoding[encoding]
        config = InputAudioConfig(
            audio_encoding=audio_encoding,
            sample_rate_hertz=sample_rate_hertz,
            single_utterance=True,
        )
        audio_input = session.AudioInput(config=config)
        query_input = session.QueryInput(audio=audio_input, language_code=language_code)
        yield session.StreamingDetectIntentRequest(
            session=session_path,
            query_input=query_input,
            enable_partial_response=True,
        )
        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_name, "rb") as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                audio_input = session.AudioInput(audio=chunk, config=config)
                query_input = session.QueryInput(
                    audio=audio_input, language_code=language_code
                )
                yield session.StreamingDetectIntentRequest(
                    session=session_path,
                    query_input=query_input,
                    enable_partial_response=True,
                )

    responses = session_client.streaming_detect_intent(requests=request_generator())

    print("=" * 20)
    for response in responses:
        print(f'Intermediate transcript: "{response.recognition_result.transcript}".')

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    response = response.detect_intent_response
    print(f"Query text: {response.query_result.transcript}")
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    print(f"Response text: {' '.join(response_messages)}\n")


# [END dialogflow_cx_streaming_detect_intent_enable_partial_response]


if __name__ == "__main__":
    run_sample()
