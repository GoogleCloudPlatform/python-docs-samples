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
Command-line sample that creates a one-time transfer from a Google Cloud
Storage bucket to another.
"""


import argparse

# [START storagetransfer_quickstart]
from google.cloud import storage_transfer


def create_one_time_transfer(project_id: str = "my_project_id",
                             source_bucket: str = "my_source_bucket",
                             sink_bucket: str = "my_sink_bucket"):
    """Creates a one-time transfer job."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # Google Cloud Storage source bucket name
    # source_bucket = 'my-gcs-source-bucket'

    # Google Cloud Storage destination bucket name
    # sink_bucket = 'my-gcs-destination-bucket'

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'transfer_spec': {
                'gcs_data_source': {
                    'bucket_name': source_bucket,
                },
                'gcs_data_sink': {
                    'bucket_name': sink_bucket,
                }
            }
        }
    })

    transfer_job = client.create_transfer_job(transfer_job_request)
    client.run_transfer_job({
        'job_name': transfer_job.name,
        'project_id': project_id
    })

    print(f'Created and ran transfer job: {transfer_job.name}')


# [END storagetransfer_quickstart]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--project-id',
        help='The ID of the Google Cloud Platform Project that owns the job',
        required=False)
    parser.add_argument(
        '--source-bucket',
        help='S3 source bucket name',
        required=False)
    parser.add_argument(
        '--sink-bucket',
        help='Cloud Storage bucket name',
        required=False)

    args = parser.parse_args()

    if args.project_id is None and args.source_bucket is None and args.sink_bucket is None:
        create_one_time_transfer()
    else:
        create_one_time_transfer(**vars(args))
