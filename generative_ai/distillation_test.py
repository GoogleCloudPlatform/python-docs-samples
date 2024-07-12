# Copyright 2023 Google LLC
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
import uuid

from google.cloud import aiplatform
from google.cloud import storage
from google.cloud.aiplatform.compat.types import pipeline_state
import pytest
from vertexai.preview.language_models import TextGenerationModel

import distillation

_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"
_BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]


def get_model_display_name(tuned_model: TextGenerationModel) -> str:
    language_model_tuning_job = tuned_model._job
    pipeline_job = language_model_tuning_job._job
    return dict(pipeline_job._gca_resource.runtime_config.parameter_values)[
        "model_display_name"
    ]


def upload_to_gcs(bucket: str, name: str, data: str) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(name)
    blob.upload_from_string(data)


def download_from_gcs(bucket: str, name: str) -> str:
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(name)
    data = blob.download_as_bytes()
    return "\n".join(data.decode().splitlines()[:10])


def delete_from_gcs(bucket: str, name: str) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(name)
    blob.delete()


@pytest.fixture(scope="function")
def training_data_filename() -> str:
    temp_filename = f"{uuid.uuid4()}.jsonl"
    data = download_from_gcs(
        "cloud-samples-data", "ai-platform/generative_ai/headline_classification.jsonl"
    )
    upload_to_gcs(_BUCKET, temp_filename, data)
    try:
        yield f"gs://{_BUCKET}/{temp_filename}"
    finally:
        delete_from_gcs(_BUCKET, temp_filename)


def teardown_model(
    tuned_model: TextGenerationModel, training_data_filename: str
) -> None:
    for tuned_model_name in tuned_model.list_tuned_model_names():
        model_registry = aiplatform.models.ModelRegistry(model=tuned_model_name)
        if (
            training_data_filename
            in model_registry.get_version_info("1").model_display_name
        ):
            display_name = model_registry.get_version_info("1").model_display_name
            for endpoint in aiplatform.Endpoint.list():
                for _ in endpoint.list_models():
                    if endpoint.display_name == display_name:
                        endpoint.undeploy_all()
                        endpoint.delete()
            aiplatform.Model(model_registry.model_resource_name).delete()


@pytest.mark.skip("Blocked on b/277959219")
def test_distill_model(training_data_filename: str) -> None:
    """Takes approx. 60 minutes."""
    student_model = distillation.distill_model(
        dataset=training_data_filename,
        teacher_model="text-unicorn@001",
        project_id=_PROJECT_ID,
        location=_LOCATION,
        train_steps=1,
        evaluation_dataset=training_data_filename,
    )
    try:
        assert (
            student_model._job.state
            == pipeline_state.PipelineState.PIPELINE_STATE_SUCCEEDED
        )
    finally:
        teardown_model(student_model, training_data_filename)
