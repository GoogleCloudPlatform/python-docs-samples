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

import get_document


def test_get_document(capsys):
    name = "documents/docs.cloud.google.com/storage/docs/creating-buckets"
    doc = get_document.get_document(name=name)
    out, _ = capsys.readouterr()

    assert doc is not None
    assert doc.name == name
    assert len(doc.title) > 0
    assert len(doc.content) > 0
    assert "Title:" in out
