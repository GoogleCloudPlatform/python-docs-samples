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
Command-line sample that creates a one-time transfer from Amazon S3 to
Google Cloud Storage.
"""


import argparse

# [START storagetransfer_transfer_from_aws]
from datetime import datetime

from google.cloud import storage_transfer


def create_one_time_aws_transfer(
        project_id: str, description: str,
        source_bucket: str, aws_access_key_id: str,
        aws_secret_access_key: str, sink_bucket: str):
    """Creates a one-time transfer job from Amazon S3 to Google Cloud
    Storage."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # AWS S3 source bucket name
    # source_bucket = 'my-s3-source-bucket'

    # AWS Access Key ID
    # aws_access_key_id = 'AKIA...'

    # AWS Secret Access Key
    # aws_secret_access_key = 'HEAoMK2.../...ku8'

    # Google Cloud Storage destination bucket name
    # sink_bucket = 'my-gcs-destination-bucket'

    now = datetime.utcnow()
    # Setting the start date and the end date as
    # the same time creates a one-time transfer
    one_time_schedule = {
        'day': now.day,
        'month': now.month,
        'year': now.year
    }

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'schedule': {
                'schedule_start_date': one_time_schedule,
                'schedule_end_date': one_time_schedule
            },
            'transfer_spec': {
                'aws_s3_data_source': {
                    'bucket_name': source_bucket,
                    'aws_access_key': {
                        'access_key_id': aws_access_key_id,
                        'secret_access_key': aws_secret_access_key,
                    }
                },
                'gcs_data_sink': {
                    'bucket_name': sink_bucket,
                }
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_transfer_from_aws]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--project-id',
        help='The ID of the Google Cloud Platform Project that owns the job',
        required=True)
    parser.add_argument(
        '--description',
        help='A useful description for your transfer job',
        default='My transfer job')
    parser.add_argument(
        '--source-bucket',
        help='AWS S3 source bucket name',
        required=True)
    parser.add_argument(
        '--aws-access-key-id',
        help='AWS access key ID',
        required=True)
    parser.add_argument(
        '--aws-secret-access-key',
        help='AWS secret access key',
        required=True)
    parser.add_argument(
        '--sink-bucket',
        help='Google Cloud Storage destination bucket name',
        required=True)

    args = parser.parse_args()

    create_one_time_aws_transfer(**vars(args))
