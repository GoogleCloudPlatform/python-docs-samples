# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import random
import time
from typing import Callable

from google.cloud import aiplatform, storage
from google.cloud.aiplatform import CustomJob
from google.cloud.aiplatform_v1 import JobState
from google.cloud.exceptions import NotFound
from google.cloud.storage import transfer_manager

from prompt_optimizer import optimize_prompts

import pytest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
STAGING_BUCKET_NAME = "prompt_optimizer_bucket"
CONFIGURATION_DIRECTORY = "test_resources"
CONFIGURATION_FILENAME = "sample_configuration.json"
LOCATION = random.choice(["us-central1", "us-east4", "us-west4", "us-west1"])
OUTPUT_PATH = "instruction"

STORAGE_CLIENT = storage.Client()


def _clean_resources(bucket_resource_name: str) -> None:
    # delete blobs and bucket if exists
    try:
        bucket = STORAGE_CLIENT.get_bucket(bucket_resource_name)
    except NotFound:
        print(f"Bucket {bucket_resource_name} cannot be accessed")
        return

    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
    bucket.delete()


def substitute_env_variable(data: dict, target_key: str, env_var_name: str) -> dict:
    # substitute env variables in the given config file with runtime values
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                data[key] = os.environ.get(env_var_name)
            else:
                data[key] = substitute_env_variable(value, target_key, env_var_name)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            data[i] = substitute_env_variable(value, target_key, env_var_name)
    return data


def update_json() -> dict:
    # Load the JSON file
    file_path = os.path.join(
        os.path.dirname(__file__), CONFIGURATION_DIRECTORY, CONFIGURATION_FILENAME
    )
    with open(file_path, "r") as f:
        data = json.load(f)
    # Substitute only the "project" variable with the value of "PROJECT_ID"
    substituted_data = substitute_env_variable(data, "project", "PROJECT_ID")
    return substituted_data


@pytest.fixture(scope="session")
def bucket_name() -> str:
    filenames = [
        "sample_prompt_template.txt",
        "sample_prompts.jsonl",
        "sample_system_instruction.txt",
    ]
    # cleanup existing stale resources
    _clean_resources(STAGING_BUCKET_NAME)
    # create bucket
    bucket = STORAGE_CLIENT.bucket(STAGING_BUCKET_NAME)
    bucket.storage_class = "STANDARD"
    new_bucket = STORAGE_CLIENT.create_bucket(bucket, location="us")
    # update JSON to substitute env variables
    substituted_data = update_json()
    # convert the JSON data to a byte string
    json_str = json.dumps(substituted_data, indent=2)
    json_bytes = json_str.encode("utf-8")
    # upload substituted JSON file to the bucket
    blob = bucket.blob(CONFIGURATION_FILENAME)
    blob.upload_from_string(json_bytes)
    # upload config files to the bucket
    transfer_manager.upload_many_from_filenames(
        new_bucket,
        filenames,
        source_directory=os.path.join(
            os.path.dirname(__file__), CONFIGURATION_DIRECTORY
        ),
    )
    yield new_bucket.name
    _clean_resources(new_bucket.name)


def _main_test(test_func: Callable) -> None:
    job_resource_name: str = ""
    timeout = 900  # seconds
    # wait for the job to complete
    try:
        job_resource_name = test_func()
        start_time = time.time()
        while (
            get_job(job_resource_name).state
            not in [JobState.JOB_STATE_SUCCEEDED, JobState.JOB_STATE_FAILED]
            and time.time() - start_time < timeout
        ):
            time.sleep(10)
    finally:
        # delete job
        get_job(job_resource_name).delete()


def test_prompt_optimizer(bucket_name: pytest.fixture()) -> None:
    _main_test(
        test_func=lambda: optimize_prompts(
            PROJECT_ID,
            LOCATION,
            f"gs://{bucket_name}",
            f"gs://{bucket_name}/{CONFIGURATION_FILENAME}",
        )
    )
    assert (
        STORAGE_CLIENT.get_bucket(bucket_name).list_blobs(prefix=OUTPUT_PATH)
        is not None
    )


def get_job(job_resource_name: str) -> CustomJob:
    return aiplatform.CustomJob.get(
        resource_name=job_resource_name, project=PROJECT_ID, location=LOCATION
    )
