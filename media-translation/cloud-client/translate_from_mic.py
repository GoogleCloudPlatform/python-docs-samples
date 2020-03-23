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

"""Cloud Media Translation API sample application using a microphone.

Example usage:
    python translate_from_mic.py
"""

# [START media_translation_translate_from_mic]
from __future__ import division

import itertools

from google.cloud import mediatranslation
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

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

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.
    """
    for response in responses:
        # Once the transcription settles, the response contains the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        result = response.result
        translation = result.text_translation_result.translation
        source = result.recognition_result

        if result.text_translation_result.is_final:
            print(u'\nFinal translation: {0}'.format(translation))
            print(u'Final recognition result: {0}'.format(source))
            break

        print(u'\nPartial translation: {0}'.format(translation))
        print(u'Partial recognition result: {0}'.format(source))


def main():
    client = mediatranslation.SpeechTranslationServiceClient()

    speech_config = mediatranslation.TranslateSpeechConfig(
        audio_encoding='linear16',
        source_language_code='en-US',
        target_language_code='es-ES')

    config = mediatranslation.StreamingTranslateSpeechConfig(
        audio_config=speech_config)

    # The first request contains the configuration.
    # Note that audio_content is explicitly set to None.
    first_request = mediatranslation.StreamingTranslateSpeechRequest(
        streaming_config=config, audio_content=None)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        mic_requests = (mediatranslation.StreamingTranslateSpeechRequest(
            audio_content=content,
            streaming_config=config)
            for content in audio_generator)

        requests = itertools.chain(iter([first_request]), mic_requests)

        responses = client.streaming_translate_speech(requests)

        # Print the translation responses as they arrive
        listen_print_loop(responses)


if __name__ == '__main__':
    print('Start speaking ...')
    main()
# [END media_translation_translate_from_mic]
