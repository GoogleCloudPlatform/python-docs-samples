from unittest import mock

import requests
import pytest
import tempfile
import add_dags_to_composer
from google.api_core.exceptions import Forbidden
from google.cloud import storage

from google.resumable_media.common import InvalidResponse
# fixture of valid directory

# fixture of empty directory
@pytest.fixture(scope="function")
def empty_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir

# fixture of composer storage bucket
#TODO: implement
@pytest.fixture(scope="function")
def bucket():
    yield "leah-playground"


@pytest.fixture(scope="function")
def insufficient_permissions_response() -> None:
    with mock.patch(
        "google.cloud.storage.Blob.upload_from_string",
        side_effect=Forbidden('User does not have access to the bucket'),
    ):
        yield
# create dags list
## test invalid directory
def test_create_dags_list_invalid_directory():
    with pytest.raises(FileNotFoundError):
        (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")

## test valid directory
#TODO: implement
# def test_create_dags_list():
#     (temp_dir, dags) = add_dags_to_composer._create_dags_list("this-directory-does-not-exist/")
#     assert len(dags) > 0

# upload
## test no files in directory
def test_upload_dags_to_composer_no_files(capsys, empty_directory, bucket):
    add_dags_to_composer.upload_dags_to_composer(empty_directory, bucket)
    out, _ = capsys.readouterr()
    assert "No DAGs to upload." in out

## test invalid permissions
#TODO: do I even need this test??
def test_upload_dags_to_composer_insufficient_permissions(insufficient_permissions_response):
    with pytest.raises(Forbidden):
        add_dags_to_composer.upload_dags_to_composer("../dags/", "your-bucket")
 
def test_upload_dags_to_composer_insufficient_permissions_FAKE(capsys):
        add_dags_to_composer.upload_dags_to_composer("../dags/", "your-bucket")
        out, _ = capsys.readouterr()
        assert "hi" in out



## test successful upload
#TODO: implement
# notes - patch the upload to just return a 200 but not actually upload dags
# def test_upload_dags_to_composer(capsys):
#     add_dags_to_composer.upload_dags_to_composer("this-directory-does-not-exist/", "not-a-bucket")
#     out, _ = capsys.readouterr()
#     assert "this is a dag" in out