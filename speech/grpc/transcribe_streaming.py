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

from __future__ import division

import logging
logging.basicConfig(level=logging.INFO , format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(threadName)s: %(message)s')
logger = logging.getLogger(__name__)

import contextlib
import functools
import re
import signal
import sys
from itertools import imap

import google.auth
import google.auth.transport.grpc
import google.auth.transport.requests
from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2
from google.rpc import code_pb2
import grpc
import pyaudio
import wave
import time
from six.moves import queue

# Audio recording parameters
RATE = 16000            # bytes/second
PACKET_DURATION = 0.1    # 100 ms
PACKET_SIZE = int(RATE*PACKET_DURATION)
                        # 16000 bytes
CHUNK_DURATION = 30    # 30 seconds
NUM_CHUNKS = int(CHUNK_DURATION/PACKET_DURATION)
                        # 30/0.1 = 300

SUBCHUNK_DURATION = 1  # 1sec
NUM_SUBCHUNKS = int(SUBCHUNK_DURATION/PACKET_DURATION)
                        # 1/0.1 = 10
SUBCHUNK_SLEEP = SUBCHUNK_DURATION

audio_generated_for = 0.0

# The Speech API has a streaming limit of 60 seconds of audio*, so keep the
# connection alive for that long, plus some more to give the API time to figure
# out the transcription.
# * https://g.co/cloud/speech/limits#content
DEADLINE_SECS = 60 * 3 + 5
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'


def make_channel(host, port):
    """Creates a secure channel with auth credentials from the environment."""
    # Grab application default credentials from the environment
    credentials, _ = google.auth.default(scopes=[SPEECH_SCOPE])

    # Create a secure channel using the credentials.
    http_request = google.auth.transport.requests.Request()
    target = '{}:{}'.format(host, port)

    return google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, target)


def _audio_data_generator(buff):
    """A generator that yields all available data in the given buffer.

    Args:
        buff - a Queue object, where each element is a chunk of data.
    Yields:
        A chunk of data that is the aggregate of all chunks of data in `buff`.
        The function will block until at least one data chunk is available.
    """
    global audio_generated_for
    num_packets_to_yield = 500
    stop_none = False
    stop_limit = False
    total_packets_yielded = 0
    while not (stop_limit or stop_none):
        # Use a blocking get() to ensure there's at least one chunk of data.
        data = [buff.get()]

        # Now consume whatever other data's still buffered.
        for _i in range(NUM_SUBCHUNKS-1):
            try:
                data.append(buff.get(block=False))
            except queue.Empty:
                break

        # `None` in the buffer signals that the audio stream is closed. Yield
        # the final bit of the buffer and exit the loop.
        if None in data:
            stop_none = True
            data.remove(None)

        total_packets_yielded += len(data)
        logger.debug('yielded {} packets of audio'.format(total_packets_yielded))
        if( total_packets_yielded > num_packets_to_yield ):
            stop_limit = True
        if(len(data)>0):
            audio_generated_for += (len(data)*PACKET_DURATION)
            yield b''.join(data)

    if( stop_none ):
        logger.debug('None encountered')
    elif( stop_limit ):
        logger.warn('limit exceeded')
    return

def _fill_buffer(buff, in_data, frame_count, time_info, status_flags):
    """Continuously collect data from the audio stream, into the buffer."""
    buff.put(in_data)
    return None, pyaudio.paContinue


# [START audio_stream]
@contextlib.contextmanager
def record_audio(rate, chunk_size):
    """Opens a recording stream in a context manager."""
    # Create a thread-safe buffer of audio data
    buff = queue.Queue()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        # The API currently only supports 1-channel (mono) audio
        # https://goo.gl/z757pE
        channels=1, rate=rate,
        input=True, frames_per_buffer=chunk_size,
        # Run the audio stream asynchronously to fill the buffer object.
        # This is necessary so that the input device's buffer doesn't overflow
        # while the calling thread makes network requests, etc.
        stream_callback=functools.partial(_fill_buffer, buff),
    )

    yield _audio_data_generator(buff)

    audio_stream.stop_stream()
    audio_stream.close()
    # Signal the _audio_data_generator to finish
    buff.put(None)
    audio_interface.terminate()
# [END audio_stream]

# [START audio_file]
@contextlib.contextmanager
def get_audio(rate, chunk_size, audio_file):
    """Opens a recording stream in a context manager."""
    # Create a thread-safe buffer of audio data
    buff = queue.Queue()

    wr = wave.open(audio_file, 'rb')
    data = wr.readframes(chunk_size)

    i = 0
    while data!='':
        buff.put(data)
        i+=1
        logger.debug('put {} packets of data in buffer'.format(i))
        data = wr.readframes(chunk_size)

    logger.info('generated audio from file: {}'.format(audio_file))
    logger.info('number of packets: {} '.format(i))
    buff.put(None)
    yield _audio_data_generator(buff)

    # Signal the _audio_data_generator to finish
# [END audio_file]

# [START audio_file]
@contextlib.contextmanager
def get_audio_multiple(rate, chunk_size, audio_file):
    """Opens a recording stream in a context manager."""
    # Create a thread-safe buffer of audio data
    assert chunk_size==PACKET_SIZE
    buffs = []

    wr = wave.open(audio_file, 'rb')
    data = wr.readframes(PACKET_SIZE)

    i = 0
    while data!='':
        if(i%NUM_CHUNKS== 0):
            try:
                buffs[-1].put(None)
            except Exception as e:
                pass
            logger.debug('adding new buffer to list')
            buffs.append(queue.Queue())
        buffs[-1].put(data)
        i+=1
        logger.debug('put {} packets of data in buffer'.format(i))
        data = wr.readframes(PACKET_SIZE)
    logger.info('generated audio from file: {}'.format(audio_file))
    logger.info('number of packets: {} '.format(i))
    logger.info('number of buffers: {}'.format(len(buffs)))
    buffs[-1].put(None)
    yield imap(_audio_data_generator, buffs)

    # Signal the _audio_data_generator to finish
    for buff in buffs:
        buff.put(None)
# [END audio_file]


def request_stream(data_stream, rate, interim_results=True):
    """Yields `StreamingRecognizeRequest`s constructed from a recording audio
    stream.

    Args:
        data_stream: A generator that yields raw audio data to send.
        rate: The sampling rate in hertz.
        interim_results: Whether to return intermediate results, before the
            transcription is finalized.
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
        logging.debug('requesting after {}s'.format(audio_generated_for))
        time.sleep(SUBCHUNK_SLEEP)
        yield cloud_speech_pb2.StreamingRecognizeRequest(audio_content=data)


def listen_print_loop(recognize_stream):
    """Iterates through server responses and prints them.

    The recognize_stream passed is a generator that will block until a response
    is provided by the server. When the transcription response comes, print it.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    num_responses = 0
    for resp in recognize_stream:
        num_responses+=1
        if resp.error.code != code_pb2.OK:
            raise RuntimeError('Server error: ' + resp.error.message)
        log_format = '{}s, err:{}, final:{}, conf:{}, {}'

        if not resp.results:
            logger.debug(log_format.format(audio_generated_for, resp.error.code, None, None, resp.results)) 
            continue

        # Display the top transcription
        result = resp.results[0]
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # overwrite_chars = ' ' * max(0, num_chars_printed - len(transcript))

        log_message = log_format.format(audio_generated_for, resp.error.code, result.is_final, confidence, transcript)
        if( result.is_final ):
            logging.info(log_message)
        else:
            logging.debug(log_message)
            # sys.stdout.write(str(confidence) + transcript + overwrite_chars + '\n')
            # sys.stdout.flush()
            # num_chars_printed = len(transcript)

            # print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            # num_chars_printed = 0


def main(args):
    print 'making service'
    service = cloud_speech_pb2.SpeechStub(
        make_channel('speech.googleapis.com', 443))

    # For streaming audio from the microphone, there are three threads.
    # First, a thread that collects audio data as it comes in
    print 'opening file:'
    speech_file = args.filename
    with get_audio_multiple(RATE, PACKET_SIZE, speech_file) as list_buffered_audio_data:
      for buffered_audio_data in list_buffered_audio_data:
        # Second, a thread that sends requests with that data
        requests = request_stream(buffered_audio_data, RATE)
        # Third, a thread that listens for transcription responses
        recognize_stream = service.StreamingRecognize(
            requests, DEADLINE_SECS)

        # Exit things cleanly on interrupt
        signal.signal(signal.SIGINT, lambda *_: recognize_stream.cancel())

        # Now, put the transcription responses to use.
        try:
            listen_print_loop(recognize_stream)

            recognize_stream.cancel()
        except grpc.RpcError as e:
            code = e.code()
            # CANCELLED is caused by the interrupt handler, which is expected.
            if code is not code.CANCELLED:
                raise

def parse_args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename', type=str)
    args = p.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main( args )

