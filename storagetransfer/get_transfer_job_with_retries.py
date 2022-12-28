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
Command-line sample that gets the latest transfer operation for a given
transfer job with request retry configuration.
"""


import argparse

# [START storagetransfer_create_retry_handler]
from google.api_core.retry import Retry
from google.cloud import storage_transfer


def get_transfer_job_with_retries(
        project_id: str, job_name: str, max_retry_duration: float):
    """
    Check the latest transfer operation associated with a transfer job with
    retries.
    """

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # Storage Transfer Service job name
    # job_name = 'transferJobs/1234567890'

    # The maximum amount of time to delay in seconds
    # max_retry_duration = 60

    transfer_job = client.get_transfer_job({
        'project_id': project_id,
        'job_name': job_name,
    },
        retry=Retry(maximum=max_retry_duration)
    )

    print(f"Fetched transfer job: {transfer_job.name} "
          f"with a max retry duration of {max_retry_duration}s")


# [END storagetransfer_create_retry_handler]

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
    parser.add_argument(
        '--max-retry-duration',
        help='The maximum amount of time to delay in seconds',
        type=float,
        default=60)

    args = parser.parse_args()

    get_transfer_job_with_retries(**vars(args))
