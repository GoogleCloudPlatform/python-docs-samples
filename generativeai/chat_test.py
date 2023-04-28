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

import pytest

from google.cloud.aiplatform.private_preview.language_models import ChatModel, InputOutputTextPair

import chat


def test_science_tutoring(capsys):
    chat.science_tutoring(temperature=0)
    out, _ = capsys.readouterr()
    assert "Mercury" in out
    assert "Venus" in out
    assert "Earth" in out
    assert "Mars" in out
    assert "Jupiter" in out
    assert "Saturn" in out
    assert "Uranus" in out
    assert "Neptune" in out