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

import search_document_chunks


def test_search_document_chunks(capsys):
    response = search_document_chunks.search_document_chunks(
        query="Cloud Storage bucket creation",
        page_size=3,
    )
    out, _ = capsys.readouterr()

    assert response is not None
    assert len(response.results) > 0
    assert response.results[0].parent.startswith("documents/")
    assert len(response.results[0].content) > 0
    assert "Parent Document: documents/" in out
