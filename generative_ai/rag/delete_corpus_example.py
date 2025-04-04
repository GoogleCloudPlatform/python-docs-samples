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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def delete_corpus(corpus_name: str) -> None:
    # [START generativeaionvertexai_rag_delete_corpus]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    rag.delete_corpus(name=corpus_name)
    print(f"Corpus {corpus_name} deleted.")
    # Example response:
    # Successfully deleted the RagCorpus.
    # Corpus projects/[PROJECT_ID]/locations/us-central1/ragCorpora/123456789012345 deleted.

    # [END generativeaionvertexai_rag_delete_corpus]


if __name__ == "__main__":
    delete_corpus(
        "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    )
