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
Command-line sample that creates a transfer from an AWS S3-compatible source
to GCS.
"""


import argparse

# [START storagetransfer_transfer_from_s3_compatible_source]
from google.cloud import storage_transfer

AuthMethod = storage_transfer.S3CompatibleMetadata.AuthMethod
NetworkProtocol = storage_transfer.S3CompatibleMetadata.NetworkProtocol
RequestModel = storage_transfer.S3CompatibleMetadata.RequestModel


def transfer_from_S3_compat_to_gcs(
    project_id: str,
    description: str,
    source_agent_pool_name: str,
    source_bucket_name: str,
    source_path: str,
    gcs_sink_bucket: str,
    gcs_path: str,
    region: str,
    endpoint: str,
    protocol: NetworkProtocol,
    request_model: RequestModel,
    auth_method: AuthMethod,
) -> None:
    """Creates a transfer from an AWS S3-compatible source to GCS"""

    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # The agent pool associated with the S3-compatible data source.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # source_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The S3 compatible bucket name to transfer data from
    # source_bucket_name = "my-bucket-name"

    # The S3 compatible path (object prefix) to transfer data from
    # source_path = "path/to/data/"

    # The ID of the GCS bucket to transfer data to
    # gcs_sink_bucket = "my-sink-bucket"

    # The GCS path (object prefix) to transfer data to
    # gcs_path = "path/to/data/"

    # The S3 region of the source bucket
    # region = 'us-east-1'

    # The S3-compatible endpoint
    # endpoint = "us-east-1.example.com"

    # The S3-compatible network protocol
    # protocol = NetworkProtocol.NETWORK_PROTOCOL_HTTPS

    # The S3-compatible request model
    # request_model = RequestModel.REQUEST_MODEL_VIRTUAL_HOSTED_STYLE

    # The S3-compatible auth method
    # auth_method = AuthMethod.AUTH_METHOD_AWS_SIGNATURE_V4

    transfer_job_request = storage_transfer.CreateTransferJobRequest({
        'transfer_job': {
            'project_id': project_id,
            'description': description,
            'status': storage_transfer.TransferJob.Status.ENABLED,
            'transfer_spec': {
                'source_agent_pool_name': source_agent_pool_name,
                'aws_s3_compatible_data_source': {
                    'region': region,
                    's3_metadata': {
                        'auth_method': auth_method,
                        'protocol': protocol,
                        'request_model': request_model
                    },
                    'endpoint': endpoint,
                    'bucket_name': source_bucket_name,
                    'path': source_path
                },
                'gcs_data_sink': {
                    'bucket_name': gcs_sink_bucket,
                    'path': gcs_path,
                }
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_transfer_from_s3_compatible_source]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--project-id',
        help='The ID of the Google Cloud Platform Project that owns the job',
        required=True)
    parser.add_argument(
        '--description',
        help='A useful description for your transfer job')
    parser.add_argument(
        '--source-agent-pool-name',
        default='',
        help="The agent pool associated with the S3-compatible data source.")
    parser.add_argument(
        '--source-bucket-name',
        default="my-bucket-name",
        help="The S3 compatible bucket name to transfer data from")
    parser.add_argument(
        '--source-path',
        default="path/to/data/",
        help="The S3 compatible path (object prefix) to transfer data from")
    parser.add_argument(
        '--gcs-sink-bucket',
        default="my-sink-bucket",
        help="The ID of the GCS bucket to transfer data to")
    parser.add_argument(
        '--gcs-path',
        default="path/to/data/",
        help="The GCS path (object prefix) to transfer data to")
    parser.add_argument(
        '--region',
        default='us-east-1',
        help="The S3 region of the source bucket")
    parser.add_argument(
        '--endpoint',
        default="us-east-1.example.com",
        help="The S3-compatible endpoint")
    parser.add_argument(
        '--protocol',
        default=NetworkProtocol.NETWORK_PROTOCOL_HTTPS,
        type=int,
        help="The S3-compatible network protocol. "
        "See google.cloud.storage_transfer.\
            S3CompatibleMetadata.NetworkProtocol")
    parser.add_argument(
        '--request-model',
        default=RequestModel.REQUEST_MODEL_VIRTUAL_HOSTED_STYLE,
        type=int,
        help="The S3-compatible request model. "
        "See google.cloud.storage_transfer.S3CompatibleMetadata.RequestModel")
    parser.add_argument(
        '--auth-method',
        default=AuthMethod.AUTH_METHOD_AWS_SIGNATURE_V4,
        type=int,
        help="The S3-compatible auth method. "
        "See google.cloud.storage_transfer.S3CompatibleMetadata.AuthMethod")

    args = parser.parse_args()

    transfer_from_S3_compat_to_gcs(**vars(args))
