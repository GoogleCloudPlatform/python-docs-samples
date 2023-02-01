#!/usr/bin/env python

# Copyright 2022 Google LLC
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
Command-line sample that creates a transfer from a POSIX file system to a
GCS bucket using a manifest file.
"""


import argparse

# [START storagetransfer_manifest_request]
from google.cloud import storage_transfer


def create_transfer_with_manifest(
        project_id: str, description: str, source_agent_pool_name: str,
        root_directory: str, sink_bucket: str, manifest_location: str):
    """Create a transfer from a POSIX file system to a GCS bucket using
    a manifest file."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # The agent pool associated with the POSIX data source.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # source_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The root directory path on the source filesystem
    # root_directory = '/directory/to/transfer/source'

    # Google Cloud Storage destination bucket name
    # sink_bucket = 'my-gcs-destination-bucket'

    # Transfer manifest location. Must be a `gs:` URL
    # manifest_location = 'gs://my-bucket/sample_manifest.csv'

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'transfer_spec': {
                'source_agent_pool_name': source_agent_pool_name,
                'posix_data_source': {
                    'root_directory': root_directory,
                },
                'gcs_data_sink': {
                    'bucket_name': sink_bucket,
                },
                'transfer_manifest': {
                    'location': manifest_location
                }
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_manifest_request]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--project-id',
        help='The ID of the Google Cloud Platform Project that owns the job',
        required=True)
    parser.add_argument(
        '--description',
        help='A useful description for your transfer job',
        required=True)
    parser.add_argument(
        '--source-agent-pool-name',
        help='The agent pool associated with the POSIX data source',
        required=True)
    parser.add_argument(
        '--root-directory',
        help='The root directory path on the source filesystem',
        required=True)
    parser.add_argument(
        '--sink-bucket',
        help='Google Cloud Storage destination bucket name',
        required=True)
    parser.add_argument(
        '--manifest-location',
        help='Transfer manifest location. Must be a `gs:` URL',
        required=True)

    args = parser.parse_args()

    create_transfer_with_manifest(**vars(args))
