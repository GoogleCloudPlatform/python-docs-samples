#!/usr/bin/env python

# Copyright 2017 Google LLC
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

"""DialogFlow API Detect Intent Python sample with audio files processed
as an audio stream.

Examples:
  python detect_intent_stream.py -h
  python detect_intent_stream.py --project-id PROJECT_ID \
  --session-id SESSION_ID --audio-file-path resources/book_a_room.wav
  python detect_intent_stream.py --project-id PROJECT_ID \
  --session-id SESSION_ID --audio-file-path resources/mountain_view.wav
"""

import argparse
import uuid


# [START dialogflow_detect_intent_streaming]
def detect_intent_stream(project_id, session_id, audio_file_path, language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.StreamingDetectIntentRequest(
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
                yield dialogflow.StreamingDetectIntentRequest(input_audio=chunk)

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests=requests)

    print("=" * 20)
    for response in responses:
        print(
            'Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript
            )
        )
        # Note: Since Python gRPC doesn't have closeSend method, to stop processing the audio after result is recognized,
        # you may close the channel manually to prevent further iteration.
        # Keep in mind that if there is a silence chunk in the audio, part after it might be missed because of early teardown.
        # https://cloud.google.com/dialogflow/es/docs/how/detect-intent-stream#streaming_basics
        if response.recognition_result.is_final:
            session_client.transport.close()
            break

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print("=" * 20)
    print("Query text: {}".format(query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            query_result.intent.display_name, query_result.intent_detection_confidence
        )
    )
    print("Fulfillment text: {}\n".format(query_result.fulfillment_text))


# [END dialogflow_detect_intent_streaming]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--project-id", help="Project/agent id.  Required.", required=True
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
        args.project_id, args.session_id, args.audio_file_path, args.language_code
    )
