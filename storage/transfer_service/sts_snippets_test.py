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

import googleapiclient.discovery

import check_latest_transfer_operation
import get_transfer_job_with_retries


def test_latest_transfer_operation(capsys):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    transfer_job = {
        "description": "Sample job",
        "status": "ENABLED",
        "projectId": project_id,
        "schedule": {
            "scheduleStartDate": {"day": "01", "month": "01", "year": "2000"},
            "startTimeOfDay": {"hours": "00", "minutes": "00", "seconds": "00"},
        },
        "transferSpec": {
            "gcsDataSource": {"bucketName": project_id + "-storagetransfer-source"},
            "gcsDataSink": {"bucketName": project_id + "-storagetransfer-sink"},
            "objectConditions": {
                "minTimeElapsedSinceLastModification": "2592000s"  # 30 days
            },
            "transferOptions": {"deleteObjectsFromSourceAfterTransfer": "true"},
        },
    }
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")
    result = storagetransfer.transferJobs().create(body=transfer_job).execute()

    job_name = result.get("name")
    check_latest_transfer_operation.check_latest_transfer_operation(
        project_id, job_name
    )
    out, _ = capsys.readouterr()
    # The latest operation field can take a while to populate, so to avoid a
    # flaky test we just check that the job exists and the field was checked
    assert job_name in out


def test_get_transfer_Job_with_retries(capsys):
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    transfer_job = {
        "description": "Sample job",
        "status": "ENABLED",
        "projectId": project_id,
        "schedule": {
            "scheduleStartDate": {"day": "01", "month": "01", "year": "2000"},
            "startTimeOfDay": {"hours": "00", "minutes": "00", "seconds": "00"},
        },
        "transferSpec": {
            "gcsDataSource": {"bucketName": project_id + "-storagetransfer-source"},
            "gcsDataSink": {"bucketName": project_id + "-storagetransfer-sink"},
            "objectConditions": {
                "minTimeElapsedSinceLastModification": "2592000s"  # 30 days
            },
            "transferOptions": {"deleteObjectsFromSourceAfterTransfer": "true"},
        },
    }
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")
    result = storagetransfer.transferJobs().create(body=transfer_job).execute()

    job_name = result.get("name")

    retries = 3

    get_transfer_job_with_retries.get_transfer_job_with_retries(
        project_id, job_name, retries
    )
    out, _ = capsys.readouterr()
    # This sample isn't really meant to do anything, just check that it ran without any issues
    # when we populated num_retries
    assert f"using {str(retries)} retries" in out
