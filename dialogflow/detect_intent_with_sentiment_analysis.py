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

"""Dialogflow API Beta Detect Intent Python sample with sentiment analysis.

Examples:
  python detect_intent_with_sentiment_analysis.py -h
  python detect_intent_with_sentiment_analysis.py --project-id PROJECT_ID \
  --session-id SESSION_ID \
  "hello" "book a meeting room" "Mountain View"
"""

import argparse
import uuid


# [START dialogflow_detect_intent_with_sentiment_analysis]
def detect_intent_with_sentiment_analysis(project_id, session_id, texts,
                                          language_code):
    """Returns the result of detect intent with texts as inputs and analyzes the
    sentiment of the query text.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        # Enable sentiment analysis
        sentiment_config = dialogflow.SentimentAnalysisRequestConfig(
            analyze_query_text_sentiment=True)

        # Set the query parameters with sentiment analysis
        query_params = dialogflow.QueryParameters(
            sentiment_analysis_request_config=sentiment_config)

        response = session_client.detect_intent(
            request={'session': session_path, 'query_input': query_input, 'query_params': query_params})

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        # Score between -1.0 (negative sentiment) and 1.0 (positive sentiment).
        print('Query Text Sentiment Score: {}\n'.format(
            response.query_result.sentiment_analysis_result
            .query_text_sentiment.score))
        print('Query Text Sentiment Magnitude: {}\n'.format(
            response.query_result.sentiment_analysis_result
            .query_text_sentiment.magnitude))
# [END dialogflow_detect_intent_with_sentiment_analysis]


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

    detect_intent_with_sentiment_analysis(
        args.project_id, args.session_id, args.texts, args.language_code)
