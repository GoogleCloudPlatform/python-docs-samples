#!/usr/bin/python
# Copyright (C) 2016 Google Inc.
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
"""Sample that streams audio to the Google Cloud Speech API via GRPC."""

import contextlib
import re
import threading

from gcloud.credentials import get_credentials
from google.cloud.speech.v1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations
import pyaudio

# Audio recording parameters
RATE = 16000
CHANNELS = 1
CHUNK = RATE // 10  # 100ms

# Keep the request alive for this many seconds
DEADLINE_SECS = 8 * 60 * 60
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


def make_channel(host, port):
    """Creates an SSL channel with auth credentials from the environment."""
    # In order to make an https call, use an ssl channel with defaults
    ssl_channel = implementations.ssl_channel_credentials(None, None, None)

    # Grab application default credentials from the environment
    creds = get_credentials().create_scoped([SPEECH_SCOPE])
    # Add a plugin to inject the creds into the header
    auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token)
    auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds')

    # compose the two together for both ssl and google auth
    composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)

    return implementations.secure_channel(host, port, composite_channel)


@contextlib.contextmanager
def record_audio(channels, rate, chunk):
    """Opens a recording stream in a context manager."""
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16, channels=channels, rate=rate,
        input=True, frames_per_buffer=chunk,
    )

    yield audio_stream

    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()


def request_stream(stop_audio, channels=CHANNELS, rate=RATE, chunk=CHUNK):
    """Yields `RecognizeRequest`s constructed from a recording audio stream.

    Args:
        stop_audio: A threading.Event object stops the recording when set.
        channels: How many audio channels to record.
        rate: The sampling rate.
        chunk: Buffer audio into chunks of this size before sending to the api.
    """
    with record_audio(channels, rate, chunk) as audio_stream:
        # The initial request must contain metadata about the stream, so the
        # server knows how to interpret it.
        metadata = cloud_speech.InitialRecognizeRequest(
            encoding='LINEAR16', sample_rate=rate,
            # Note that setting interim_results to True means that you'll
            # likely get multiple results for the same bit of audio, as the
            # system re-interprets audio in the context of subsequent audio.
            # However, this will give us quick results without having to tell
            # the server when to finalize a piece of audio.
            interim_results=True, continuous=False,
        )
        data = audio_stream.read(chunk)
        audio_request = cloud_speech.AudioRequest(content=data)

        yield cloud_speech.RecognizeRequest(
            initial_request=metadata,
            audio_request=audio_request)

        while not stop_audio.is_set():
            data = audio_stream.read(chunk)
            if not data:
                raise StopIteration()
            # Subsequent requests can all just have the content
            audio_request = cloud_speech.AudioRequest(content=data)

            yield cloud_speech.RecognizeRequest(audio_request=audio_request)


def listen_print_loop(recognize_stream):
    for resp in recognize_stream:
        if resp.error.code != code_pb2.OK:
            raise RuntimeError('Server error: ' + resp.error.message)

        # Display the transcriptions & their alternatives
        for result in resp.results:
            print(result.alternatives)

        # Exit recognition if any of the transcribed phrases could be
        # one of our keywords.
        if any(re.search(r'\b(exit|quit)\b', alt.transcript)
               for result in resp.results
               for alt in result.alternatives):
            print('Exiting..')
            return


def main():
    stop_audio = threading.Event()
    with cloud_speech.beta_create_Speech_stub(
            make_channel('speech.googleapis.com', 443)) as service:
        try:
            listen_print_loop(
                service.Recognize(request_stream(stop_audio), DEADLINE_SECS))
        finally:
            # Stop the request stream once we're done with the loop - otherwise
            # it'll keep going in the thread that the grpc lib makes for it..
            stop_audio.set()


if __name__ == '__main__':
    main()
