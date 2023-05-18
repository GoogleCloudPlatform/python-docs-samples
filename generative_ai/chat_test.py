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
# WITHcontent WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import chat


def test_science_tutoring() -> None:
    content = chat.science_tutoring(temperature=0).text
    assert "Mercury" in content
    assert "Venus" in content
    assert "Earth" in content
    assert "Mars" in content
    assert "Jupiter" in content
    assert "Saturn" in content
    assert "Uranus" in content
    assert "Neptune" in content
