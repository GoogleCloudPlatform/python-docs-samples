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

# [START generativeaionvertexai_evaluate_model]
import os

from google.auth import default

import vertexai
from vertexai.preview.language_models import (
    EvaluationTextClassificationSpec,
    TextGenerationModel,
)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def evaluate_model() -> object:
    """Evaluate the performance of a generative AI model."""

    # Set credentials for the pipeline components used in the evaluation task
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    vertexai.init(project=PROJECT_ID, location="us-central1", credentials=credentials)

    # Create a reference to a generative AI model
    model = TextGenerationModel.from_pretrained("text-bison@002")

    # Define the evaluation specification for a text classification task
    task_spec = EvaluationTextClassificationSpec(
        ground_truth_data=[
            "gs://cloud-samples-data/ai-platform/generative_ai/llm_classification_bp_input_prompts_with_ground_truth.jsonl"
        ],
        class_names=["nature", "news", "sports", "health", "startups"],
        target_column_name="ground_truth",
    )

    # Evaluate the model
    eval_metrics = model.evaluate(task_spec=task_spec)
    print(eval_metrics)
    # Example response:
    # ...
    # PipelineJob run completed.
    # Resource name: projects/123456789/locations/us-central1/pipelineJobs/evaluation-llm-classification-...
    # EvaluationClassificationMetric(label_name=None, auPrc=0.53833705, auRoc=0.8...

    return eval_metrics


# [END generativeaionvertexai_evaluate_model]


if __name__ == "__main__":
    evaluate_model()
