#!/usr/bin/env python

# Copyright 2021 Google LLC
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
"""Dialogflow API Python sample showing how to manage Participants.
"""

import google.auth
from google.cloud import dialogflow_v2beta1 as dialogflow

ROLES = ["HUMAN_AGENT", "AUTOMATED_AGENT", "END_USER"]


# [START dialogflow_create_participant]
def create_participant(project_id, conversation_id, role):
    """Creates a participant in a given conversation.

    Args:
        project_id: The GCP project linked with the conversation profile.
        conversation_id: Id of the conversation.
        participant: participant to be created."""

    client = dialogflow.ParticipantsClient()
    conversation_path = dialogflow.ConversationsClient.conversation_path(
        project_id, conversation_id
    )
    if role in ROLES:
        response = client.create_participant(
            parent=conversation_path, participant={"role": role}, timeout=600
        )
        print("Participant Created.")
        print("Role: {}".format(response.role))
        print("Name: {}".format(response.name))

        return response


# [END dialogflow_create_participant]


# [START dialogflow_analyze_content_text]
def analyze_content_text(project_id, conversation_id, participant_id, text):
    """Analyze text message content from a participant.

    Args:
        project_id: The GCP project linked with the conversation profile.
        conversation_id: Id of the conversation.
        participant_id: Id of the participant.
        text: the text message that participant typed."""

    client = dialogflow.ParticipantsClient()
    participant_path = client.participant_path(
        project_id, conversation_id, participant_id
    )
    text_input = {"text": text, "language_code": "en-US"}
    response = client.analyze_content(
        participant=participant_path, text_input=text_input
    )
    print("AnalyzeContent Response:")
    print("Reply Text: {}".format(response.reply_text))

    for suggestion_result in response.human_agent_suggestion_results:
        if suggestion_result.error is not None:
            print("Error: {}".format(suggestion_result.error.message))
        if suggestion_result.suggest_articles_response:
            for answer in suggestion_result.suggest_articles_response.article_answers:
                print("Article Suggestion Answer: {}".format(answer.title))
                print("Answer Record: {}".format(answer.answer_record))
        if suggestion_result.suggest_faq_answers_response:
            for answer in suggestion_result.suggest_faq_answers_response.faq_answers:
                print("Faq Answer: {}".format(answer.answer))
                print("Answer Record: {}".format(answer.answer_record))
        if suggestion_result.suggest_smart_replies_response:
            for (
                answer
            ) in suggestion_result.suggest_smart_replies_response.smart_reply_answers:
                print("Smart Reply: {}".format(answer.reply))
                print("Answer Record: {}".format(answer.answer_record))

    for suggestion_result in response.end_user_suggestion_results:
        if suggestion_result.error:
            print("Error: {}".format(suggestion_result.error.message))
        if suggestion_result.suggest_articles_response:
            for answer in suggestion_result.suggest_articles_response.article_answers:
                print("Article Suggestion Answer: {}".format(answer.title))
                print("Answer Record: {}".format(answer.answer_record))
        if suggestion_result.suggest_faq_answers_response:
            for answer in suggestion_result.suggest_faq_answers_response.faq_answers:
                print("Faq Answer: {}".format(answer.answer))
                print("Answer Record: {}".format(answer.answer_record))
        if suggestion_result.suggest_smart_replies_response:
            for (
                answer
            ) in suggestion_result.suggest_smart_replies_response.smart_reply_answers:
                print("Smart Reply: {}".format(answer.reply))
                print("Answer Record: {}".format(answer.answer_record))

    return response


# [END dialogflow_analyze_content_text]

# [START dialogflow_analyze_content_audio_stream]
def analyze_content_audio_stream(
    conversation_id, participant_id, audio_file_path
):
    """Analyze audio content for END_USER with audio files.

    Args:
        conversation_id: Id of the conversation.
        participant_id: Id of the participant.
        audio_file_path: audio file in wav/mp3 format contains utterances of END_USER."""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    credentials, project_id = google.auth.default()
    client = dialogflow.ParticipantsClient(credentials=credentials)

    participant_path = client.participant_path(
        project_id, conversation_id, participant_id
    )
    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    # Generates requests based on the audio files. Will by default use the first channel as
    # END_USER, and second channel as HUMAN_AGENT.
    def request_generator(audio_config, audio_file_path):

        # The first request contains the configuration.
        yield dialogflow.StreamingAnalyzeContentRequest(
            participant=participant_path, audio_config=audio_config
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
                yield dialogflow.StreamingAnalyzeContentRequest(input_audio=chunk)

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code="en-US",
        sample_rate_hertz=sample_rate_hertz,
        single_utterance=True,
        model="phone_call",
        # Make sure your project is Dialogflow ES ENTERPRISE_TIER in order to "USE_ENHANCED" model.
        model_variant="USE_ENHANCED",
    )
    requests = request_generator(audio_config, audio_file_path)
    responses = client.streaming_analyze_content(requests=requests)
    print("=" * 20)
    for response in responses:
        print(f'Transcript: "{response.message.content}".')

    print("=" * 20)


# [END dialogflow_analyze_content_audio_stream]


# [START dialogflow_streaming_analyze_content_audio]
def streaming_analyze_content_audio(participant_name,
                                    sample_rate_herz,
                                    stream,
                                    timeout,
                                    language_code,
                                    single_utterance=False):
    """Stream audio to Dialogflow and receive transcripts and suggestions.

    Args:
        participant_name: resource name of the participant.
        sample_rate_herz: herz rate of the sample.
        stream: the stream to process.
        timeout: the timeout of one stream.
        language_code: the language code of the audio
        single_utterance: whether to use single_utterance.
    """
    from google.cloud import dialogflow_v2beta1 as dialogflow_beta
    client = dialogflow_beta.ParticipantsClient()

    audio_config = dialogflow_beta.types.audio_config.InputAudioConfig(
        audio_encoding=dialogflow_beta.types.audio_config.AudioEncoding.
        AUDIO_ENCODING_LINEAR_16,
        sample_rate_hertz=sample_rate_herz,
        language_code=language_code,
        single_utterance=single_utterance)

    def gen_requests(participant_name, audio_config, stream):
        """Generates requests for streaming.
        """
        audio_generator = stream.generator()
        while not stream.closed:
            print("Yield config to streaming analyze content.")
            yield dialogflow_beta.types.participant.StreamingAnalyzeContentRequest(
                participant=participant_name,
                audio_config=audio_config)
            print("Yield audios to streaming analyze content.")
            for content in audio_generator:
                # print('Yield audio to streaming analyze content')
                yield dialogflow_beta.types.participant.StreamingAnalyzeContentRequest(
                    input_audio=content)

    return client.streaming_analyze_content(gen_requests(
        participant_name, audio_config, stream),
        timeout=timeout)


# [END dialogflow_streaming_analyze_content_audio]
