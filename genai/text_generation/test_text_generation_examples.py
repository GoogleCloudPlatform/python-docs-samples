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

import model_optimizer_textgen_with_txt
import textgen_async_with_txt
import textgen_chat_stream_with_txt
import textgen_chat_with_txt
import textgen_config_with_txt
import textgen_sys_instr_with_txt
import textgen_transcript_with_gcs_audio
import textgen_with_gcs_audio
import textgen_with_local_video
import textgen_with_multi_img
import textgen_with_multi_local_img
import textgen_with_mute_video
import textgen_with_pdf
import textgen_with_txt
import textgen_with_txt_img
import textgen_with_txt_stream
import textgen_with_video
import textgen_with_youtube_video
import thinking_textgen_with_txt

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"  # "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_textgen_with_txt_stream() -> None:
    response = textgen_with_txt_stream.generate_content()
    assert response


def test_textgen_with_txt() -> None:
    response = textgen_with_txt.generate_content()
    assert response


def test_textgen_chat_with_txt() -> None:
    response = textgen_chat_with_txt.generate_content()
    assert response


def test_textgen_chat_with_txt_stream() -> None:
    response = textgen_chat_stream_with_txt.generate_content()
    assert response


def test_textgen_config_with_txt() -> None:
    response = textgen_config_with_txt.generate_content()
    assert response


def test_textgen_sys_instr_with_txt() -> None:
    response = textgen_sys_instr_with_txt.generate_content()
    assert response


def test_textgen_with_pdf() -> None:
    response = textgen_with_pdf.generate_content()
    assert response


def test_textgen_with_txt_img() -> None:
    response = textgen_with_txt_img.generate_content()
    assert response


def test_textgen_with_txt_thinking() -> None:
    response = thinking_textgen_with_txt.generate_content()
    assert response


def test_textgen_with_multi_img() -> None:
    response = textgen_with_multi_img.generate_content()
    assert response


def test_textgen_with_multi_local_img() -> None:
    response = textgen_with_multi_local_img.generate_content(
        "./test_data/latte.jpg",
        "./test_data/scones.jpg",
    )
    assert response


def test_textgen_with_mute_video() -> None:
    response = textgen_with_mute_video.generate_content()
    assert response


def test_textgen_with_gcs_audio() -> None:
    response = textgen_with_gcs_audio.generate_content()
    assert response


def test_textgen_transcript_with_gcs_audio() -> None:
    response = textgen_transcript_with_gcs_audio.generate_content()
    assert response


def test_textgen_with_video() -> None:
    response = textgen_with_video.generate_content()
    assert response


def test_textgen_async_with_txt() -> None:
    response = textgen_async_with_txt.generate_content()
    assert response


def test_textgen_with_local_video() -> None:
    response = textgen_with_local_video.generate_content()
    assert response


def test_textgen_with_youtube_video() -> None:
    response = textgen_with_youtube_video.generate_content()
    assert response


def test_model_optimizer_textgen_with_txt() -> None:
    os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
    response = model_optimizer_textgen_with_txt.generate_content()
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"  # "us-central1"
    assert response
