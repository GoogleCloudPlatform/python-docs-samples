# Copyright 2023 Google LLC
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
import vertexai

import gemini_chat_example
import gemini_count_token_example
import gemini_guide_example
import gemini_multi_image_example
import gemini_safety_config_example
import gemini_single_turn_video_example


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)


def test_gemini_guide_example() -> None:
    text = gemini_guide_example.generate_text(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "scones" in text


def test_gemini_multi_image_example() -> None:
    text = gemini_multi_image_example.generate_text_multimodal(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "city" in text
    assert "landmark" in text


def test_gemini_count_token_example() -> None:
    text = gemini_count_token_example.generate_text(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "sky" in text


def test_gemini_safety_config_example() -> None:
    import urllib
    import typing
    import http
    from vertexai.preview.generative_models import Image

    def load_image_from_url(image_url: str) -> str:
        with urllib.request.urlopen(image_url) as response:
            response = typing.cast(http.client.HTTPResponse, response)
            image_bytes = response.read()
        return Image.from_bytes(image_bytes)

    # import base64

    # base64_image_data = base64.b64encode(
    #     open('scones.jpg', 'rb').read()).decode("utf-8")
    # image = generative_models.Part.from_data(
    #     data=base64.b64decode(base64_image_data), mime_type="image/png")
    image = load_image_from_url(
        "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    )

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    text = gemini_safety_config_example.generate_text(PROJECT_ID, LOCATION, image)
    text = text.lower()
    assert len(text) > 0
    assert "scones" in text


def test_gemini_single_turn_video_example() -> None:
    text = gemini_single_turn_video_example.generate_text(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "sky" in text


def test_gemini_chat_example() -> None:
    text = gemini_chat_example.chat_text_example(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "ai" in text

    text = gemini_chat_example.chat_stream_example(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "ai" in text
