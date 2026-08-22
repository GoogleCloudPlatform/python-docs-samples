# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import answer_query


def test_answer_query(capsys):
    response = answer_query.answer_query(
        query="How to create a Cloud Storage bucket",
    )
    out, _ = capsys.readouterr()

    assert response is not None
    assert response.answer is not None
    assert len(response.answer.answer_text) > 0
    assert "Answer:" in out
