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

# [START aiplatform_genai_tune_code_generation_model]
import os

from google import genai

# TODO (Developer) Set environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")

# Resource format: 'publishers/google/models/{model_id}'
BASE_MODEL_RESOURCE = "publishers/google/models/gemini-2.5-flash"
TRAINING_DATASET = (
    "gs://cloud-samples-data/ai-platform/generative_ai/gemini/text/sft_train_data.jsonl"
)


def tune_code_generation_model() -> genai.types.TuningJob:
    """Submits a supervised fine-tuning job for a Gemini model on code/text tasks."""

    client = genai.Client(
        enterprise=True,
        project=PROJECT_ID,
        location=LOCATION_ID,
    )

    tuning_job = client.tunings.tune(
        base_model=BASE_MODEL_RESOURCE,
        training_dataset=genai.types.TuningDataset(
            gcs_uri=TRAINING_DATASET,
        ),
        config=genai.types.CreateTuningJobConfig(
            tuned_model_display_name="tuned_gemini_code_model",
            epoch_count=2,
            learning_rate_multiplier=1.0,
        ),
    )

    print(f"Tuning job submitted successfully: {tuning_job.name}")
    print(f"Current State: {tuning_job.state}")

    return tuning_job


# [END aiplatform_genai_tune_code_generation_model]
