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

# [START generativeaionvertexai_embedding_model_tuning]
import re

from google.cloud.aiplatform import initializer as aiplatform_init
from vertexai.language_models import TextEmbeddingModel


def tune_embedding_model(
    api_endpoint: str,
    base_model_name: str = "text-embedding-005",
    corpus_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/corpus.jsonl",
    queries_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/queries.jsonl",
    train_label_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/train.tsv",
    test_label_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/test.tsv",
):  # noqa: ANN201
    """Tune an embedding model using the specified parameters.
    Args:
        api_endpoint (str): The API endpoint for the Vertex AI service.
        base_model_name (str): The name of the base model to use for tuning.
        corpus_path (str): GCS URI of the JSONL file containing the corpus data.
        queries_path (str): GCS URI of the JSONL file containing the queries data.
        train_label_path (str): GCS URI of the TSV file containing the training labels.
        test_label_path (str): GCS URI of the TSV file containing the test labels.
    """
    match = re.search(r"^(\w+-\w+)", api_endpoint)
    location = match.group(1) if match else "us-central1"
    base_model = TextEmbeddingModel.from_pretrained(base_model_name)
    tuning_job = base_model.tune_model(
        task_type="DEFAULT",
        corpus_data=corpus_path,
        queries_data=queries_path,
        training_data=train_label_path,
        test_data=test_label_path,
        batch_size=128,  # The batch size to use for training.
        train_steps=1000,  # The number of training steps.
        tuned_model_location=location,
        output_dimensionality=768,  # The dimensionality of the output embeddings.
        learning_rate_multiplier=1.0,  # The multiplier for the learning rate.
    )
    return tuning_job


# [END generativeaionvertexai_embedding_model_tuning]
if __name__ == "__main__":
    tune_embedding_model(aiplatform_init.global_config.api_endpoint)
