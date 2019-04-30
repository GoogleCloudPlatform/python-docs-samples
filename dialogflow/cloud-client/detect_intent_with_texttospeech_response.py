#!/usr/bin/env python

# Copyright 2018 Google LLC
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

"""Dialogflow API Beta Detect Intent Python sample with an audio response.

Examples:
  python detect_intent_with_texttospeech_response_test.py -h
  python detect_intent_with_texttospeech_response_test.py \
  --project-id PROJECT_ID --session-id SESSION_ID "hello"
"""

import argparse
import uuid


# [START dialogflow_detect_intent_with_texttospeech_response]
def detect_intent_with_texttospeech_response(project_id, session_id, texts,
                                             language_code):
    """Returns the result of detect intent with texts as inputs and includes
    the response in an audio format.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2beta1 as dialogflow
    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        # Set the query parameters with sentiment analysis
        output_audio_config = dialogflow.types.OutputAudioConfig(
            audio_encoding=dialogflow.enums.OutputAudioEncoding
            .OUTPUT_AUDIO_ENCODING_LINEAR_16)

        response = session_client.detect_intent(
            session=session_path, query_input=query_input,
            output_audio_config=output_audio_config)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        # The response's audio_content is binary.
        with open('output.wav', 'wb') as out:
            out.write(response.output_audio)
            print('Audio content written to file "output.wav"')
# [END dialogflow_detect_intent_with_texttospeech_response]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id',
        help='Project/agent id.  Required.',
        required=True)
    parser.add_argument(
        '--session-id',
        help='Identifier of the DetectIntent session. '
             'Defaults to a random UUID.',
        default=str(uuid.uuid4()))
    parser.add_argument(
        '--language-code',
        help='Language code of the query. Defaults to "en-US".',
        default='en-US')
    parser.add_argument(
        'texts',
        nargs='+',
        type=str,
        help='Text inputs.')

    args = parser.parse_args()

    detect_intent_with_texttospeech_response(
        args.project_id, args.session_id, args.texts, args.language_code)
