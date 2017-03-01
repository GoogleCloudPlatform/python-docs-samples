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

"""Sample that streams audio to the Google Cloud Speech API via GRPC.

This sample expands on transcribe_streaming.py to work around the 1-minute
limit on streaming requests. It does this by transcribing normally until
WRAP_IT_UP_SECS seconds before the 1-minute limit. At that point, it waits for
the end of an utterance and once it hears it, it closes the current stream and
opens a new one. It also keeps a buffer of audio around while this is
happening, that it sends to the new stream in its initial request, to minimize
losing any speech that occurs while this happens.

Note that you could do this a little more simply by simply re-starting the
stream after every utterance, though this increases the possibility of audio
being missed between streams. For learning purposes (and robustness), the more
complex implementation is shown here.
"""

from __future__ import division

import argparse
import collections
import contextlib
import functools
import logging
import re
import signal
import sys
import time

import google.auth
import google.auth.transport.grpc
import google.auth.transport.requests
from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2
from google.rpc import code_pb2
import grpc
import pyaudio
from six.moves import queue

# Seconds you have to wrap up your utterance
WRAP_IT_UP_SECS = 15
SECS_OVERLAP = 1

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# The Speech API has a streaming limit of 60 seconds of audio*, so keep the
# connection alive for that long, plus some more to give the API time to figure
# out the transcription.
# * https://g.co/cloud/speech/limits#content
DEADLINE_SECS = 60 * 3 + 5
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


def make_channel(host):
    """Creates a secure channel with auth credentials from the environment."""
    # Grab application default credentials from the environment
    credentials, _ = google.auth.default(scopes=[SPEECH_SCOPE])

    # Create a secure channel using the credentials.
    http_request = google.auth.transport.requests.Request()

    return google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, host)


def _audio_data_generator(buff, overlap_buffer):
    """A generator that yields all available data in the given buffer.

    Args:
        buff (Queue): A Queue where each element is a chunk of data.
        overlap_buffer (deque): a ring buffer for storing trailing data chunks
    Yields:
        bytes: A chunk of data that is the aggregate of all chunks of data in
        `buff`. The function will block until at least one data chunk is
        available.
    """
    if overlap_buffer:
        yield b''.join(overlap_buffer)
        overlap_buffer.clear()

    while True:
        # Use a blocking get() to ensure there's at least one chunk of data.
        data = [buff.get()]

        # Now consume whatever other data's still buffered.
        while True:
            try:
                data.append(buff.get(block=False))
            except queue.Empty:
                break

        # `None` in the buffer signals that we should stop generating. Put the
        # data back into the buffer for the next generator.
        if None in data:
            data.remove(None)
            if data:
                buff.put(b''.join(data))
            break
        else:
            overlap_buffer.extend(data)

        yield b''.join(data)


def _fill_buffer(buff, in_data, frame_count, time_info, status_flags):
    """Continuously collect data from the audio stream, into the buffer."""
    buff.put(in_data)
    return None, pyaudio.paContinue


# [START audio_stream]
@contextlib.contextmanager
def record_audio(rate, chunk):
    """Opens a recording stream in a context manager."""
    # Create a thread-safe buffer of audio data
    buff = queue.Queue()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        # The API currently only supports 1-channel (mono) audio
        # https://goo.gl/z757pE
        channels=1, rate=rate,
        input=True, frames_per_buffer=chunk,
        # Run the audio stream asynchronously to fill the buffer object.
        # This is necessary so that the input device's buffer doesn't overflow
        # while the calling thread makes network requests, etc.
        stream_callback=functools.partial(_fill_buffer, buff),
    )

    yield buff

    audio_stream.stop_stream()
    audio_stream.close()
    # Signal the _audio_data_generator to finish
    buff.put(None)
    audio_interface.terminate()
# [END audio_stream]


def request_stream(data_stream, rate, interim_results=True):
    """Yields `StreamingRecognizeRequest`s constructed from a recording audio
    stream.

    Args:
        data_stream (generator): The raw audio data to send.
        rate (int): The sampling rate in hertz.
        interim_results (boolean): Whether to return intermediate results,
            before the transcription is finalized.
    """
    # The initial request must contain metadata about the stream, so the
    # server knows how to interpret it.
    recognition_config = cloud_speech_pb2.RecognitionConfig(
        # There are a bunch of config options you can specify. See
        # https://goo.gl/KPZn97 for the full list.
        encoding='LINEAR16',  # raw 16-bit signed LE samples
        sample_rate=rate,  # the rate in hertz
        # See http://g.co/cloud/speech/docs/languages
        # for a list of supported languages.
        language_code='en-US',  # a BCP-47 language tag
    )
    streaming_config = cloud_speech_pb2.StreamingRecognitionConfig(
        interim_results=interim_results,
        config=recognition_config,
    )

    yield cloud_speech_pb2.StreamingRecognizeRequest(
        streaming_config=streaming_config)

    for data in data_stream:
        # Subsequent requests can all just have the content
        yield cloud_speech_pb2.StreamingRecognizeRequest(audio_content=data)


def listen_print_loop(
        recognize_stream, wrap_it_up_secs, buff, max_recog_secs=60):
    """Iterates through server responses and prints them.

    The recognize_stream passed is a generator that will block until a response
    is provided by the server. When the transcription response comes, print it.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    # What time should we switch to a new stream?
    time_to_switch = time.time() + max_recog_secs - wrap_it_up_secs
    graceful_exit = False
    num_chars_printed = 0
    for resp in recognize_stream:
        if resp.error.code != code_pb2.OK:
            raise RuntimeError('Server error: ' + resp.error.message)

        if not resp.results:
            if resp.endpointer_type is resp.END_OF_SPEECH and (
                    time.time() > time_to_switch):
                graceful_exit = True
                buff.put(None)
            continue

        # Display the top transcription
        result = resp.results[0]
        transcript = result.alternatives[0].transcript

        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * max(0, num_chars_printed - len(transcript))

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                recognize_stream.cancel()

            elif graceful_exit:
                break

            num_chars_printed = 0


def main():
    service = cloud_speech_pb2.SpeechStub(
        make_channel('speech.googleapis.com'))

    # For streaming audio from the microphone, there are three threads.
    # First, a thread that collects audio data as it comes in
    with record_audio(RATE, CHUNK) as buff:
        # Second, a thread that sends requests with that data
        overlap_buffer = collections.deque(
            maxlen=int(SECS_OVERLAP * RATE / CHUNK))
        requests = request_stream(
            _audio_data_generator(buff, overlap_buffer), RATE)
        # Third, a thread that listens for transcription responses
        recognize_stream = service.StreamingRecognize(
            requests, DEADLINE_SECS)

        # Exit things cleanly on interrupt
        signal.signal(signal.SIGINT, lambda *_: recognize_stream.cancel())

        # Now, put the transcription responses to use.
        try:
            while True:
                listen_print_loop(recognize_stream, WRAP_IT_UP_SECS, buff)

                # Discard this stream and create a new one.
                # Note: calling .cancel() doesn't immediately raise an RpcError
                # - it only raises when the iterator's next() is requested
                recognize_stream.cancel()

                logging.debug('Starting new stream')
                requests = request_stream(_audio_data_generator(
                    buff, overlap_buffer), RATE)
                recognize_stream = service.StreamingRecognize(
                        requests, DEADLINE_SECS)

        except grpc.RpcError:
            # This happens because of the interrupt handler
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', help='increase output verbosity',
        action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    main()
