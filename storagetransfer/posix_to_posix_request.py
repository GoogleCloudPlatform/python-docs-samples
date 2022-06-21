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
Command-line sample that creates a transfer between POSIX file systems.
"""


import argparse

# [START storagetransfer_transfer_posix_to_posix]
from google.cloud import storage_transfer


def transfer_between_posix(
        project_id: str, description: str, source_agent_pool_name: str,
        sink_agent_pool_name: str, root_directory: str,
        destination_directory: str, intermediate_bucket: str):
    """Creates a transfer between POSIX file systems."""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # The agent pool associated with the POSIX data source.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # source_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The agent pool associated with the POSIX data sink.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # sink_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The root directory path on the source filesystem
    # root_directory = '/directory/to/transfer/source'

    # The root directory path on the destination filesystem
    # destination_directory = '/directory/to/transfer/sink'

    # The Google Cloud Storage bucket for intermediate storage
    # intermediate_bucket = 'my-intermediate-bucket'

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'transfer_spec': {
                'source_agent_pool_name': source_agent_pool_name,
                'sink_agent_pool_name': sink_agent_pool_name,
                'posix_data_source': {
                    'root_directory': root_directory,
                },
                'posix_data_sink': {
                    'root_directory': destination_directory,
                },
                'gcs_intermediate_data_location': {
                    'bucket_name': intermediate_bucket
                },
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_transfer_posix_to_posix]

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
        '--sink-agent-pool-name',
        help='The agent pool associated with the POSIX data sink',
        required=True)
    parser.add_argument(
        '--root-directory',
        help='The root directory path on the source filesystem',
        required=True)
    parser.add_argument(
        '--destination-directory',
        help='The root directory path on the destination filesystem',
        required=True)
    parser.add_argument(
        '--intermediate-bucket',
        help='The Google Cloud Storage bucket for intermediate storage',
        required=True)

    args = parser.parse_args()

    transfer_between_posix(**vars(args))
