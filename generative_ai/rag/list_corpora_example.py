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

import os

from google.cloud.aiplatform_v1beta1.services.vertex_rag_data_service.pagers import (
    ListRagCorporaPager,
)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_corpora() -> ListRagCorporaPager:
    # [START generativeaionvertexai_rag_list_corpora]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    corpora = rag.list_corpora()
    print(corpora)
    # Example response:
    # ListRagCorporaPager<rag_corpora {
    #   name: "projects/[PROJECT_ID]/locations/us-central1/ragCorpora/2305843009213693952"
    #   display_name: "test_corpus"
    #   create_time {
    # ...

    # [END generativeaionvertexai_rag_list_corpora]
    return corpora


if __name__ == "__main__":
    list_corpora()
