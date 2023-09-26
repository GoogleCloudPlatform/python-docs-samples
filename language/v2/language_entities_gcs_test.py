#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import language_entities_gcs


def test_sample_analyze_entities_gcs(capsys: ...) -> None:
    assert os.environ["GOOGLE_CLOUD_PROJECT"] != ""

    language_entities_gcs.sample_analyze_entities()
    captured = capsys.readouterr()
    assert "Representative name for the entity: " in captured.out
    assert "Entity type: " in captured.out
    assert "Mention text: " in captured.out
    assert "Mention type: " in captured.out
    assert "Probability score: " in captured.out
    assert "Language of the text: " in captured.out
