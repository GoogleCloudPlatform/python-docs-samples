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

def generate_content(
    PROJECT_ID: str, REGION: str, MODEL_ID: str
) -> object:
    # [START generativeaionvertexai_text_embedding_advanced]
    import vertexai
    from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

    vertexai.init(project=PROJECT_ID, location=REGION)

    model = TextEmbeddingModel.from_pretrained(MODEL_ID)
    embeddings = model.get_embeddings(
        texts=[
            TextEmbeddingInput(
                text="What is life?", task_type="RETRIEVAL_DOCUMENT", title="life question"
            )
        ],
        auto_truncate=False,
        output_dimensionality=256,
    )

    print("embeddings\n", embeddings)
    # [END generativeaionvertexai_text_embedding_advanced]

    return embeddings
