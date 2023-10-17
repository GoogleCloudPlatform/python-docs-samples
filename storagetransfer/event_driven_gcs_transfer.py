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
Command-line sample that creates aan event driven transfer between two GCS buckets that tracks a PubSub subscription.
"""

import argparse

# [START storagetransfer_create_event_driven_gcs_transfer]

from google.cloud import storage_transfer


def create_event_driven_gcs_transfer(
    project_id: str,
    description: str,
    source_bucket: str,
    sink_bucket: str,
    pubsub_id: str,
):
    """Create an event driven transfer between two GCS buckets that tracks a PubSub subscription"""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A description of this job
    # description = 'Creates an event-driven transfer that tracks a pubsub subscription'

    # Google Cloud Storage source bucket name
    # source_bucket = 'my-gcs-source-bucket'

    # Google Cloud Storage destination bucket name
    # sink_bucket = 'my-gcs-destination-bucket'

    # The Pubsub Subscription ID to track
    # pubsub_id = 'projects/PROJECT_NAME/subscriptions/SUBSCRIPTION_ID'

    transfer_job_request = storage_transfer.CreateTransferJobRequest(
        {
            "transfer_job": {
                "project_id": project_id,
                "description": description,
                "status": storage_transfer.TransferJob.Status.ENABLED,
                "transfer_spec": {
                    "gcs_data_source": {
                        "bucket_name": source_bucket,
                    },
                    "gcs_data_sink": {
                        "bucket_name": sink_bucket,
                    },
                },
                "event_stream": {
                    "name": pubsub_id,
                },
            },
        }
    )

    result = client.create_transfer_job(transfer_job_request)
    print(f"Created transferJob: {result.name}")


# [END storagetransfer_create_event_driven_gcs_transfer]

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
        "--source-bucket", help="Google Cloud Storage source bucket name", required=True
    )
    parser.add_argument(
        "--sink-bucket",
        help="Google Cloud Storage destination bucket name",
        required=True,
    )
    parser.add_argument(
        "--pubsub-id",
        help="The subscription ID of the PubSub queue to track",
        required=True,
    )

    args = parser.parse_args()

    create_event_driven_gcs_transfer(**vars(args))
