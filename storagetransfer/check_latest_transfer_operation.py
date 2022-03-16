#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Command-line sample that checks the latest transfer operation for a given
transfer job.
"""


import argparse

# [START storagetransfer_get_latest_transfer_operation]
from google.cloud import storage_transfer


def check_latest_transfer_operation(project_id: str, job_name: str):
    """Checks the latest transfer operation for a given transfer job."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # Storage Transfer Service job name
    # job_name = 'transferJobs/1234567890'

    transfer_job = client.get_transfer_job({
        'project_id': project_id,
        'job_name': job_name,
    })

    if transfer_job.latest_operation_name:
        response = client.transport.operations_client.get_operation(
            transfer_job.latest_operation_name)
        operation = storage_transfer.TransferOperation.deserialize(
            response.metadata.value)

        print(f"Latest transfer operation for `{job_name}`: {operation}")
    else:
        print(f"Transfer job {job_name} has not ran yet.")


# [END storagetransfer_get_latest_transfer_operation]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--project-id',
        help='The ID of the Google Cloud Platform Project that owns the job',
        required=True)
    parser.add_argument(
        '--job-name',
        help='The transfer job to get',
        required=True)

    args = parser.parse_args()

    check_latest_transfer_operation(**vars(args))
