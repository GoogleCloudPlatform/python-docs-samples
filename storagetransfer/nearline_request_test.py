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

from datetime import datetime
import json
import uuid
import warnings

import backoff
from google.api_core.exceptions import RetryError
from google.cloud import storage_transfer
from google.cloud.storage import Bucket
from googleapiclient.errors import HttpError
import pytest

import nearline_request
import nearline_request_apiary


@pytest.fixture()
def job_description(project_id: str):
    # Create description
    client = storage_transfer.StorageTransferServiceClient()
    description = f"Storage Transfer Service Samples Test - {uuid.uuid4().hex}"

    yield description

    # Remove job based on description as the job's name isn't predetermined
    try:
        transfer_job_name = ''

        transfer_jobs = client.list_transfer_jobs({
            'filter': json.dumps({
                "projectId": project_id,
                "jobStatuses": [
                    storage_transfer.TransferJob.Status.ENABLED.name
                ]
            })
        })

        for transfer_job in transfer_jobs:
            if transfer_job.description == description:
                transfer_job_name = transfer_job.name
                break

        client.update_transfer_job({
            "job_name": transfer_job_name,
            "project_id": project_id,
            "transfer_job": {
                "status": storage_transfer.TransferJob.Status.DELETED
            }
        })
    except Exception as e:
        warnings.warn(f"Exception while cleaning up transfer job: {e}")


@backoff.on_exception(backoff.expo, (RetryError,), max_time=60)
def test_nearline_request(
        capsys, project_id: str, source_bucket: Bucket,
        destination_bucket: Bucket, job_description: str):

    nearline_request.create_daily_nearline_30_day_migration(
        project_id=project_id,
        description=job_description,
        source_bucket=source_bucket.name,
        sink_bucket=destination_bucket.name,
        start_date=datetime.utcnow()
    )

    out, _ = capsys.readouterr()

    assert "Created transferJob" in out


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_nearline_request_apiary(
        capsys, project_id: str, source_bucket: Bucket,
        destination_bucket: Bucket, job_description: str):

    nearline_request_apiary.main(
        description=job_description,
        project_id=project_id,
        start_date=datetime.utcnow(),
        start_time=datetime.utcnow(),
        source_bucket=source_bucket.name,
        sink_bucket=destination_bucket.name
    )

    out, _ = capsys.readouterr()

    assert "Returned transferJob" in out
