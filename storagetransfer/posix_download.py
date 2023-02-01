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
Command-line sample that creates a transfer from a GCS bucket to a POSIX file
system.
"""


import argparse

# [START storagetransfer_download_to_posix]
from google.cloud import storage_transfer


def download_from_gcs(
        project_id: str, description: str, sink_agent_pool_name: str,
        root_directory: str, source_bucket: str, gcs_source_path: str):
    """Create a transfer from a GCS bucket to a POSIX file system."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # The agent pool associated with the POSIX data sink.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # sink_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The root directory path on the destination filesystem
    # root_directory = '/directory/to/transfer/sink'

    # Google Cloud Storage source bucket name
    # source_bucket = 'my-gcs-source-bucket'

    # An optional path on the Google Cloud Storage bucket to download from
    # gcs_source_path = 'foo/bar/'

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'transfer_spec': {
                'sink_agent_pool_name': sink_agent_pool_name,
                'posix_data_sink': {
                    'root_directory': root_directory,
                },
                'gcs_data_source': {
                    'bucket_name': source_bucket,
                    'path': gcs_source_path,
                },
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_download_to_posix]

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
        '--sink-agent-pool-name',
        help='The agent pool associated with the POSIX data sink',
        required=True)
    parser.add_argument(
        '--root-directory',
        help='The root directory path on the destination filesystem',
        required=True)
    parser.add_argument(
        '--source-bucket',
        help='Google Cloud Storage source bucket name',
        required=True)
    parser.add_argument(
        '--gcs-source-path',
        help='A path on the Google Cloud Storage bucket to download from',
        required=True)

    args = parser.parse_args()

    download_from_gcs(**vars(args))
