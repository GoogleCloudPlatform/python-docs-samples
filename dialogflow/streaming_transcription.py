# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Dialogflow API sample code using the StreamingAnalyzeContent
API.

Also please contact Google to get credentials of this project and set up the
credential file json locations by running:
export GOOGLE_APPLICATION_CREDENTIALS=<cred_json_file_location>

Example usage:
    export GOOGLE_CLOUD_PROJECT='cloud-contact-center-ext-demo'
    export CONVERSATION_PROFILE='FnuBYO8eTBWM8ep1i-eOng'
    export GOOGLE_APPLICATION_CREDENTIALS='/Users/ruogu/Desktop/keys/cloud-contact-center-ext-demo-78798f9f9254.json'
    python streaming_transcription.py

Then started to talk in English, you should see transcription shows up as you speak.

Say "Quit" or "Exit" to stop.
"""

import time
import re
import sys
import os

import conversation_management
import participant_management

import pyaudio
from six.moves import queue
from google.api_core import client_options
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import dialogflow_v2beta1 as dialogflow

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
CONVERSATION_PROFILE_ID = os.getenv('CONVERSATION_PROFILE')

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
RESTART_TIMEOUT = 160  # seconds
MAX_LOOKBACK = 3  # seconds

YELLOW = '\033[0;33m'


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        # Count the number of times the stream analyze content restarts.
        self.restart_counter = 0
        self.last_start_time = 0
        # Time end of the last is_final in millisec since last_start_time.
        self.is_final_offset = 0
        # Save the audio chunks generated from the start of the audio stream for
        # replay after restart.
        self.audio_input_chunks = []
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer in
        chunksize."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""
        # Handle restart.
        if not self.closed:
            total_processed_time = self.last_start_time + self.is_final_offset
            processed_bytes_length = int(
                total_processed_time * SAMPLE_RATE * 16 / 8) / 1000
            self.last_start_time = total_processed_time
            # Send out bytes stored in self.audio_input_chunks that is after the
            # processed_bytes_length.
            if (processed_bytes_length != 0):
                audio_bytes = b''.join(self.audio_input_chunks)
                # Lookback for unprocessed audio data.
                need_to_process_length = min(
                    int(len(audio_bytes) - processed_bytes_length),
                    int(MAX_LOOKBACK * SAMPLE_RATE * 16 / 8))
                # Note that you need to explicitly use `int` type for substring.
                need_to_process_bytes = audio_bytes[(-1)
                                                    * need_to_process_length:]
                yield need_to_process_bytes

        while not self.closed:
            data = []
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()

            if chunk is None:
                return
            data.append(chunk)
            # Now try to the rest of chunks if there are any left in the _buff.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)

                except queue.Empty:
                    break
            self.audio_input_chunks.extend(data)
            if data:
                yield b''.join(data)


def main():
    """start bidirectional streaming from microphone input to Dialogflow API"""
    # Create conversation.
    conversation = conversation_management.create_conversation(
        project_id=PROJECT_ID, conversation_profile_id=CONVERSATION_PROFILE_ID)

    conversation_id = conversation.name.split('conversations/')[1].rstrip()

    # Create end user participant.
    end_user = participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role='END_USER')

    mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
    print(mic_manager.chunk_size)
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening, say "Quit" or "Exit" to stop.\n\n')
    sys.stdout.write('End (ms)       Transcript Results/Status\n')
    sys.stdout.write('=====================================================\n')

    with mic_manager as stream:

        while not stream.closed:
            terminate = False
            while not terminate:
                try:
                    print("New Streaming Analyze Request: {}".format(
                        stream.restart_counter))
                    stream.restart_counter += 1
                    # Send request to streaming and get response.
                    responses = participant_management.streaming_analyze_content_audio(
                        participant_name=end_user.name,
                        sample_rate_herz=SAMPLE_RATE,
                        stream=stream,
                        timeout=RESTART_TIMEOUT,
                        language_code='en-US',
                        single_utterance=False)

                    # Now, put the transcription responses to user.
                    for response in responses:
                        # if response.human_agent_suggestion_results:
                        #     print(response)
                        if response.recognition_result.is_final:
                            print(response.recognition_result)
                            # offset return from recognition_result is relative
                            # to the beginning of audio stream.
                            offset = response.recognition_result.speech_end_offset
                            stream.is_final_offset = int(
                                offset.seconds * 1000 + offset.microseconds * 1000000)
                            transcript = response.recognition_result.transcript
                            # Exit recognition if any of the transcribed phrases could be
                            # one of our keywords.
                            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                                sys.stdout.write(YELLOW)
                                sys.stdout.write('Exiting...\n')
                                terminate = True
                                break
                except DeadlineExceeded:
                    print('Deadline Exceeded, restarting.')

            if terminate:
                conversation_management.complete_conversation(
                    project_id=PROJECT_ID, conversation_id=conversation_id)
                break


if __name__ == '__main__':

    main()
