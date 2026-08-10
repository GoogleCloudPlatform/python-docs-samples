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

import os

from google import genai

import pretrained_codegen_example

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("LOCATION_ID", "us-central1")

JOB_STATES_CANCELLABLE = [
    genai.types.JobState.JOB_STATE_RUNNING,
    genai.types.JobState.JOB_STATE_PENDING,
]
JOB_STATES_DELETABLE = [
    genai.types.JobState.JOB_STATE_SUCCEEDED,
    genai.types.JobState.JOB_STATE_CANCELLED,
    genai.types.JobState.JOB_STATE_FAILED,
]


def test_tuning_code_generation_model() -> None:
    """Validate tuning creation, and cleans after execution."""

    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION_ID)

    tuned_model = None
    job_is_finished = False
    job_is_pending = False

    try:

        tuned_model = pretrained_codegen_example.tune_code_generation_model()

        job_is_pending = tuned_model.state in JOB_STATES_CANCELLABLE
        job_is_finished = tuned_model.state in JOB_STATES_DELETABLE
        result = job_is_finished or job_is_pending

        assert result

    finally:

        # cleanup
        if job_is_pending:
            client.tunings.cancel(name=tuned_model.name)
        if job_is_finished:
            client.models.delete(model=tuned_model.model)
