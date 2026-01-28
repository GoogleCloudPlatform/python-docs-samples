# Copyright 2025 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import uuid
import os

import pytest
from google.cloud.storage import Client
import contextlib

from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)

# Import all the snippets
import storage_create_and_write_appendable_object
import storage_finalize_appendable_object_upload
import storage_open_multiple_objects_ranged_read
import storage_open_object_multiple_ranged_read
import storage_open_object_read_full_object
import storage_open_object_single_ranged_read
import storage_pause_and_resume_appendable_upload
import storage_read_appendable_object_tail

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_ZONAL_SYSTEM_TESTS") != "True",
    reason="Zonal system tests need to be explicitly enabled. This helps scheduling tests in Kokoro and Cloud Build.",
)


# TODO: replace this with a fixture once zonal bucket creation / deletion
# is supported in grpc client or json client client.
_ZONAL_BUCKET = os.getenv("ZONAL_BUCKET")


async def create_async_grpc_client():
    """Initializes async client and gets the current event loop."""
    return AsyncGrpcClient()


# Forcing a single event loop for the whole test session
@pytest.fixture(scope="session")
def event_loop():
    """Redefine pytest-asyncio's event_loop fixture to be session-scoped."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def async_grpc_client(event_loop):
    """Yields a StorageAsyncClient that is closed after the test session."""
    grpc_client = event_loop.run_until_complete(create_async_grpc_client())
    yield grpc_client


@pytest.fixture(scope="session")
def json_client():
    client = Client()
    with contextlib.closing(client):
        yield client


async def create_appendable_object(grpc_client, object_name, data):
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=_ZONAL_BUCKET,
        object_name=object_name,
        generation=0,  # throws `FailedPrecondition` if object already exists.
    )
    await writer.open()
    await writer.append(data)
    await writer.close()
    return writer.generation


# TODO: replace this with a fixture once zonal bucket creation / deletion
# is supported in grpc client or json client client.
_ZONAL_BUCKET = os.getenv("ZONAL_BUCKET")


def test_storage_create_and_write_appendable_object(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"zonal-snippets-test-{uuid.uuid4()}"

    event_loop.run_until_complete(
        storage_create_and_write_appendable_object.storage_create_and_write_appendable_object(
            _ZONAL_BUCKET, object_name, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert f"Appended object {object_name} created of size" in out

    blob = json_client.bucket(_ZONAL_BUCKET).blob(object_name)
    blob.delete()


def test_storage_finalize_appendable_object_upload(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-finalize-appendable-{uuid.uuid4()}"
    event_loop.run_until_complete(
        storage_finalize_appendable_object_upload.storage_finalize_appendable_object_upload(
            _ZONAL_BUCKET, object_name, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert f"Appendable object {object_name} created and finalized." in out
    blob = json_client.bucket(_ZONAL_BUCKET).get_blob(object_name)
    blob.delete()


def test_storage_pause_and_resume_appendable_upload(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-pause-resume-{uuid.uuid4()}"
    event_loop.run_until_complete(
        storage_pause_and_resume_appendable_upload.storage_pause_and_resume_appendable_upload(
            _ZONAL_BUCKET, object_name, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert "First writer closed. Upload is 'paused'." in out
    assert "Second writer closed. Full object uploaded." in out

    blob = json_client.bucket(_ZONAL_BUCKET).get_blob(object_name)
    blob.delete()


def test_storage_read_appendable_object_tail(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-read-tail-{uuid.uuid4()}"
    event_loop.run_until_complete(
        storage_read_appendable_object_tail.read_appendable_object_tail(
            _ZONAL_BUCKET, object_name, duration=3, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert f"Created empty appendable object: {object_name}" in out
    assert "Appender started." in out
    assert "Tailer started." in out
    assert "Tailer read" in out
    assert "Tailer finished." in out
    assert "Writer closed." in out

    bucket = json_client.bucket(_ZONAL_BUCKET)
    blob = bucket.blob(object_name)
    blob.delete()


def test_storage_open_object_read_full_object(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-open-read-full-{uuid.uuid4()}"
    data = b"Hello, is it me you're looking for?"
    event_loop.run_until_complete(
        create_appendable_object(async_grpc_client, object_name, data)
    )
    event_loop.run_until_complete(
        storage_open_object_read_full_object.storage_open_object_read_full_object(
            _ZONAL_BUCKET, object_name, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert (
        f"Downloaded all {len(data)} bytes from object {object_name} in bucket {_ZONAL_BUCKET}."
        in out
    )
    blob = json_client.bucket(_ZONAL_BUCKET).blob(object_name)
    blob.delete()


def test_storage_open_object_single_ranged_read(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-open-single-range-{uuid.uuid4()}"
    event_loop.run_until_complete(
        create_appendable_object(
            async_grpc_client, object_name, b"Hello, is it me you're looking for?"
        )
    )
    download_size = 5
    event_loop.run_until_complete(
        storage_open_object_single_ranged_read.storage_open_object_single_ranged_read(
            _ZONAL_BUCKET,
            object_name,
            start_byte=0,
            size=download_size,
            grpc_client=async_grpc_client,
        )
    )
    out, _ = capsys.readouterr()
    assert f"Downloaded {download_size} bytes from {object_name}" in out
    blob = json_client.bucket(_ZONAL_BUCKET).blob(object_name)
    blob.delete()


def test_storage_open_object_multiple_ranged_read(
    async_grpc_client, json_client, event_loop, capsys
):
    object_name = f"test-open-multi-range-{uuid.uuid4()}"
    data = b"a" * 100
    event_loop.run_until_complete(
        create_appendable_object(async_grpc_client, object_name, data)
    )
    event_loop.run_until_complete(
        storage_open_object_multiple_ranged_read.storage_open_object_multiple_ranged_read(
            _ZONAL_BUCKET, object_name, grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert "Downloaded 10 bytes into buffer 1 from start byte 0: b'aaaaaaaaaa'" in out
    assert "Downloaded 10 bytes into buffer 2 from start byte 20: b'aaaaaaaaaa'" in out
    assert "Downloaded 10 bytes into buffer 3 from start byte 40: b'aaaaaaaaaa'" in out
    assert "Downloaded 10 bytes into buffer 4 from start byte 60: b'aaaaaaaaaa'" in out
    blob = json_client.bucket(_ZONAL_BUCKET).blob(object_name)
    blob.delete()


def test_storage_open_multiple_objects_ranged_read(
    async_grpc_client, json_client, event_loop, capsys
):
    blob1_name = f"multi-obj-1-{uuid.uuid4()}"
    blob2_name = f"multi-obj-2-{uuid.uuid4()}"
    data1 = b"Content of object 1"
    data2 = b"Content of object 2"
    event_loop.run_until_complete(
        create_appendable_object(async_grpc_client, blob1_name, data1)
    )
    event_loop.run_until_complete(
        create_appendable_object(async_grpc_client, blob2_name, data2)
    )

    event_loop.run_until_complete(
        storage_open_multiple_objects_ranged_read.storage_open_multiple_objects_ranged_read(
            _ZONAL_BUCKET, [blob1_name, blob2_name], grpc_client=async_grpc_client
        )
    )
    out, _ = capsys.readouterr()
    assert f"Downloaded {len(data1)} bytes from {blob1_name}" in out
    assert f"Downloaded {len(data2)} bytes from {blob2_name}" in out
    blob1 = json_client.bucket(_ZONAL_BUCKET).blob(blob1_name)
    blob2 = json_client.bucket(_ZONAL_BUCKET).blob(blob2_name)
    blob1.delete()
    blob2.delete()
