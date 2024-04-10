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

import pytest
import vertexai

import gemini_all_modalities
import gemini_audio
import gemini_chat_example
import gemini_count_token_example
import gemini_grounding_example
import gemini_guide_example
import gemini_multi_image_example
import gemini_pdf_example
import gemini_pro_basic_example
import gemini_pro_config_example
import gemini_safety_config_example
import gemini_single_turn_video_example
import gemini_system_instruction
import gemini_video_audio


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)


def test_gemini_guide_example() -> None:
    text = gemini_guide_example.generate_text(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert "scones" in text


def test_gemini_pro_basic_example() -> None:
    text = gemini_pro_basic_example.generate_text(PROJECT_ID, LOCATION)
    assert len(text) > 0


def test_gemini_pro_config_example() -> None:
    import urllib.request

    #  download the image
    fname = "scones.jpg"
    url = "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    urllib.request.urlretrieve(url, fname)

    if os.path.isfile(fname):
        text = gemini_pro_config_example.generate_text(PROJECT_ID, LOCATION)
        text = text.lower()
        assert len(text) > 0
        assert any(e in text for e in ("blueberry", "coffee", "flower", "table"))

        # clean-up
        os.remove(fname)
    else:
        raise Exception("File(scones.jpg) not found!")


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


@pytest.mark.skip("Skip the test until it gets stable.")
def test_gemini_safety_config_example() -> None:
    import http
    import typing
    import urllib

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
    assert any(
        [_ in text for _ in ("scone", "blueberry", "coffee,", "flower", "table")]
    )


def test_gemini_single_turn_video_example() -> None:
    text = gemini_single_turn_video_example.generate_text(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("zoo", "tiger", "leaf", "water")])


def test_gemini_pdf_example() -> None:
    text = gemini_pdf_example.analyze_pdf(PROJECT_ID)
    assert len(text) > 0


def test_gemini_chat_example() -> None:
    text = gemini_chat_example.chat_text_example(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])

    text = gemini_chat_example.chat_stream_example(PROJECT_ID, LOCATION)
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])


@pytest.mark.skip(
    "Unable to test Google Search grounding due to allowlist restrictions."
)
def test_gemini_grounding_example() -> None:
    data_store_id = "test-search-engine_1689960780551"
    data_store_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/dataStores/{data_store_id}"
    response = gemini_grounding_example.generate_text_with_grounding(
        PROJECT_ID, LOCATION, data_store_path=data_store_path
    )
    assert response


def test_summarize_audio() -> None:
    text = gemini_audio.summarize_audio(PROJECT_ID)
    assert len(text) > 0


def test_transcript_audio() -> None:
    text = gemini_audio.transcript_audio(PROJECT_ID)
    assert len(text) > 0


def test_analyze_video_with_audio() -> None:
    text = gemini_video_audio.analyze_video_with_audio(PROJECT_ID)
    assert len(text) > 0


def test_analyze_all_modalities() -> None:
    text = gemini_all_modalities.analyze_all_modalities(PROJECT_ID)
    assert len(text) > 0


def test_set_system_instruction() -> None:
    text = gemini_system_instruction.set_system_instruction(PROJECT_ID)
    assert len(text) > 0
