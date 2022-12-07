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


import datetime
import json
import re
import shlex
import subprocess

from google.api_core.exceptions import NotFound
import google.auth

from google.cloud import bigquery
from google.cloud import storage
from google.cloud.retail import ProductDetail, PurgeUserEventsRequest, \
    UserEvent, UserEventServiceClient, WriteUserEventRequest
from google.cloud.retail_v2 import Product

from google.protobuf.timestamp_pb2 import Timestamp

project_id = google.auth.default()[1]
default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"


# get user event
def get_user_event(visitor_id):
    timestamp = Timestamp()
    timestamp.seconds = int(datetime.datetime.now().timestamp())

    product = Product()
    product.id = 'test_id'

    product_detail = ProductDetail()
    product_detail.product = product

    user_event = UserEvent()
    user_event.event_type = "detail-page-view"
    user_event.visitor_id = visitor_id
    user_event.event_time = timestamp
    user_event.product_details = [product_detail]

    print(user_event)
    return user_event


# write user event
def write_user_event(visitor_id):
    write_user_event_request = WriteUserEventRequest()
    write_user_event_request.user_event = get_user_event(visitor_id)
    write_user_event_request.parent = default_catalog
    user_event = UserEventServiceClient().write_user_event(
        write_user_event_request)
    print("---the user event is written---")
    print(user_event)
    return user_event


# purge user event
def purge_user_event(visitor_id):
    purge_user_event_request = PurgeUserEventsRequest()
    purge_user_event_request.filter = f'visitorId="{visitor_id}"'
    purge_user_event_request.parent = default_catalog
    purge_user_event_request.force = True
    purge_operation = UserEventServiceClient().purge_user_events(
        purge_user_event_request)

    print("---the purge operation was started:----")
    print(purge_operation.operation.name)


def get_project_id():
    get_project_command = "gcloud config get-value project --format json"
    config = subprocess.check_output(shlex.split(get_project_command))
    project_id = re.search('\"(.*?)\"', str(config)).group(1)
    return project_id


def create_bucket(bucket_name: str):
    """Create a new bucket in Cloud Storage"""
    print("Creating new bucket:" + bucket_name)
    buckets_in_your_project = list_buckets()
    if bucket_name in buckets_in_your_project:
        print(f"Bucket {bucket_name} already exists")
    else:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = storage_client.create_bucket(bucket, location="us")
        print(
            f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}")
        return new_bucket


def delete_bucket(bucket_name: str):
    """Delete a bucket from Cloud Storage"""
    storage_client = storage.Client()
    print("Deleting bucket:" + bucket_name)
    buckets_in_your_project = list_buckets()
    if bucket_name in buckets_in_your_project:
        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            blob.delete()
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete()
        print(f"Bucket {bucket.name} is deleted")
    else:
        print(f"Bucket {bucket_name} is not found")


def list_buckets():
    """Lists all buckets"""
    bucket_list = []
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        bucket_list.append(bucket.name)
    return bucket_list


def upload_blob(bucket_name, source_file_name):
    """Uploads a file to the bucket."""
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    print(f"Uploading data from {source_file_name} to the bucket {bucket_name}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    object_name = re.search('resources/(.*?)$', source_file_name).group(1)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to {object_name}."
    )


def create_bq_dataset(dataset_name):
    """Create a BigQuery dataset"""
    full_dataset_id = f"{project_id}.{dataset_name}"
    bq = bigquery.Client()
    print(f"Creating dataset {full_dataset_id}")
    try:
        bq.get_dataset(full_dataset_id)
        print(f"dataset {full_dataset_id} already exists")
    except NotFound:
        # Construct a Dataset object to send to the API.
        dataset = bigquery.Dataset(full_dataset_id)
        dataset.location = "US"
        bq.create_dataset(dataset)
        print("dataset is created")


def create_bq_table(dataset, table_name, schema_file_path):
    """Create a BigQuery table"""
    full_table_id = f"{project_id}.{dataset}.{table_name}"
    bq = bigquery.Client()
    print(f"Check if BQ table {full_table_id} exists")
    try:
        bq.get_table(full_table_id)
        print(f"table {full_table_id} exists and will be deleted")
        delete_bq_table(dataset, table_name)
    except NotFound:
        print(f"table {full_table_id} does not exist")
    # Construct a Table object to send to the API.
    with open(schema_file_path, "rb") as schema:
        schema_dict = json.load(schema)
        table = bigquery.Table(full_table_id, schema=schema_dict)
    bq.create_table(table)
    print(f"table {full_table_id} is created")


def delete_bq_table(dataset, table_name):
    full_table_id = f"{project_id}.{dataset}.{table_name}"
    bq = bigquery.Client()
    bq.delete_table(full_table_id, not_found_ok=True)
    print(f"Table '{full_table_id}' is deleted.")


def upload_data_to_bq_table(dataset, table_name, source, schema_file_path):
    """Upload data to the table from specified source file"""
    full_table_id = f"{project_id}.{dataset}.{table_name}"
    bq = bigquery.Client()
    print(f"Uploading data from {source} to the table {full_table_id}")
    with open(schema_file_path, "rb") as schema:
        schema_dict = json.load(schema)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema=schema_dict)
    with open(source, "rb") as source_file:
        job = bq.load_table_from_file(source_file, full_table_id,
                                      job_config=job_config)
    job.result()  # Waits for the job to complete.
    print("data was uploaded")
