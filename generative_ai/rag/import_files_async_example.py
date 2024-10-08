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

from google.cloud.aiplatform_v1beta1 import ImportRagFilesResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


async def import_files_async(
    corpus_name: str,
    paths: List[str],
) -> ImportRagFilesResponse:
    # [START generativeaionvertexai_rag_import_files_async]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Supports Google Cloud Storage and Google Drive Links
    # paths = ["https://drive.google.com/file/d/123", "gs://my_bucket/my_files_dir"]

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    response = await rag.import_files_async(
        corpus_name=corpus_name,
        paths=paths,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
        max_embedding_requests_per_min=900,  # Optional
    )

    result = await response.result()
    print(f"Imported {result.imported_rag_files_count} files.")
    # Example response:
    # Imported 2 files.

    # [END generativeaionvertexai_rag_import_files_async]
    return result


if __name__ == "__main__":
    import asyncio

    gdrive_path = "https://drive.google.com/file/1234567890"
    gcloud_path = "gs://your-bucket-name/file.txt"
    asyncio.run(
        import_files_async(
            corpus_name="projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}",
            paths=[gdrive_path, gcloud_path],
        )
    )
