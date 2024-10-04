# Copyright 2024 Google LLC
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

import backoff

import code_completion_example
import codegen_example
import credentials_refresher_usage_example
import gemini_describe_http_image_example
import gemini_describe_http_pdf_example

from google.api_core.exceptions import ResourceExhausted

import image_example01
import image_example02
import multimodal_example01
import multimodal_example02
import multimodal_stream_example
import pdf_example
import pro_config_example
import single_turn_multi_image_example


def test_gemini_describe_http_image_example() -> None:
    text = gemini_describe_http_image_example.generate_content()
    assert len(text) > 0


def test_gemini_describe_http_pdf_example() -> None:
    text = gemini_describe_http_pdf_example.generate_content()
    assert len(text) > 0


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_completion_comment() -> None:
    content = code_completion_example.complete_code_function().text
    assert len(content) > 0


def test_credentials_refresher() -> None:
    response = credentials_refresher_usage_example.generate_text()
    assert response


def test_analyze_all_modalities() -> None:
    text = multimodal_example01.analyze_all_modalities()
    assert len(text) > 0


def test_stream_multi_modality_basic() -> None:
    responses = multimodal_example02.generate_content()
    assert responses


def test_stream_multi_modality_basic_example() -> None:
    responses = multimodal_stream_example.generate_content()
    assert responses


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_generation_function() -> None:
    content = codegen_example.generate_a_function().text
    print(content)
    assert "year" in content
    assert "return" in content


def test_gemini_guide_example() -> None:
    text = image_example01.generate_text()
    text = text.lower()
    assert len(text) > 0


def test_gemini_multi_image_example() -> None:
    text = single_turn_multi_image_example.generate_text_multimodal()
    text = text.lower()
    assert len(text) > 0
    assert "city" in text
    assert "landmark" in text


# @pytest.mark.skip(
#     "TODO: Exception Logs indicate safety filters are likely blocking model output b/339985493"
# )
def test_gemini_pdf_example() -> None:
    text = pdf_example.analyze_pdf()
    assert len(text) > 0


def test_gemini_pro_basic_example() -> None:
    text = image_example02.generate_text()
    assert len(text) > 0


def test_gemini_pro_config_example() -> None:
    import urllib.request

    #  download the image
    fname = "scones.jpg"
    url = "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    urllib.request.urlretrieve(url, fname)

    if os.path.isfile(fname):
        text = pro_config_example.generate_text()
        text = text.lower()
        assert len(text) > 0

        # clean-up
        os.remove(fname)
    else:
        raise Exception("File(scones.jpg) not found!")
