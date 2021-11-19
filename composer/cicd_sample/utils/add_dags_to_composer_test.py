from unittest import mock

import requests
import pytest
import tempfile
import uuid
import add_dags_to_composer
from google.api_core.exceptions import Forbidden
from google.cloud import storage

from google.resumable_media.common import InvalidResponse
# fixture of valid directory

storage_client = storage.Client()
# fixture of empty directory
@pytest.fixture(scope="function")
def empty_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir

# test bucket used in lieu of an actual Composer environment
@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""
    
    bucket_name = f"temp-composer-cicd-test-{str(uuid.uuid4())}"
    bucket = storage_client.bucket(bucket_name)

    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
    yield bucket_name

    bucket = storage_client.bucket(bucket_name)
    bucket.delete(force=True)


# create dags list
## test invalid directory
def test_create_dags_list_invalid_directory():
    with pytest.raises(FileNotFoundError):
        (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")

## test valid directory
#TODO: implement
def test_create_dags_list():
    (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")
    assert len(dags) > 0

# upload
## test no files in directory
def test_upload_dags_to_composer_no_files(capsys, empty_directory, test_bucket):
    add_dags_to_composer.upload_dags_to_composer(empty_directory, test_bucket)
    out, _ = capsys.readouterr()
    assert "No DAGs to upload." in out


## test successful upload
def test_upload_dags_to_composer( test_bucket, capsys):
    add_dags_to_composer.upload_dags_to_composer("../dags", test_bucket)
    out, _ = capsys.readouterr()
    assert "uploaded" in out