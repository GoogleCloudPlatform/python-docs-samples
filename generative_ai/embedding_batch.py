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

# TODO: Delete this file after approving /embeddings/batch_example.py
import os

from google.cloud.aiplatform import BatchPredictionJob


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
OUTPUT_URI = os.getenv("GCS_OUTPUT_URI")


def embed_text_batch() -> BatchPredictionJob:
    """Example of how to generate embeddings from text using batch processing.

    Read more: https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/batch-prediction-genai-embeddings
    """
    # [START generativeaionvertexai_sdk_embedding_batch]
    import vertexai
    from vertexai.preview import language_models

    # TODO(developer): Update variables
    vertexai.init(project=PROJECT_ID, location="us-central1")
    input_uri = (
        "gs://cloud-samples-data/generative-ai/embeddings/embeddings_input.jsonl"
    )
    # Format: `gs://BUCKET_NAME/DIRECTORY/` or `bq://project_name.llm_dataset`
    output_uri = OUTPUT_URI

    textembedding_model = language_models.TextEmbeddingModel.from_pretrained(
        "textembedding-gecko"
    )

    batch_prediction_job = textembedding_model.batch_predict(
        dataset=[input_uri],
        destination_uri_prefix=output_uri,
    )
    print(batch_prediction_job.display_name)
    print(batch_prediction_job.resource_name)
    print(batch_prediction_job.state)

    # [END generativeaionvertexai_sdk_embedding_batch]

    return batch_prediction_job


if __name__ == "__main__":
    embed_text_batch()
