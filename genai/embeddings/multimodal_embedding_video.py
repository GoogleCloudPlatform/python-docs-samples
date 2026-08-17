# Copyright 2026 Google LLC
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

# [START googlegenaisdk_multimodal_embedding_video]
from google import genai
from google.genai import types


def embed_content() -> types.EmbedContentResponse:
    client = genai.Client()

    part = types.Part(
        file_data=types.FileData(
            file_uri="gs://cloud-samples-data/vertex-ai-vision/highway_vehicles.mp4",
            mime_type="video/mp4",
        ),
        video_metadata=types.VideoMetadata(end_offset="1s"),
    )

    content = types.Content(parts=[part])

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=[content],
    )
    print(response)
    # Example response:
    # embeddings=[ContentEmbedding(values=[-0.0123147098, 0.0727171078, ...])]
    return response


# [END googlegenaisdk_multimodal_embedding_video]
