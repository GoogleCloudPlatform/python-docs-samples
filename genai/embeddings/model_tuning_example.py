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

# [START aiplatform_genai_embedding_model_tuning]
import os

from google.cloud import aiplatform

# TODO (Developer) set the following environment variables.
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "text-embedding-004")
# A storage bucket: gs://your-bucket-name/embedding-tuning-output
OUTPUT_URI = os.getenv("OUTPUT_DIR")

API_ENDPOINT = f"{LOCATION_ID}-aiplatform.googleapis.com"
BATCH_SIZE = 128
LEARNING_RATE_MULTIPLIER = 1.0
TRAIN_LABEL_PATH = (
    "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/train.tsv"
)
TEST_LABEL_PATH = (
    "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/test.tsv"
)
CORPUS_PATH = (
    "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/corpus.jsonl"
)
QUERIES_PATH = (
    "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/queries.jsonl"
)

ACCELERATOR_TYPE = "NVIDIA_L4"

# Official Google Cloud KFP pipeline template URI for text embedding model tuning
EMBEDDING_TUNING_PIPELINE_URI = "https://us-kfp.pkg.dev/ml-pipeline/llm-text-embedding/tune-text-embedding-model/v1.1.3"


def tune_embedding_model() -> aiplatform.PipelineJob:
    """Tune an embedding model using the specified parameters."""

    aiplatform.init(project=PROJECT_ID, location=LOCATION_ID)

    # Configure parameters expected by the embedding tuning pipeline template
    pipeline_parameters = {
        "base_model_version_id": MODEL_NAME,
        "corpus_path": CORPUS_PATH,
        "queries_path": QUERIES_PATH,
        "train_label_path": TRAIN_LABEL_PATH,
        "test_label_path": TEST_LABEL_PATH,
        "batch_size": BATCH_SIZE,
        "accelerator_type": ACCELERATOR_TYPE,
    }

    # Instantiate the Vertex AI Pipeline job
    pipeline_job = aiplatform.PipelineJob(
        display_name="tune-text-embedding-model-job",
        template_path=EMBEDDING_TUNING_PIPELINE_URI,
        pipeline_root=OUTPUT_URI,
        parameter_values=pipeline_parameters,
        project=PROJECT_ID,
        location=LOCATION_ID,
    )

    pipeline_job.submit()

    print(f"Pipeline submitted successfully: {pipeline_job.resource_name}")

    return pipeline_job


# [END aiplatform_genai_embedding_model_tuning]
