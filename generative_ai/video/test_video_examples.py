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

import gemini_describe_http_video_example
import gemini_youtube_video_key_moments_example
import gemini_youtube_video_summarization_example
import multimodal_example01
import multimodal_example02


def test_gemini_describe_http_video_example() -> None:
    text = gemini_describe_http_video_example.generate_content()
    assert len(text) > 0


def test_gemini_youtube_video_key_moments_example() -> None:
    text = gemini_youtube_video_key_moments_example.generate_content()
    assert len(text) > 0


def test_gemini_youtube_video_summarization_example() -> None:
    text = gemini_youtube_video_summarization_example.generate_content()
    assert len(text) > 0


def test_analyze_all_modalities() -> None:
    text = multimodal_example01.analyze_all_modalities()
    assert len(text) > 0


def test_stream_multi_modality_basic() -> None:
    responses = multimodal_example02.generate_content()
    assert responses
