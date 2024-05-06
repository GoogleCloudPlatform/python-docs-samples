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

import tuning_basic
import tuning_advanced
import list_tunning_job
import get_tunning_job
import cancel_tunning_job


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
MODEL_ID = "gemini-1.5-pro-preview-0409"
TUNING_JOB_ID = "tuning_job_ID"


def test_tuning_basic() -> None:
    response = tuning_basic.generate_content(PROJECT_ID, REGION)
    assert response


def test_tuning_advanced() -> None:
    response = tuning_advanced.generate_content(PROJECT_ID, REGION)
    assert response
    
    
def test_list_tunning_job() -> None:
    response = list_tunning_job.generate_content(PROJECT_ID, REGION)
    assert response
    

def test_get_tunning_job() -> None:
    response = get_tunning_job.generate_content(PROJECT_ID, REGION, TUNING_JOB_ID)
    assert response
    

def test_cancel_tunning_job() -> None:
    response = cancel_tunning_job.generate_content(PROJECT_ID, REGION, TUNING_JOB_ID)
    assert response






