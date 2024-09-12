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
import backoff

import code_retrieval_example
import document_retrieval_example

from google.api_core.exceptions import ResourceExhausted


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_text_embed_text() -> None:
    texts = [
        "banana bread?",
        "banana muffin?",
        "banana?",
    ]
    dimensionality = 256
    embeddings = document_retrieval_example.embed_text(
        texts, "RETRIEVAL_QUERY", dimensionality
    )
    assert [len(e) for e in embeddings] == [dimensionality or 768] * len(texts)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_embed_text() -> None:
    texts = [
        "banana bread?",
        "banana muffin?",
        "banana?",
    ]
    dimensionality = 256
    embeddings = code_retrieval_example.embed_text(
        texts=texts,
        task="CODE_RETRIEVAL_QUERY",
        dimensionality=dimensionality,
    )
    assert [len(e) for e in embeddings] == [dimensionality or 768] * len(texts)
