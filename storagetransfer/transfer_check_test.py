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

import backoff
from google.api_core.exceptions import RetryError
from google.cloud import storage_transfer
from google.cloud.storage import Bucket
from google.protobuf.duration_pb2 import Duration
from googleapiclient.errors import HttpError
import pytest

import transfer_check
import transfer_check_apiary


@pytest.fixture()
def transfer_job(
        project_id: str, source_bucket: Bucket, destination_bucket: Bucket):
    # Create job
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
                "bucket_name": source_bucket.name},
            "gcs_data_sink": {
                "bucket_name": destination_bucket.name},
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
    client.run_transfer_job({
        'job_name': result.name,
        'project_id': project_id
    })

    yield result.name

    # Remove job
    client.update_transfer_job({
        "job_name": result.name,
        "project_id": project_id,
        "transfer_job": {
            "status": storage_transfer.TransferJob.Status.DELETED
        }
    })


@backoff.on_exception(backoff.expo, (RetryError,), max_time=60)
def test_transfer_check(capsys, project_id: str, transfer_job: str):
    transfer_check.transfer_check(project_id, transfer_job)

    out, _ = capsys.readouterr()
    normalized_name = transfer_job.replace('/', '-')

    # This sample isn't really meant to do anything, just check that it ran
    # without any issues while listing `transferOperations`
    assert f"transferOperations/{normalized_name}" in out


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_transfer_check_apiary(capsys, project_id: str, transfer_job: str):
    transfer_check_apiary.main(project_id, transfer_job)

    out, _ = capsys.readouterr()
    normalized_name = transfer_job.replace('/', '-')

    # This sample isn't really meant to do anything, just check that it ran
    # without any issues while listing `transferOperations`
    assert f"transferOperations/{normalized_name}" in out
