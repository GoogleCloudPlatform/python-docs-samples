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

from agentplatform import types

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_files(corpus_name: str) -> types.ListRagFilesResponse:
    # [START generativeaionvertexai_rag_list_files]

    import agentplatform

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # corpus_name = "projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Agent Platform client once per session
    client = agentplatform.Client(project=PROJECT_ID, location="us-central1")

    files_response = client.rag.list_files(name=corpus_name)
    for file in files_response.rag_files:
        print(file.display_name)
        print(file.name)
    # Example response:
    # g-drive_file.txt
    # projects/1234567890/locations/us-central1/ragCorpora/111111111111/ragFiles/222222222222
    # g_cloud_file.txt
    # projects/1234567890/locations/us-central1/ragCorpora/111111111111/ragFiles/333333333333

    # [END generativeaionvertexai_rag_list_files]
    return files


if __name__ == "__main__":
    list_files("projects/{PROJECT_ID}/locations/us-central1/ragCorpora/{rag_corpus_id}")
