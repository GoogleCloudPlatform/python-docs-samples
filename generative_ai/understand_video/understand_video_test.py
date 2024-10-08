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

import audio_video_example
import single_turn_video_example


def test_analyze_video_with_audio() -> None:
    text = audio_video_example.analyze_video_with_audio()
    assert len(text) > 0


def test_gemini_single_turn_video_example() -> None:
    text = single_turn_video_example.generate_text()
    text = text.lower()
    assert len(text) > 0
    assert any(
        [_ in text for _ in ("zoo", "tiger", "leaf", "water", "animals", "photos")]
    )
