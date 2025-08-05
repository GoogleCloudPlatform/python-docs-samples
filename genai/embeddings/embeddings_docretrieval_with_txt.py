# Copyright 2025 Google LLC
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


def embed_content() -> str:
    # [START googlegenaisdk_embeddings_docretrieval_with_txt]
    from google import genai
    from google.genai.types import EmbedContentConfig

    client = genai.Client()
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents="How do I get a driver's license/learner's permit?",
        config=EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",  # Optional
            output_dimensionality=3072,  # Optional
            title="Driver's License",  # Optional
        ),
    )
    print(response)
    # Example response:
    # embeddings=[ContentEmbedding(values=[-0.06302902102470398, 0.00928034819662571, 0.014716853387653828, -0.028747491538524628, ... ],
    # statistics=ContentEmbeddingStatistics(truncated=False, token_count=13.0))]
    # metadata=EmbedContentMetadata(billable_character_count=112)
    # [END googlegenaisdk_embeddings_docretrieval_with_txt]
    return response


if __name__ == "__main__":
    embed_content()
