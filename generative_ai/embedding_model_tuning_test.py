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

import os

import backoff

from google.api_core.exceptions import FailedPrecondition
import google.auth
from google.cloud import aiplatform
from google.cloud.aiplatform import initializer as aiplatform_init
from google.cloud.aiplatform import pipeline_jobs


import embedding_model_tuning


@backoff.on_exception(backoff.expo, FailedPrecondition, max_time=300)
def dispose(job: pipeline_jobs.PipelineJob) -> None:
    if not job.done():
        job.cancel()
    job.delete()


def test_tune_embedding_model() -> None:
    credentials, _ = google.auth.default(  # Set explicit credentials with Oauth scopes.
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    aiplatform.init(
        api_endpoint="us-central1-aiplatform.googleapis.com:443",
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        staging_bucket="gs://ucaip-samples-us-central1/training_pipeline_output",
        credentials=credentials,
    )
    job = embedding_model_tuning.tune_embedding_model(
        aiplatform_init.global_config.api_endpoint,
        aiplatform_init.global_config.project,
        aiplatform_init.global_config.staging_bucket,
    )
    try:
        assert job.state != "PIPELINE_STATE_FAILED"
    finally:
        dispose(job)
