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

"""Dialogflow API Detect Knowledge Base Intent Python sample with text inputs.

Examples:
  python detect_intent_knowledge.py -h
  python detect_intent_knowledge.py --project-id PROJECT_ID \
  --session-id SESSION_ID --knowledge-base-id KNOWLEDGE_BASE_ID \
  "hello" "how do I reset my password?"
"""

import argparse
import uuid


# [START dialogflow_detect_intent_knowledge]
def detect_intent_knowledge(project_id, session_id, language_code,
                            knowledge_base_id, texts):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    import dialogflow_v2beta1 as dialogflow
    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        knowledge_base_path = dialogflow.knowledge_bases_client \
            .KnowledgeBasesClient \
            .knowledge_base_path(project_id, knowledge_base_id)

        query_params = dialogflow.types.QueryParameters(
            knowledge_base_names=[knowledge_base_path])

        response = session_client.detect_intent(
            session=session_path, query_input=query_input,
            query_params=query_params)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        print('Knowledge results:')
        knowledge_answers = response.query_result.knowledge_answers
        for answers in knowledge_answers.answers:
            print(' - Answer: {}'.format(answers.answer))
            print(' - Confidence: {}'.format(
                answers.match_confidence))
# [END dialogflow_detect_intent_knowledge]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id', help='Project/agent id.  Required.', required=True)
    parser.add_argument(
        '--session-id',
        help='ID of the DetectIntent session. '
             'Defaults to a random UUID.',
        default=str(uuid.uuid4()))
    parser.add_argument(
        '--language-code',
        help='Language code of the query. Defaults to "en-US".',
        default='en-US')
    parser.add_argument(
        '--knowledge-base-id',
        help='The id of the Knowledge Base to query against',
        required=True)
    parser.add_argument('texts', nargs='+', type=str, help='Text inputs.')

    args = parser.parse_args()

    detect_intent_knowledge(args.project_id, args.session_id,
                            args.language_code, args.knowledge_base_id,
                            args.texts)
