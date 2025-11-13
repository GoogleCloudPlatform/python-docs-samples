# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Using Google Cloud Vertex AI to test the code samples.
#
import base64
import os
import sys
import types

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_mock

import live_audio_with_txt
import live_audiogen_with_txt
import live_code_exec_with_txt
import live_func_call_with_txt
import live_ground_googsearch_with_txt
import live_ground_ragengine_with_txt
import live_structured_output_with_txt
import live_transcribe_with_audio
import live_txt_with_audio
import live_txtgen_with_audio
import live_websocket_audiogen_with_txt
import live_websocket_audiotranscript_with_txt
# import live_websocket_textgen_with_audio
import live_websocket_textgen_with_txt
import live_with_txt


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


@pytest.fixture
def mock_live_session() -> tuple[MagicMock, MagicMock]:
    async def async_gen(items: list) -> AsyncMock:
        for i in items:
            yield i

    mock_session = MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.send_client_content = AsyncMock()
    mock_session.send = AsyncMock()
    mock_session.receive = lambda: async_gen([])

    mock_client = MagicMock()
    mock_client.aio.live.connect.return_value = mock_session

    return mock_client, mock_session


@pytest.fixture()
def mock_rag_components(mocker: pytest_mock.MockerFixture) -> None:
    mock_client_cls = mocker.patch("google.genai.Client")

    class AsyncIterator:
        def __init__(self) -> None:
            self.used = False

        def __aiter__(self) -> "AsyncIterator":
            return self

        async def __anext__(self) -> object:
            if not self.used:
                self.used = True
                return mocker.MagicMock(
                    text="""In December 2023, Google launched Gemini, their "most capable and general model". It's multimodal, meaning it understands and combines different types of information like text, code, audio, images, and video."""
                )
            raise StopAsyncIteration

    mock_session = mocker.AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.receive = lambda: AsyncIterator()
    mock_client_cls.return_value.aio.live.connect.return_value = mock_session


@pytest.fixture()
def live_conversation() -> None:
    google_mod = types.ModuleType("google")
    genai_mod = types.ModuleType("google.genai")
    genai_types_mod = types.ModuleType("google.genai.types")

    class AudioTranscriptionConfig:
        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

    class Blob:
        def __init__(self, data: bytes, mime_type: str) -> None:
            self.data = data
            self.mime_type = mime_type

    class HttpOptions:
        def __init__(self, api_version: str | None = None) -> None:
            self.api_version = api_version

    class LiveConnectConfig:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.kwargs = kwargs

    class Modality:
        AUDIO = "AUDIO"

    genai_types_mod.AudioTranscriptionConfig = AudioTranscriptionConfig
    genai_types_mod.Blob = Blob
    genai_types_mod.HttpOptions = HttpOptions
    genai_types_mod.LiveConnectConfig = LiveConnectConfig
    genai_types_mod.Modality = Modality

    class FakeSession:
        async def __aenter__(self) -> "FakeSession":
            print("MOCK: entering FakeSession")
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            tb: types.TracebackType | None,
        ) -> None:
            print("MOCK: exiting FakeSession")

        async def send_realtime_input(self, media: object) -> None:
            print("MOCK: send_realtime_input called (no network)")

        async def receive(self) -> object:
            print("MOCK: receive started")
            if False:
                yield

    class FakeClient:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.aio = MagicMock()
            self.aio.live = MagicMock()
            self.aio.live.connect = MagicMock(return_value=FakeSession())
            print("MOCK: FakeClient created")

    def fake_client_constructor(*args: object, **kwargs: object) -> FakeClient:
        return FakeClient()

    genai_mod.Client = fake_client_constructor
    genai_mod.types = genai_types_mod

    old_modules = sys.modules.copy()

    sys.modules["google"] = google_mod
    sys.modules["google.genai"] = genai_mod
    sys.modules["google.genai.types"] = genai_types_mod

    import live_conversation_audio_with_audio as live

    def fake_read_wavefile(path: str) -> tuple[str, str]:
        print("MOCK: read_wavefile called")
        fake_bytes = b"\x00\x00" * 1000
        return base64.b64encode(fake_bytes).decode("ascii"), "audio/pcm;rate=16000"

    def fake_write_wavefile(path: str, frames: bytes, rate: int) -> None:
        print(f"MOCK: write_wavefile called (no file written) rate={rate}")

    live.read_wavefile = fake_read_wavefile
    live.write_wavefile = fake_write_wavefile

    yield live

    sys.modules.clear()
    sys.modules.update(old_modules)


@pytest.mark.asyncio
async def test_live_with_text() -> None:
    assert await live_with_txt.generate_content()


# @pytest.mark.asyncio
# async def test_live_websocket_textgen_with_audio() -> None:
#     assert await live_websocket_textgen_with_audio.generate_content()


@pytest.mark.asyncio
async def test_live_websocket_textgen_with_txt() -> None:
    assert await live_websocket_textgen_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_websocket_audiogen_with_txt() -> None:
    assert await live_websocket_audiogen_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_websocket_audiotranscript_with_txt() -> None:
    assert await live_websocket_audiotranscript_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_audiogen_with_txt() -> None:
    assert live_audiogen_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_code_exec_with_txt() -> None:
    assert await live_code_exec_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_func_call_with_txt() -> None:
    assert await live_func_call_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_ground_googsearch_with_txt() -> None:
    assert await live_ground_googsearch_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_transcribe_with_audio() -> None:
    assert await live_transcribe_with_audio.generate_content()


@pytest.mark.asyncio
async def test_live_txtgen_with_audio() -> None:
    assert await live_txtgen_with_audio.generate_content()


@pytest.mark.asyncio
def test_live_structured_output_with_txt() -> None:
    assert live_structured_output_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_ground_ragengine_with_txt(mock_rag_components: None) -> None:
    assert await live_ground_ragengine_with_txt.generate_content("test")


@pytest.mark.asyncio
async def test_live_txt_with_audio() -> None:
    assert await live_txt_with_audio.generate_content()


@pytest.mark.asyncio
async def test_live_audio_with_txt(mock_live_session: None) -> None:
    mock_client, mock_session = mock_live_session

    with patch("google.genai.Client", return_value=mock_client):
        with patch("simpleaudio.WaveObject.from_wave_file") as mock_wave:
            with patch("soundfile.write"):
                mock_wave_obj = mock_wave.return_value
                mock_wave_obj.play.return_value = MagicMock()
                result = await live_audio_with_txt.generate_content()

    assert result is not None


@pytest.mark.asyncio
async def test_live_conversation_audio_with_audio(live_conversation: types.ModuleType) -> None:
    result = await live_conversation.main()
    assert result is True or result is None
