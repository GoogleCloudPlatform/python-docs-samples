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
Useful utilities for STS samples tests.
"""

import json
import os
import uuid

from azure.storage.blob import BlobServiceClient, ContainerClient
import boto3
from google.cloud import secretmanager, storage, storage_transfer
from google.cloud.storage_transfer import TransferJob

import pytest


# cache secret from secret manager
aws_secret_cache = None
azure_secret_cache = None


@pytest.fixture(scope='module')
def project_id():
    yield os.environ.get("GOOGLE_CLOUD_PROJECT")


def retrieve_from_secret_manager(name: str):
    """
    Retrieves a secret given a name.

    example ``name`` = ``projects/123/secrets/my-secret/versions/latest``
    """

    client = secretmanager.SecretManagerServiceClient()

    # retrieve from secret manager
    response = client.access_secret_version(request={"name": name})

    # parse and cache secret from secret manager
    return response.payload.data.decode("UTF-8")


def aws_parse_and_cache_secret_json(payload: str):
    """
    Decodes a JSON string in AWS AccessKey JSON format.
    Supports both single-key "AccessKey" and JSON with props.

    ``payload`` examples:
    - ``{"AccessKey": {"AccessKeyId": "", "SecretAccessKey": ""}``
    - ``{"AccessKeyId": "", "SecretAccessKey": ""}``
    """

    global aws_secret_cache

    secret = json.loads(payload)

    # normalize to props as keys
    if secret.get('AccessKey'):
        secret = secret.get('AccessKey')

    aws_secret_cache = {
        'aws_access_key_id': secret['AccessKeyId'],
        'aws_secret_access_key': secret['SecretAccessKey'],
    }

    return aws_secret_cache


def aws_key_pair():
    global aws_secret_cache

    sts_aws_secret = os.environ.get("STS_AWS_SECRET")
    sts_aws_secret_name = os.environ.get("STS_AWS_SECRET_NAME")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if aws_secret_cache:
        return aws_secret_cache

    if sts_aws_secret:
        return aws_parse_and_cache_secret_json(sts_aws_secret)

    if sts_aws_secret_name:
        res = retrieve_from_secret_manager(sts_aws_secret_name)
        return aws_parse_and_cache_secret_json(res)

    return {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
    }


def azure_parse_and_cache_secret_json(payload: str):
    """
    Decodes a JSON string in JSON format.
    Supports both single-key "AccessKey" and JSON with props.

    ``payload`` examples:
    - ``{"StorageAccount": "", "ConnectionString": "", "SAS": ""}``
    """

    global azure_secret_cache

    secret = json.loads(payload)

    azure_secret_cache = {
        'storage_account': secret['StorageAccount'],
        'connection_string': secret['ConnectionString'],
        'sas_token': secret['SAS'],
    }

    return azure_secret_cache


def azure_credentials():
    global azure_secret_cache

    sts_azure_secret = os.environ.get("STS_AZURE_SECRET")
    sts_azure_secret_name = os.environ.get("STS_AZURE_SECRET_NAME")

    if azure_secret_cache:
        return azure_secret_cache

    if sts_azure_secret:
        return aws_parse_and_cache_secret_json(sts_azure_secret)

    if sts_azure_secret_name:
        res = retrieve_from_secret_manager(sts_azure_secret_name)
        return aws_parse_and_cache_secret_json(res)

    return azure_secret_cache


@pytest.fixture(scope='module')
def aws_access_key_id():
    yield aws_key_pair()['aws_access_key_id']


@pytest.fixture(scope='module')
def aws_secret_access_key():
    yield aws_key_pair()['aws_secret_access_key']


@pytest.fixture(scope='module')
def azure_storage_account():
    yield azure_credentials()['storage_account']


@pytest.fixture(scope='module')
def azure_connection_string():
    yield azure_credentials()['connection_string']


@pytest.fixture(scope='module')
def azure_sas_token():
    yield azure_credentials()['sas_token']


@pytest.fixture(scope='module')
def bucket_name():
    yield f"sts-python-samples-test-{uuid.uuid4()}"


@pytest.fixture(scope='module')
def sts_service_account(project_id):
    client = storage_transfer.StorageTransferServiceClient()
    account = client.get_google_service_account({'project_id': project_id})

    yield account.account_email


@pytest.fixture(scope='module')
def job_description_unique(project_id: str):
    """
    Generate a unique job description. Attempts to find and delete a job with
    this generated description after tests are ran.
    """

    # Create description
    client = storage_transfer.StorageTransferServiceClient()
    description = f"Storage Transfer Service Samples Test - {uuid.uuid4().hex}"

    yield description

    # Remove job based on description as the job's name isn't predetermined
    transfer_job_to_delete: TransferJob = None

    transfer_jobs = client.list_transfer_jobs({
        'filter': json.dumps({"projectId": project_id})
    })

    for transfer_job in transfer_jobs:
        if transfer_job.description == description:
            transfer_job_to_delete = transfer_job
            break

    if transfer_job_to_delete and \
            transfer_job_to_delete.status != TransferJob.Status.DELETED:
        client.update_transfer_job({
            "job_name": transfer_job_to_delete.name,
            "project_id": project_id,
            "transfer_job": {
                "status": storage_transfer.TransferJob.Status.DELETED
            }
        })


@pytest.fixture(scope='module')
def aws_source_bucket(bucket_name: str):
    """
    Creates an S3 bucket for testing. Empties and auto-deletes after
    tests are ran.
    """

    s3_client = boto3.client('s3', **aws_key_pair())
    s3_resource = boto3.resource('s3', **aws_key_pair())

    s3_client.create_bucket(Bucket=bucket_name)

    yield bucket_name

    s3_resource.Bucket(bucket_name).objects.all().delete()
    s3_client.delete_bucket(Bucket=bucket_name)


@pytest.fixture(scope='module')
def azure_source_container(bucket_name: str):
    """
    Creates an Azure container for testing. Empties and auto-deletes after
    tests are ran.
    """

    service: BlobServiceClient = BlobServiceClient.from_connection_string(
        conn_str=azure_connection_string)

    container_client: ContainerClient = service.get_container_client(
        container=bucket_name)
    container_client.create_container()

    yield bucket_name

    container_client.delete_container()


@pytest.fixture(scope='module')
def gcs_bucket(project_id: str, bucket_name: str):
    """
    Yields and auto-cleans up a CGS bucket for use in STS jobs
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete()


@pytest.fixture(scope='module')
def source_bucket(gcs_bucket: storage.Bucket, sts_service_account: str):
    """
    Yields and auto-cleans up a CGS bucket preconfigured with necessary
    STS service account read perms
    """

    # Setup policy for STS
    member: str = f"serviceAccount:{sts_service_account}"
    objectViewer = "roles/storage.objectViewer"
    bucketReader = "roles/storage.legacyBucketReader"

    # Prepare policy
    policy = gcs_bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": objectViewer, "members": {member}})
    policy.bindings.append({"role": bucketReader, "members": {member}})

    # Set policy
    gcs_bucket.set_iam_policy(policy)

    yield gcs_bucket


@pytest.fixture(scope='module')
def destination_bucket(gcs_bucket: storage.Bucket, sts_service_account: str):
    """
    Yields and auto-cleans up a CGS bucket preconfigured with necessary
    STS service account write perms
    """

    # Setup policy for STS
    member: str = f"serviceAccount:{sts_service_account}"
    bucketWriter = "roles/storage.legacyBucketWriter"

    # Prepare policy
    policy = gcs_bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": bucketWriter, "members": {member}})

    # Set policy
    gcs_bucket.set_iam_policy(policy)

    yield gcs_bucket


@pytest.fixture(scope='module')
def intermediate_bucket(gcs_bucket: storage.Bucket, sts_service_account: str):
    """
    Yields and auto-cleans up a GCS bucket preconfigured with necessary
    STS service account write perms
    """

    # Setup policy for STS
    member: str = f"serviceAccount:{sts_service_account}"
    objectViewer = "roles/storage.objectViewer"
    bucketReader = "roles/storage.legacyBucketReader"
    bucketWriter = "roles/storage.legacyBucketWriter"

    # Prepare policy
    policy = gcs_bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": objectViewer, "members": {member}})
    policy.bindings.append({"role": bucketReader, "members": {member}})
    policy.bindings.append({"role": bucketWriter, "members": {member}})

    # Set policy
    gcs_bucket.set_iam_policy(policy)

    yield gcs_bucket


@pytest.fixture(scope='module')
def agent_pool_name():
    """
    Yields a source agent pool name
    """

    # use default agent
    yield ''


@pytest.fixture(scope='module')
def posix_root_directory():
    """
    Yields a POSIX root directory
    """

    # use arbitrary path
    yield '/my-posix-root/'


@pytest.fixture(scope='module')
def manifest_file(source_bucket: storage.Bucket):
    """
    Yields a transfer manifest file name
    """

    # use arbitrary path and name
    yield f'gs://{source_bucket.name}/test-manifest.csv'
