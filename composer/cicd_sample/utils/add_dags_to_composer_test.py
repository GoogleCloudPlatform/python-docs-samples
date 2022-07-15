# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
from shutil import copytree
import tempfile
import uuid

from google.cloud import storage
import pytest

import add_dags_to_composer  # noqa: I100 - lint is incorrectly saying this is out of order


DAGS_DIR = pathlib.Path(__file__).parent.parent / "dags/"


@pytest.fixture(scope="function")
def dags_directory() -> str:
    """Copies contents of dags/ folder to a temporary directory"""
    temp_dir = tempfile.mkdtemp()
    copytree(DAGS_DIR, f"{temp_dir}/", dirs_exist_ok=True)
    yield temp_dir


@pytest.fixture(scope="function")
def empty_directory() -> str:
    temp_dir = tempfile.mkdtemp()
    yield temp_dir


# test bucket used in lieu of an actual Composer environment bucket
@pytest.fixture(scope="module")
def test_bucket() -> str:
    """Yields a bucket that is deleted after the test completes."""
    storage_client = storage.Client()

    bucket_name = f"temp-composer-cicd-test-{str(uuid.uuid4())}"
    bucket = storage_client.bucket(bucket_name)

    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
    yield bucket_name

    bucket = storage_client.bucket(bucket_name)
    bucket.delete(force=True)


def test_create_dags_list_invalid_directory() -> None:
    with pytest.raises(FileNotFoundError):
        (temp_dir, dags) = add_dags_to_composer._create_dags_list(
            "this-directory-does-not-exist/"
        )  # noqa: E117


def test_create_dags_list_empty_directory(empty_directory: str) -> None:
    (temp_dir, dags) = add_dags_to_composer._create_dags_list(
        empty_directory
    )  # noqa: E117
    assert len(dags) == 0
    assert len(os.listdir(temp_dir)) == 0


def test_create_dags_list(dags_directory: str) -> None:
    (temp_dir, dags) = add_dags_to_composer._create_dags_list(dags_directory)
    assert len(dags) == 2
    assert f"{temp_dir}/__init__.py" not in dags
    assert f"{temp_dir}/example_dag.py" in dags
    assert f"{temp_dir}/example2_dag.py" in dags
    assert f"{temp_dir}/example_dag_test.py" not in dags
    assert f"{temp_dir}/example2_dag_test.py" not in dags


def test_upload_dags_to_composer_no_files(
    capsys: pytest.CaptureFixture, empty_directory: str, test_bucket: str
) -> None:
    add_dags_to_composer.upload_dags_to_composer(empty_directory, test_bucket)
    out, _ = capsys.readouterr()
    assert "No DAGs to upload." in out


def test_upload_dags_to_composer_no_name_override(test_bucket: str) -> None:
    with pytest.raises(FileNotFoundError):
        add_dags_to_composer.upload_dags_to_composer(DAGS_DIR, test_bucket)


def test_upload_dags_to_composer(
    test_bucket: str, capsys: pytest.CaptureFixture
) -> None:
    add_dags_to_composer.upload_dags_to_composer(DAGS_DIR, test_bucket, "../dags/")
    out, _ = capsys.readouterr()
    assert "uploaded" in out
