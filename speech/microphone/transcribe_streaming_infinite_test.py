# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
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

from unittest import mock

import pytest

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


class MockPyAudio:
    def __init__(self: object, audio_filename: str) -> None:
        self.audio_filename = audio_filename

    def __call__(self: object, *args: object) -> object:
        return self

    def open(
        self: object,
        stream_callback: object,
        rate: int,
        *args: object,
        **kwargs: object
    ) -> object:
        self.rate = rate
        self.closed = threading.Event()
        self.stream_thread = threading.Thread(
            target=self.stream_audio,
            args=(self.audio_filename, stream_callback, self.closed),
        )
        self.stream_thread.start()
        return self

    def close(self: object) -> None:
        self.closed.set()

    def stop_stream(self: object) -> None:
        pass

    def terminate(self: object) -> None:
        pass

    def stream_audio(
        self: object,
        audio_filename: str,
        callback: object,
        closed: object,
        num_frames: int = 512,
    ) -> None:
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
def test_main(capsys: pytest.CaptureFixture) -> None:
    import transcribe_streaming_infinite

    transcribe_streaming_infinite.main()
    out, err = capsys.readouterr()

    assert re.search(r"quit", out, re.DOTALL | re.I)
