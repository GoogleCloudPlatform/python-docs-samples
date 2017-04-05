# Copyright 2016, Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import re
import threading
import time

import transcribe_streaming_minute as transcribe_streaming

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


class MockPyAudio(object):
    def __init__(self, *audio_filenames):
        self.audio_filenames = audio_filenames

    def __call__(self, *args):
        return self

    def open(self, stream_callback, *args, **kwargs):
        self.closed = threading.Event()
        self.stream_thread = threading.Thread(
            target=self.stream_audio, args=(
                self.audio_filenames, stream_callback, self.closed))
        self.stream_thread.start()
        return self

    def close(self):
        self.closed.set()

    def stop_stream(self):
        pass

    def terminate(self):
        pass

    @staticmethod
    def stream_audio(audio_filenames, callback, closed, num_frames=512):
        # audio is 16-bit samples, whereas python byte is 8-bit
        num_bytes = 2 * num_frames
        # Approximate realtime by sleeping for the appropriate time for the
        # requested number of frames
        sleep_secs = num_frames / float(transcribe_streaming.RATE)

        for audio_filename in audio_filenames:
            with open(audio_filename, 'rb') as audio_file:
                # While the audio stream hasn't been closed, give it chunks of
                # the audio file, until we run out of audio file.
                while not closed.is_set():
                    chunk = audio_file.read(num_bytes)
                    if not chunk:
                        break
                    time.sleep(sleep_secs)
                    callback(chunk, None, None, None)
                else:
                    break

                # Ran out of audio data. Give a second of silence between files
                for _ in range(int(1 + 1 / sleep_secs)):
                    if closed.is_set():
                        break
                    time.sleep(sleep_secs)
                    callback(b'\0' * num_bytes, None, None, None)
        else:
            # No more audio left. Just give silence until we're done
            while not closed.is_set():
                time.sleep(sleep_secs)
                callback(b'\0' * num_bytes, None, None, None)


def test_main(monkeypatch, capsys, caplog):
    caplog.setLevel(logging.DEBUG)
    monkeypatch.setattr(
        transcribe_streaming.pyaudio, 'PyAudio',
        MockPyAudio(
            os.path.join(RESOURCES, 'audio.raw'),
            os.path.join(RESOURCES, 'quit.raw')))
    monkeypatch.setattr(
        transcribe_streaming, 'WRAP_IT_UP_SECS', 59)

    transcribe_streaming.main()
    out, err = capsys.readouterr()

    assert re.search(
        r'old is the.*quit', out, re.DOTALL | re.I)
    assert 'Starting new stream' in caplog.text()
