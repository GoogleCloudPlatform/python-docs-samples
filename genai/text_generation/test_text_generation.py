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

import os

from typing import Generator

from google import genai

import pytest

import textgen_chat_with_txt
import textgen_chat_with_txt_stream
import textgen_with_txt
import textgen_with_txt_img
import textgen_with_txt_stream


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


@pytest.fixture(autouse=True)
def setup_client() -> Generator[None, None, None]:
    original_Client = genai.Client

    class AutoInitClient(original_Client):
        def __new__(cls, *args, **kwargs) -> genai.Client:  # noqa: ANN002 ANN003
            return original_Client(
                vertexai=True,
                project=PROJECT_ID,
                location="us-central1"
            )

    genai.Client = AutoInitClient

    yield

    genai.Client = original_Client


def test_textgen_with_txt() -> None:
    response = textgen_with_txt.generate_content()
    assert response


def test_textgen_with_txt_img() -> None:
    response = textgen_with_txt_img.generate_content()
    assert response


def test_textgen_with_txt_stream() -> None:
    response = textgen_with_txt_stream.generate_content()
    assert response


def test_textgen_chat_with_txt() -> None:
    response = textgen_chat_with_txt.generate_content()
    assert response


def test_textgen_chat_with_txt_stream() -> None:
    response = textgen_chat_with_txt_stream.generate_content()
    assert response
