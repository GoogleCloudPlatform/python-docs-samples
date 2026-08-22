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

import batch_get_documents


def test_batch_get_documents(capsys):
    names = [
        "documents/docs.cloud.google.com/storage/docs/creating-buckets",
        "documents/docs.cloud.google.com/storage/docs/deleting-buckets",
    ]
    response = batch_get_documents.batch_get_documents(names=names)
    out, _ = capsys.readouterr()

    assert response is not None
    assert len(response.documents) == 2
    for doc in response.documents:
        assert doc.name in names
        assert len(doc.title) > 0
    assert "Title:" in out
