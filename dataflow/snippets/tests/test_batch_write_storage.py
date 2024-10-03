#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import gc
import sys
import uuid

from google.cloud import storage

import pytest

from ..batch_write_storage import write_to_cloud_storage


bucket_name = f"test-bucket-{uuid.uuid4()}"
storage_client = storage.Client()


@pytest.fixture(scope="function")
def setup_and_teardown() -> None:
    try:
        bucket = storage_client.create_bucket(bucket_name)
        yield
    finally:
        bucket.delete(force=True)
        # Ensure that PipelineOptions subclasses have been cleaned up between tests
        # See https://github.com/apache/beam/issues/18197
        gc.collect()


def test_write_to_cloud_storage(setup_and_teardown: None) -> None:
    sys.argv = ["", f"--output=gs://{bucket_name}/output/out-"]
    write_to_cloud_storage()

    blobs = list(storage_client.list_blobs(bucket_name))
    # Ensure the pipeline wrote files to Cloud Storage
    assert blobs
    for blob in blobs:
        assert blob.name.endswith(".txt")
