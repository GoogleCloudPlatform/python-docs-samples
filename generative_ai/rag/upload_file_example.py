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

from typing import Optional

from vertexai import rag

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def upload_file(
    corpus_name: str,
    path: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
) -> rag.RagFile:
    # [START generativeaionvertexai_rag_upload_file]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    # path = "path/to/local/file.txt"
    # display_name = "file_display_name"
    # description = "file description"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=path,
        display_name=display_name,
        description=description,
    )
    print(rag_file)
    # RagFile(name='projects/[PROJECT_ID]/locations/us-central1/ragCorpora/1234567890/ragFiles/09876543',
    #  display_name='file_display_name', description='file description')

    # [END generativeaionvertexai_rag_upload_file]
    return rag_file


if __name__ == "__main__":
    upload_file(
        corpus_name="projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}",
        path="path/to/file.txt",
        display_name="file_display_name",
        description="file description",
    )
