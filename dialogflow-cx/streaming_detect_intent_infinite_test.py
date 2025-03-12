# Copyright 2025 Google LLC
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

import logging
import os
import threading
import time

from unittest import mock

import pytest

DIRNAME = os.path.realpath(os.path.dirname(__file__))
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "global"
AGENT_ID = os.getenv("AGENT_ID")
AGENT_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}"
AUDIO_PATH = os.getenv("AUDIO_PATH")
AUDIO = f"{DIRNAME}/{AUDIO_PATH}"
AUDIO_SAMPLE_RATE = 24000
CHUNK_SECONDS = 0.1
TIMEOUT = 10  # timeout in seconds


class MockPyAudio:
    def __init__(self: object, audio_filename: str) -> None:
        self.audio_filename = audio_filename
        self.streams = []

    def __call__(self: object, *args: object) -> object:
        return self

    def open(
        self: object,
        rate: int,
        input: bool = False,
        output: bool = False,
        stream_callback: object = None,
        *args: object,
        **kwargs: object,
    ) -> object:

        stream = MockStream(self.audio_filename, rate, input, output, stream_callback)
        self.streams.append(stream)
        return stream

    def get_default_input_device_info(self: object) -> dict:
        return {"name": "input-device"}

    def get_default_output_device_info(self: object) -> dict:
        return {"name": "output-device"}

    def terminate(self: object) -> None:
        for stream in self.streams:
            stream.close()


class MockStream:
    def __init__(
        self: object,
        audio_filename: str,
        rate: int,
        input: bool = False,
        output: bool = False,
        stream_callback: object = None,
    ) -> None:
        self.closed = threading.Event()
        self.input = input
        self.output = output
        if input:
            self.rate = rate
            self.stream_thread = threading.Thread(
                target=self.stream_audio,
                args=(audio_filename, stream_callback, self.closed),
            )
            self.stream_thread.start()

    def stream_audio(
        self: object,
        audio_filename: str,
        callback: object,
        closed: object,
        num_frames: int = int(AUDIO_SAMPLE_RATE * CHUNK_SECONDS),
    ) -> None:
        with open(audio_filename, "rb") as audio_file:
            logging.info(f"closed {closed.is_set()}")
            while not closed.is_set():
                # Approximate realtime by sleeping for the appropriate time for
                # the requested number of frames
                time.sleep(num_frames / self.rate)
                # audio is 16-bit samples, whereas python byte is 8-bit
                num_bytes = 2 * num_frames
                chunk = audio_file.read(num_bytes) or b"\0" * num_bytes
                callback(chunk, None, None, None)

    def start_stream(self: object) -> None:
        self.closed.clear()

    def stop_stream(self: object) -> None:
        self.closed.set()

    def write(self: object, frames: bytes) -> None:
        pass

    def close(self: object) -> None:
        self.closed.set()

    def is_stopped(self: object) -> bool:
        return self.closed.is_set()


@pytest.mark.asyncio
async def test_main(caplog: pytest.CaptureFixture) -> None:
    with mock.patch.dict(
        "sys.modules",
        pyaudio=mock.MagicMock(PyAudio=MockPyAudio(AUDIO)),
    ):
        import streaming_detect_intent_infinite

        with caplog.at_level(logging.INFO):
            await streaming_detect_intent_infinite.main(
                agent_name=AGENT_NAME,
                sample_rate=AUDIO_SAMPLE_RATE,
                dialogflow_timeout=TIMEOUT,
            )
            assert "Detected intent: Default Welcome Intent" in caplog.text
