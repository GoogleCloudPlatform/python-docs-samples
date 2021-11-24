# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff

from google.api_core.exceptions import RetryError
from google.cloud import storage_transfer
from google.protobuf.duration_pb2 import Duration
import googleapiclient.discovery
from googleapiclient.errors import HttpError

import get_transfer_job_with_retries
import get_transfer_job_with_retries_apiary

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


@backoff.on_exception(backoff.expo, (RetryError,), max_time=60)
def test_get_transfer_job_with_retries(capsys):
    client = storage_transfer.StorageTransferServiceClient()
    transfer_job = {
        "description": "Sample job",
        "status": "ENABLED",
        "project_id": project_id,
        "schedule": {
            "schedule_start_date": {
                "day": 1, "month": 1, "year": 2000},
            "start_time_of_day": {
                "hours": 0, "minutes": 0, "seconds": 0},
        },
        "transfer_spec": {
            "gcs_data_source": {
                "bucket_name": f"{project_id}-storagetransfer-source"},
            "gcs_data_sink": {
                "bucket_name": f"{project_id}-storagetransfer-sink"},
            "object_conditions": {
                'min_time_elapsed_since_last_modification': Duration(
                    seconds=2592000  # 30 days
                )
            },
            "transfer_options": {
                "delete_objects_from_source_after_transfer": True},
        },
    }
    result = client.create_transfer_job({"transfer_job": transfer_job})

    job_name = result.name
    max_retry_duration = 120

    get_transfer_job_with_retries.get_transfer_job_with_retries(
        project_id, job_name, max_retry_duration
    )
    out, _ = capsys.readouterr()
    # This sample isn't really meant to do anything, just check that it ran
    # without any issues when we populated num_retries
    assert f"max retry duration of {max_retry_duration}s" in out


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_get_transfer_job_with_retries_apiary(capsys):
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")
    transfer_job = {
        "description": "Sample job",
        "status": "ENABLED",
        "projectId": project_id,
        "schedule": {
            "scheduleStartDate": {
                "day": "01", "month": "01", "year": "2000"},
            "startTimeOfDay": {
                "hours": "00", "minutes": "00", "seconds": "00"},
        },
        "transferSpec": {
            "gcsDataSource": {
                "bucketName": f"{project_id}-storagetransfer-source"},
            "gcsDataSink": {
                "bucketName": f"{project_id}-storagetransfer-sink"},
            "objectConditions": {
                "minTimeElapsedSinceLastModification": "2592000s"  # 30 days
            },
            "transferOptions": {
                "deleteObjectsFromSourceAfterTransfer": "true"},
        },
    }

    result = storagetransfer.transferJobs().create(body=transfer_job).execute()

    job_name = result.get("name")
    retries = 3

    get_transfer_job_with_retries_apiary.get_transfer_job_with_retries(
        project_id, job_name, retries
    )
    out, _ = capsys.readouterr()
    # This sample isn't really meant to do anything, just check that it ran
    # without any issues when we populated num_retries
    assert f"using {str(retries)} retries" in out
