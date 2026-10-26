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
from typing import List

from agentplatform import types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def import_files(
    corpus_name: str,
    paths: List[str],
) -> types.ImportRagFilesResponse:
    """Imports files from Google Cloud Storage into a RAG corpus."""
    # [START generativeaionvertexai_rag_import_files]

    import agentplatform
    from agentplatform import types

    from google.genai import types as genai_types

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-east5/ragCorpora/{rag_corpus_id}"
    # paths = ["gs://my_bucket/my_files_dir/*"]

    # Initialize Agent Platform client once per session.
    # See https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview#supported-regions
    client = agentplatform.Client(project=PROJECT_ID, location="us-east5")

    response = client.rag.import_files(
        name=corpus_name,
        import_config=types.ImportRagFilesConfig(
            gcs_source=genai_types.GcsSource(uris=paths),
            rag_file_transformation_config=types.RagFileTransformationConfig(
                rag_file_chunking_config=types.RagFileChunkingConfig(
                    chunk_size=512,
                    chunk_overlap=100,
                )
            ),  # optional
            max_embedding_requests_per_min=900,  # optional
        ),
    )

    print(f"Imported {response.imported_rag_files_count} files.")
    # Example response:
    # Imported 2 files.

    # [END generativeaionvertexai_rag_import_files]
    return response


if __name__ == "__main__":
    gcloud_path = "gs://your-bucket-name/file.txt"
    import_files(
        corpus_name=f"projects/{PROJECT_ID}/locations/us-east5/ragCorpora/{{rag_corpus_id}}",
        paths=[gcloud_path],
    )
