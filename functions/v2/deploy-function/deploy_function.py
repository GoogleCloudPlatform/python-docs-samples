# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import tempfile
import zipfile
from google.cloud import storage

# [START create_cloud_function_v2]
from google.cloud.functions_v2 import FunctionServiceClient, CreateFunctionRequest
from google.cloud.functions_v2.types import (
    Function,
    BuildConfig,
    ServiceConfig,
    StorageSource,
    Source,
)


def create_cloud_function(
    project_id: str,
    bucket_name: str,
    location_id: str,
    function_id: str,
    entry_point: str,
    function_archive: str,
    runtime: str = "python311",
) -> None:
    """
    Created GCP cloud function with given args.
    Args:
        project_id: GCP project ID
        bucket_name: name of the bucket to store/retrieve your function archive
        location_id: GCP location id (f.e. "us-central1")
        function_id: id of cloud function in function list
        entry_point: name of python function which will be called by cloud function
        function_archive: name of archive with function which lies in the bucket (f.e. "my_function.zip")
        runtime: runtime (language) of your cloud function (f.e. "python39", "nodejs20", "go112")

    """
    client = FunctionServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    function_name = (
        f"projects/{project_id}/locations/{location_id}/functions/{function_id}"
    )
    function = Function(
        name=function_name,
        build_config=BuildConfig(
            source=Source(
                storage_source=StorageSource(
                    bucket=bucket_name,
                    object_=function_archive,
                    generation=2,
                )
            ),
            runtime=runtime,
            entry_point=entry_point,
        ),
        service_config=ServiceConfig(available_memory="256M"),
    )

    request = CreateFunctionRequest(
        parent=parent, function=function, function_id=function_id
    )

    operation = client.create_function(request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)
# [END create_cloud_function_v2]


def create_and_upload_function(bucket_name: str, destination_blob_name: str) -> None:
    """
        Function to create temp file, zip it, and upload to GCS
    Args:
        bucket_name: bucket name which stores archive with cloud function code
        destination_blob_name: f.e. "my_function.zip"
    """
    file_content = """
import functions_framework

@functions_framework.http
def my_function_entry(request):
    print("Hello world!")
    """
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Path for the temporary Python file
        temp_file_path = f"{temp_dir}/main.py"

        # Write the file content to main.py in the temp directory
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(file_content)

        # Path for the zip file to be created
        zip_path = f"{temp_dir}/my_function.zip"

        # Create a zip file and add main.py to it
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(temp_file_path, arcname="main.py")

        # Upload the zip file to Google Cloud Storage
        _upload_blob(bucket_name, zip_path, destination_blob_name)


def _upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str) -> None:
    """
    Uploads a file to the bucket. Helper function
    Args:
        bucket_name: bucket name which stores archive with cloud function code
        source_file_name: path to uploaded archive locally
        destination_blob_name: name of the file on the bucket, f.e. "my_function.zip"

    Returns:

    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


if __name__ == "__main__":
    import uuid
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    BUCKET_NAME = os.environ["BUCKET_NAME"]
    FILE_NAME = "my_function.zip"
    create_and_upload_function(BUCKET_NAME, FILE_NAME)
    create_cloud_function(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
        location_id="us-central1",
        function_id=f"test-function-{uuid.uuid4()}",
        entry_point="my_function_entry",
        function_archive="my_function.zip",  # assume, that function already uploaded to <BUCKET_NAME>
    )
