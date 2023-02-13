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
Command-line sample that creates a one-time transfer from Azure Blob Storage to
Google Cloud Storage.
"""


# [START storagetransfer_transfer_from_azure]
from datetime import datetime

from google.cloud import storage_transfer


def create_one_time_azure_transfer(
        project_id: str, description: str,
        azure_storage_account: str, azure_sas_token: str,
        source_container: str, sink_bucket: str):
    """Creates a one-time transfer job from Azure Blob Storage to Google Cloud
    Storage."""

    # Initialize client that will be used to create storage transfer requests.
    # This client only needs to be created once, and can be reused for
    # multiple requests.
    client = storage_transfer.StorageTransferServiceClient()

    # The ID of the Google Cloud Platform Project that owns the job
    # project_id = 'my-project-id'

    # A useful description for your transfer job
    # description = 'My transfer job'

    # Azure Storage Account name
    # azure_storage_account = 'accountname'

    # Azure Shared Access Signature token
    # azure_sas_token = '?sv=...'

    # Azure Blob source container name
    # source_container = 'my-azure-source-bucket'

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
                'azure_blob_storage_data_source': {
                    'storage_account': azure_storage_account,
                    'azure_credentials': {
                        'sas_token': azure_sas_token
                    },
                    'container': source_container
                },
                'gcs_data_sink': {
                    'bucket_name': sink_bucket,
                }
            }
        }
    })

    result = client.create_transfer_job(transfer_job_request)
    print(f'Created transferJob: {result.name}')


# [END storagetransfer_transfer_from_azure]
