# Copyright 2017 Google LLC

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

import os
import re
import threading
import time

import mock

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


class MockPyAudio(object):
    def __init__(self, audio_filename):
        self.audio_filename = audio_filename

    def __call__(self, *args):
        return self

    def open(self, stream_callback, rate, *args, **kwargs):
        self.rate = rate
        self.closed = threading.Event()
        self.stream_thread = threading.Thread(
            target=self.stream_audio,
            args=(self.audio_filename, stream_callback, self.closed),
        )
        self.stream_thread.start()
        return self

    def close(self):
        self.closed.set()

    def stop_stream(self):
        pass

    def terminate(self):
        pass

    def stream_audio(self, audio_filename, callback, closed, num_frames=512):
        with open(audio_filename, "rb") as audio_file:
            while not closed.is_set():
                # Approximate realtime by sleeping for the appropriate time for
                # the requested number of frames
                time.sleep(num_frames / float(self.rate))
                # audio is 16-bit samples, whereas python byte is 8-bit
                num_bytes = 2 * num_frames
                chunk = audio_file.read(num_bytes) or b"\0" * num_bytes
                callback(chunk, None, None, None)


@mock.patch.dict(
    "sys.modules",
    pyaudio=mock.MagicMock(PyAudio=MockPyAudio(os.path.join(RESOURCES, "quit.raw"))),
)
def test_main(capsys):
    import transcribe_streaming_mic

    transcribe_streaming_mic.main()
    out, err = capsys.readouterr()

    assert re.search(r"quit", out, re.DOTALL | re.I)
