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
Command-line sample that list operations for a transfer job.
"""


import argparse

# [START storagetransfer_transfer_check]
import json

from google.cloud import storage_transfer


def transfer_check(project_id: str, job_name: str):
    """
    Lists operations for a transfer job.
    """

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # Storage Transfer Service job name
    # job_name = 'transferJobs/1234567890'

    job_filter = json.dumps({
        'project_id': project_id,
        'job_names': [job_name]
    })

    response = client.transport.operations_client.list_operations(
        "transferOperations", job_filter)
    operations = [
        storage_transfer.TransferOperation.deserialize(
            item.metadata.value
        ) for item in response
    ]

    print(f"Transfer operations for {job_name}`:", operations)

# [END storagetransfer_transfer_check]


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

    transfer_check(**vars(args))
