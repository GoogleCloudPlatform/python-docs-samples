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

import os

import pytest

import live_websocket_audiogen_with_txt
import live_websocket_audiotranscript_with_txt
import live_websocket_textgen_with_audio
import live_websocket_textgen_with_txt
import live_with_txt
import live_audio_with_txt
import live_txt_with_audio
import live_transcribe_with_audio

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


@pytest.mark.asyncio
async def test_live_with_text() -> None:
    assert await live_with_txt.generate_content()


@pytest.mark.asyncio
async def test_live_websocket_textgen_with_audio() -> None:
    assert await live_websocket_textgen_with_audio.generate_content()


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
async def test_live_txt_with_audio() -> None:
    assert await live_txt_with_audio.generate_content()


@pytest.mark.asyncio
async def test_live_audio_with_txt() -> None:
    result = await live_audio_with_txt.generate_content()
    assert result is not None


@pytest.mark.asyncio
async def test_live_transcribe_with_audio() -> None:
    result = await live_transcribe_with_audio.generate_content()
    assert result is not None
