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

from google.cloud.aiplatform_v1 import RagFile

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_file(file_name: str) -> RagFile:
    # [START generativeaionvertexai_rag_get_file]

    from vertexai import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # file_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}/ragFiles/{rag_file_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=PROJECT_ID, location="us-central1")

    rag_file = rag.get_file(name=file_name)
    print(rag_file)
    # Example response:
    # RagFile(name='projects/1234567890/locations/us-central1/ragCorpora/11111111111/ragFiles/22222222222',
    # display_name='file_display_name', description='file description')

    # [END generativeaionvertexai_rag_get_file]

    return rag_file


if __name__ == "__main__":
    get_file(
        "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}/ragFiles/{rag_file_id}"
    )
