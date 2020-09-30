#!/usr/bin/env python

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

"""DialogFlow API Detect Intent Python sample with audio files processed as an audio stream.

Examples:
  python detect_intent_stream.py -h
  python detect_intent_stream.py --agent AGENT \
  --session-id SESSION_ID --audio-file-path resources/hello.wav
"""

import argparse
import uuid

from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import session


# [START dialogflow_detect_intent_stream]
def run_sample():
    # TODO(developer): Replace these values when running the function
    project_id = "YOUR-PROJECT-ID"
    location_id = "YOUR-LOCATION-ID"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "YOUR-AGENT-ID"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = uuid.uuid4()
    audio_file_path = "YOUR-AUDIO-FILE-PATH"
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"

    detect_intent_stream(agent, session_id, audio_file_path, language_code)


def detect_intent_stream(agent, session_id, audio_file_path, language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = SessionsClient()
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")

    input_audio_config = audio_config.InputAudioConfig(
        audio_encoding=audio_config.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
        sample_rate_hertz=24000,
    )

    def request_generator():
        audio_input = session.AudioInput(config=input_audio_config)
        query_input = session.QueryInput(audio=audio_input, language_code=language_code)

        # The first request contains the configuration.
        yield session.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input
        )

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, "rb") as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                audio_input = session.AudioInput(audio=chunk)
                query_input = session.QueryInput(audio=audio_input)
                yield session.StreamingDetectIntentRequest(query_input=query_input)

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


# [END dialogflow_detect_intent_stream]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--agent", help="Agent resource name.  Required.", required=True
    )
    parser.add_argument(
        "--session-id",
        help="Identifier of the DetectIntent session. " "Defaults to a random UUID.",
        default=str(uuid.uuid4()),
    )
    parser.add_argument(
        "--language-code",
        help='Language code of the query. Defaults to "en-US".',
        default="en-US",
    )
    parser.add_argument(
        "--audio-file-path", help="Path to the audio file.", required=True
    )

    args = parser.parse_args()

    detect_intent_stream(
        args.agent, args.session_id, args.audio_file_path, args.language_code
    )
