import os
import re
import uuid

import pytest
from deploy_function import create_cloud_function
from google.cloud import storage


def test_create_cloud_function(capsys: "pytest.CaptureFixture[str]"):
    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    BUCKET_NAME = "samples-functions-test-practice-bucket-111"
    FOLDER_NAME = "samples-functions-test-practice-folder-111"
    FILE_NAME = "my_function.zip"
    object_name = f"{FOLDER_NAME}/{FILE_NAME}"
    function_id = f"test-function-{uuid.uuid4()}"
    storage_client = storage.Client()
    RUNTIME = "python310"

    # Attempt to create the bucket (if it doesn't already exist)
    bucket = storage_client.bucket(BUCKET_NAME)
    if not bucket.exists():
        bucket = storage_client.create_bucket(BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} created.")
    blob = bucket.blob(object_name)
    current_folder = os.path.dirname(os.path.abspath(__file__))
    blob.upload_from_filename(os.path.join(current_folder, FILE_NAME))

    # upload function archive
    create_cloud_function(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
        location_id="us-central1",
        function_id=function_id,
        entry_point="my_function_entry",
        function_archive=object_name,
        runtime=RUNTIME,
    )

    out, _ = capsys.readouterr()
    assert re.search(f'url: ".*{function_id}"', out)
    assert re.search(f'runtime: "{RUNTIME}"', out)
