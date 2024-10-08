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
import gemini_chat_example
import gemini_guide_example
import gemini_multi_image_example
import gemini_pdf_example
import gemini_pro_basic_example
import gemini_pro_config_example
import gemini_text_input_example


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)


# TODO: Delete this test after approval /text_generation/image_example01.py
def test_gemini_guide_example() -> None:
    text = gemini_guide_example.generate_text()
    text = text.lower()
    assert len(text) > 0


# TODO: Delete this test after approval /text_generation/text_example01.py
def test_gemini_text_input_example() -> None:
    text = gemini_text_input_example.generate_from_text_input()
    assert len(text) > 0


# TODO: Delete this test after approval /text_generation/image_example02.py
def test_gemini_pro_basic_example() -> None:
    text = gemini_pro_basic_example.generate_text()
    assert len(text) > 0


# TODO: Delete this test after approval /text_generation/pro_config_example.py
def test_gemini_pro_config_example() -> None:
    import urllib.request

    #  download the image
    fname = "scones.jpg"
    url = "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    urllib.request.urlretrieve(url, fname)

    if os.path.isfile(fname):
        text = gemini_pro_config_example.generate_text()
        text = text.lower()
        assert len(text) > 0

        # clean-up
        os.remove(fname)
    else:
        raise Exception("File(scones.jpg) not found!")


# TODO: Delete this test after approval /text_generation/single_turn_multi_image_example.py
def test_gemini_multi_image_example() -> None:
    text = gemini_multi_image_example.generate_text_multimodal()
    text = text.lower()
    assert len(text) > 0
    assert "city" in text
    assert "landmark" in text


# TODO: Delete this test after approval /text_generation/pdf_example.py
@pytest.mark.skip(
    "TODO: Exception Logs indicate safety filters are likely blocking model output b/339985493"
)
def test_gemini_pdf_example() -> None:
    text = gemini_pdf_example.analyze_pdf()
    assert len(text) > 0


# TODO: Delete this test after approval /text_generation/multimodal_example01.py
def test_gemini_chat_example() -> None:
    text = gemini_chat_example.chat_text_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])

    text = gemini_chat_example.chat_stream_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])


# TODO: Delete this test after approval /text_generation/multimodal_example01.py
def test_analyze_all_modalities() -> None:
    text = gemini_all_modalities.analyze_all_modalities()
    assert len(text) > 0
