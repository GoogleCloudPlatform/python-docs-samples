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

from google.cloud.aiplatform_v1beta1 import RetrieveContextsResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def retrieval_query(
    corpus_name: str,
) -> RetrieveContextsResponse:
    # [START generativeaionvertexai_rag_retrieval_query]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/[PROJECT_ID]/locations/us-central1/ragCorpora/[rag_corpus_id]"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus_name,
                # Optional: supply IDs from `rag.list_files()`.
                # rag_file_ids=["rag-file-1", "rag-file-2", ...],
            )
        ],
        text="Hello World!",
        rag_retrieval_config=rag.RagRetrievalConfig(
            top_k=10,
            filter=rag.utils.resources.Filter(vector_distance_threshold=0.5),
        ),
    )
    print(response)
    # Example response:
    # contexts {
    #   contexts {
    #     source_uri: "gs://your-bucket-name/file.txt"
    #     text: "....
    #   ....

    # [END generativeaionvertexai_rag_retrieval_query]

    return response


if __name__ == "__main__":
    retrieval_query(
        "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    )
