#!/usr/bin/env python

# Copyright 2019 Google LLC
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

"""Dialogflow API streams user input through the microphone and
speaks voice responses through the speaker.

Examples:
  python mic_stream_audio_response.py
"""

# [START dialogflow_microphone_streaming]

import dialogflow
import pyaudio
import simpleaudio as sa
import uuid
from dialogflow import enums

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)


def grab_intent(projectId, sessionId, languageCode):
    """Start stream from microphone input to dialogflow API"""

    session_client = dialogflow.SessionsClient()
    # Audio output stream

    final_request_received = False

    def __request_generator():
        input_stream = pyaudio.PyAudio().open(
            channels=1, rate=SAMPLE_RATE, format=pyaudio.paInt16, input=True)
        audio_encoding = enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        session_path = session_client.session_path(projectId, sessionId)
        print('Session path: {}\n'.format(session_path))

        input_audio_config = dialogflow.types.InputAudioConfig(
            audio_encoding=audio_encoding,
            language_code=languageCode,
            sample_rate_hertz=SAMPLE_RATE)
        speech_config = dialogflow.types.SynthesizeSpeechConfig(
            voice=dialogflow.types.VoiceSelectionParams(
                ssml_gender=enums.SsmlVoiceGender.SSML_VOICE_GENDER_FEMALE))
        output_audio_config = dialogflow.types.OutputAudioConfig(
            audio_encoding=enums.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16,
            sample_rate_hertz=SAMPLE_RATE,
            synthesize_speech_config=speech_config)
        query_input = dialogflow.types.QueryInput(
            audio_config=input_audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path,
            query_input=query_input,
            output_audio_config=output_audio_config)

        while True:
            if final_request_received:
                input_stream.close()
                return
            if input_stream.is_active():
                content = input_stream.read(
                    CHUNK_SIZE, exception_on_overflow=False)
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=content)

    while True:
        print('=' * 20)
        requests = __request_generator()
        responses = session_client.streaming_detect_intent(requests)

        for response in responses:
            print('Intermediate transcription result: {}'.format(
                response.recognition_result.transcript))
            if response.recognition_result.is_final:
                final_request_received = True
            if response.query_result.query_text:
                print('Fullfilment Text: {}'.format(
                    response.query_result.fulfillment_text))
                print('Intent: {}'.format(
                    response.query_result.intent.display_name))
            if response.output_audio:
                return response


def play_audio(audio):
    audio_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    audio_obj.wait_done()


def main(project_id, session_id, language_code):
    while(True):
        response = grab_intent(project_id, session_id, language_code)
        play_audio(response.output_audio)


if __name__ == "__main__":

    # TODO: developer uncomment and replace these variables with your own
    # project_id = 'helloworld-ceyxpf'
    # session_id = uuid.uuid4()
    # language_code = 'en-US'
    main(project_id, session_id, language_code)

# [END dialogflow_microphone_streaming]
