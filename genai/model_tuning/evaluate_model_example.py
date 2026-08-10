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

# [START aiplatform_genai_evaluate_model]
import os

import vertexai
from vertexai.evaluation import EvalResult, EvalTask

# TODO (Developer) Set environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")


def evaluate_model() -> EvalResult:
    """Evaluate the performance of a generative AI model."""

    vertexai.init(project=PROJECT_ID, location=LOCATION_ID)

    # Dataset URI containing input prompts and ground truth labels
    dataset_uri = "gs://cloud-samples-data/ai-platform/generative_ai/llm_classification_bp_input_prompts_with_ground_truth.jsonl"

    metric_column_mapping = {"reference": "ground_truth"}

    # Define evaluation task
    eval_task = EvalTask(
        dataset=dataset_uri,
        metrics=["exact_match"],
        experiment="gemini-classification-eval",
        metric_column_mapping=metric_column_mapping,
    )

    # Define a prompt template so the generative Gemini model produces formatted labels
    prompt_template = (
        "Classify the following text into exactly one category from "
        "[nature, news, sports, health, startups]. Return only the category name:\n\n{prompt}"
    )

    # Evaluate using a modern Gemini model
    eval_result = eval_task.evaluate(
        model=MODEL_NAME,
        prompt_template=prompt_template,
    )

    print("=== SUMMARY METRICS ===")
    print(eval_result.summary_metrics)

    print("\n=== METRICS TABLE SAMPLE ===")
    print(eval_result.metrics_table.head())

    return eval_result


# [END aiplatform_genai_evaluate_model]
