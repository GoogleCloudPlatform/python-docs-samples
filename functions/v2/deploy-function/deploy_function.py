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

# [START functions_create_function_v2]
from google.cloud.functions_v2 import (
    CreateFunctionRequest,
    DeleteFunctionRequest,
    FunctionServiceClient,
)
from google.cloud.functions_v2.types import (
    BuildConfig,
    Environment,
    Function,
    ServiceConfig,
    Source,
    StorageSource,
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
    Creates a new Cloud Function in a project. Function source code will be taken from archive which lies in bucket.
    The function will be deployed to the specified location and runtime.
    Please note, that you need to sign your call to the function or allow some users to access.

    Args:
        project_id (str): Project ID.
        bucket_name (str): The name of the Google Cloud Storage bucket where the function archive is stored.
        location_id (str): The Google Cloud location ID where the function will be deployed (e.g., 'us-central1').
        function_id (str): The identifier of the cloud function within the specified project and location.
        entry_point (str): The name of the Python function to be executed as the entry point of the cloud function.
        function_archive (str): The name of the archive file within the bucket that contains the function's source code
        (e.g., 'my_function.zip').
        runtime (str): The runtime environment for the cloud function (default is 'python311'; f.e.
        'python39', 'nodejs20', 'go112').

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
                )
            ),
            runtime=runtime,
            entry_point=entry_point,
        ),
        service_config=ServiceConfig(
            available_memory="256M",
            ingress_settings="ALLOW_ALL",
        ),
        environment=Environment.GEN_1,
    )

    request = CreateFunctionRequest(
        parent=parent, function=function, function_id=function_id
    )

    operation = client.create_function(request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)

# [END functions_create_function_v2]


def create_and_upload_function(bucket_name: str, destination_blob_name: str) -> None:
    """
        Function to create temp file, zip it, and upload to GCS
    Args:
        bucket_name (str): bucket name which stores archive with cloud function code
        destination_blob_name (str): f.e. "my_function.zip"
    """
    file_content = """
import functions_framework

@functions_framework.http
def my_function_entry(request):
    return "ok"
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


def _upload_blob(
    bucket_name: str, source_file_name: str, destination_blob_name: str
) -> None:
    """
    Uploads a file to the bucket. Helper function
    Args:
        bucket_name (str): bucket name which stores archive with cloud function code
        source_file_name (str): path to uploaded archive locally
        destination_blob_name (str): name of the file on the bucket, f.e. "my_function.zip"

    Returns:

    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
        # Set the versioning state of the bucket
        bucket.versioning_enabled = False
        bucket.patch()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def delete_bucket(project_id: str, bucket_name: str):
    """
    Deletes a specified storage bucket. This function checks if the bucket exists before attempting to delete it.
    It ensures the bucket is deleted if found, forcibly deleting all contents if necessary.

    Args:
        project_id (str): project ID
        bucket_name (str): The name of the bucket to delete.
    """
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    if bucket.exists():
        bucket.delete(force=True)


def delete_function(project_id: str, region: str, function_id: str):
    """
    Deletes a specified function. This function checks if the function exists before attempting to delete it.
    It ensures the function is deleted if found.

    Args:
        project_id (str): project ID
        region (str): location id (f.e. "us-central1")
        function_id (str): name of the function to delete

    Returns:

    """
    client = FunctionServiceClient()
    request = DeleteFunctionRequest(
        name=f"projects/{project_id}/locations/{region}/functions/{function_id}"
    )
    client.delete_function(request=request)


if __name__ == "__main__":
    import uuid

    import google.auth

    # setup
    PROJECT = google.auth.default()[1]
    BUCKET_NAME = f"test-bucket-{uuid.uuid4()}"
    FILE_NAME = "my_function.zip"
    LOCATION = "us-central1"
    FUNCTION_ID = f"test-function-{uuid.uuid4()}"

    create_and_upload_function(BUCKET_NAME, FILE_NAME)

    # act
    create_cloud_function(
        project_id=PROJECT,
        bucket_name=BUCKET_NAME,
        location_id=LOCATION,
        function_id=FUNCTION_ID,
        entry_point="my_function_entry",
        function_archive="my_function.zip",
    )

    # cleanup
    delete_function(PROJECT, LOCATION, FUNCTION_ID)
    delete_bucket(PROJECT, BUCKET_NAME)
