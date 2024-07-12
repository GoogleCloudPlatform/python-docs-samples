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
from google.api_core.exceptions import ResourceExhausted

import multimodal_embedding_image_video_text


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_multimodal_embedding_image_video_text() -> None:
    embeddings = multimodal_embedding_image_video_text.get_image_video_text_embeddings()
    assert embeddings is not None
    assert embeddings.image_embedding is not None
    assert embeddings.video_embeddings is not None
    assert embeddings.text_embedding is not None
