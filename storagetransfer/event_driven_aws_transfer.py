#!/usr/bin/env python

# Copyright 2023 Google LLC
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
Command-line sample that creates an event driven transfer between two GCS buckets that tracks an AWS SQS queue.
"""

import argparse

# [START storagetransfer_create_event_driven_aws_transfer]

from google.cloud import storage_transfer


def create_event_driven_aws_transfer(
    project_id: str,
    description: str,
    source_s3_bucket: str,
    sink_gcs_bucket: str,
    sqs_queue_arn: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
):
    """Create an event driven transfer between two GCS buckets that tracks an AWS SQS queue"""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A description of this job
    # description = 'Creates an event-driven transfer that tracks an SQS queue'

    # AWS S3 source bucket name
    # source_s3_bucket = 'my-s3-source-bucket'

    # Google Cloud Storage destination bucket name
    # sink_gcs_bucket = 'my-gcs-destination-bucket'

    # The ARN of the SQS queue to subscribe to
    # pubsub_id = 'arn:aws:sqs:us-east-1:1234567891011:s3-notification-queue'

    # AWS Access Key ID. Should be accessed via environment variable for security purposes.
    # aws_access_key_id = 'AKIA...'

    # AWS Secret Access Key. Should be accessed via environment variable for security purposes.
    # aws_secret_access_key = 'HEAoMK2.../...ku8'

    transfer_job_request = storage_transfer.CreateTransferJobRequest(
        {
            "transfer_job": {
                "project_id": project_id,
                "description": description,
                "status": storage_transfer.TransferJob.Status.ENABLED,
                "transfer_spec": {
                    "aws_s3_data_source": {
                        "bucket_name": source_s3_bucket,
                        "aws_access_key": {
                            "access_key_id": aws_access_key_id,
                            "secret_access_key": aws_secret_access_key,
                        },
                    },
                    "gcs_data_sink": {
                        "bucket_name": sink_gcs_bucket,
                    },
                },
                "event_stream": {
                    "name": sqs_queue_arn,
                },
            },
        }
    )

    result = client.create_transfer_job(transfer_job_request)
    print(f"Created transferJob: {result.name}")


# [END storagetransfer_create_event_driven_aws_transfer]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-id",
        help="The ID of the Google Cloud Platform Project that owns the job",
        required=True,
    )
    parser.add_argument(
        "--description",
        help="A useful description for your transfer job",
        default="My transfer job",
    )
    parser.add_argument(
        "--source-s3-bucket", help="AWS S3 source bucket name", required=True
    )
    parser.add_argument(
        "--sink-gcs-bucket",
        help="Google Cloud Storage destination bucket name",
        required=True,
    )
    parser.add_argument(
        "--sqs-queue-arn",
        help="The ARN of the AWS SQS queue to track",
        required=True,
    )

    args = parser.parse_args()

    create_event_driven_aws_transfer(**vars(args))
