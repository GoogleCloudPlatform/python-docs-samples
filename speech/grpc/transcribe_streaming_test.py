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

import re
import time

import transcribe_streaming


class MockPyAudio(object):
    def __init__(self, audio_filename):
        self.audio_filename = audio_filename

    def __call__(self, *args):
        return self

    def open(self, *args, **kwargs):
        self.audio_file = open(self.audio_filename, 'rb')
        return self

    def close(self):
        self.audio_file.close()

    def stop_stream(self):
        pass

    def terminate(self):
        pass

    def read(self, num_frames):
        if self.audio_file.closed:
            raise IOError()
        # Approximate realtime by sleeping for the appropriate time for the
        # requested number of frames
        time.sleep(num_frames / float(transcribe_streaming.RATE))
        # audio is 16-bit samples, whereas python byte is 8-bit
        num_bytes = 2 * num_frames
        try:
            chunk = self.audio_file.read(num_bytes)
        except ValueError:
            raise IOError()
        if not chunk:
            raise IOError()
        return chunk


def test_main(resource, monkeypatch, capsys):
    monkeypatch.setattr(
        transcribe_streaming.pyaudio, 'PyAudio',
        MockPyAudio(resource('quit.raw')))

    transcribe_streaming.main()
    out, err = capsys.readouterr()

    assert re.search(r'quit', out, re.DOTALL | re.I)
