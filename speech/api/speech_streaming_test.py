# Copyright 2016, Google, Inc.
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

import contextlib
import io
import re
import sys

import pytest

import speech_streaming


class MockAudioStream(object):
    def __init__(self, audio_filename, trailing_silence_secs=10):
        self.audio_filename = audio_filename
        self.silence = io.BytesIO('\0\0' * speech_streaming.RATE *
                                  trailing_silence_secs)

    def __enter__(self):
        self.audio_file = open(self.audio_filename)
        return self

    def __exit__(self, *args):
        self.audio_file.close()

    def __call__(self, *args):
        return self

    def read(self, num_frames):
        # audio is 16-bit samples, whereas python byte is 8-bit
        num_bytes = 2 * num_frames
        chunk = self.audio_file.read(num_bytes) or self.silence.read(num_bytes)
        return chunk


def mock_audio_stream(filename):
    @contextlib.contextmanager
    def mock_audio_stream(channels, rate, chunk):
        with open(filename, 'rb') as audio_file:
            yield audio_file

    return mock_audio_stream


@pytest.mark.skipif(
    sys.version_info >= (3, 0), reason="can't get grpc lib to work in python3")
def test_main(resource, monkeypatch, capsys):
    monkeypatch.setattr(
        speech_streaming, 'record_audio',
        mock_audio_stream(resource('quit.raw')))
    monkeypatch.setattr(speech_streaming, 'DEADLINE_SECS', 5)

    speech_streaming.main()
    out, err = capsys.readouterr()

    assert re.search(r'transcript.*"quit"', out, re.DOTALL | re.I)
