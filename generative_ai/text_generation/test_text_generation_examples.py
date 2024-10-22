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

from google.api_core.exceptions import ResourceExhausted

import chat_code_example
import chat_multiturn_example
import chat_multiturn_stream_example
import chat_simple_example
import code_completion_example
import codegen_example
import gemini_describe_http_image_example
import gemini_describe_http_pdf_example
import generation_config_example
import multimodal_stream_example
import single_turn_multi_image_example


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_chat() -> None:
    content = chat_code_example.write_a_function().text
    assert len(content) > 0


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


def test_stream_multi_modality_basic_example() -> None:
    responses = multimodal_stream_example.generate_content()
    assert responses


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_generation_function() -> None:
    content = codegen_example.generate_a_function().text
    print(content)
    assert "year" in content
    assert "return" in content


def test_gemini_multi_image_example() -> None:
    text = single_turn_multi_image_example.generate_text_multimodal()
    text = text.lower()
    assert len(text) > 0
    assert "city" in text
    assert "landmark" in text


def test_gemini_pro_config_example() -> None:
    import urllib.request

    # Download the image
    fname = "scones.jpg"
    url = "https://storage.googleapis.com/generativeai-downloads/images/scones.jpg"
    urllib.request.urlretrieve(url, fname)

    if os.path.isfile(fname):
        text = generation_config_example.generate_text()
        text = text.lower()
        assert len(text) > 0

        # clean-up
        os.remove(fname)
    else:
        raise Exception("File(scones.jpg) not found!")


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_chat_example() -> None:
    response = chat_simple_example.send_chat()
    assert len(response) > 0


def test_gemini_chat_example() -> None:
    text = chat_multiturn_example.chat_text_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])

    text = chat_multiturn_stream_example.chat_stream_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])
