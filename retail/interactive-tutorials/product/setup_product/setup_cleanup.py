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

import json
import re

from google.api_core.exceptions import NotFound
import google.auth

from google.cloud import bigquery
from google.cloud import storage
from google.cloud.retail import CreateProductRequest, DeleteProductRequest, \
    FulfillmentInfo, GetProductRequest, PriceInfo, Product, ProductServiceClient

project_id = google.auth.default()[1]
default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"
default_branch_name = f"projects/{project_id}/locations/global/catalogs/default_catalog/branches/default_branch"


def generate_product() -> Product:
    price_info = PriceInfo()
    price_info.price = 30.0
    price_info.original_price = 35.5
    price_info.currency_code = "USD"
    fulfillment_info = FulfillmentInfo()
    fulfillment_info.type_ = "pickup-in-store"
    fulfillment_info.place_ids = ["store0", "store1"]
    return Product(
        title='Nest Mini',
        type_=Product.Type.PRIMARY,
        categories=['Speakers and displays'],
        brands=['Google'],
        price_info=price_info,
        fulfillment_info=[fulfillment_info],
        availability="IN_STOCK",
    )


def create_product(product_id: str) -> object:
    create_product_request = CreateProductRequest()
    create_product_request.product = generate_product()
    create_product_request.product_id = product_id
    create_product_request.parent = default_branch_name

    created_product = ProductServiceClient().create_product(
        create_product_request)
    print("---product is created:---")
    print(created_product)

    return created_product


def delete_product(product_name: str):
    delete_product_request = DeleteProductRequest()
    delete_product_request.name = product_name
    ProductServiceClient().delete_product(delete_product_request)

    print("---product " + product_name + " was deleted:---")


def get_product(product_name: str):
    get_product_request = GetProductRequest()
    get_product_request.name = product_name
    try:
        product = ProductServiceClient().get_product(get_product_request)
        print("---get product response:---")
        print(product)
        return product
    except NotFound as e:
        print(e.message)
        return e.message


def try_to_delete_product_if_exists(product_name: str):
    get_product_request = GetProductRequest()
    get_product_request.name = product_name
    delete_product_request = DeleteProductRequest()
    delete_product_request.name = product_name
    print(
        "---delete product from the catalog, if the product already exists---")
    try:
        product = ProductServiceClient().get_product(get_product_request)
        ProductServiceClient().delete_product(product.name)
    except NotFound as e:
        print(e.message)


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
            f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}"
        )
        return new_bucket


def delete_bucket(bucket_name: str):
    """Delete a bucket from Cloud Storage"""
    print(f"Deleting bucket name: {bucket_name}")
    storage_client = storage.Client()
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
