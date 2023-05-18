# Copyright 2018 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import uuid

import backoff
from googleapiclient.errors import HttpError
import pytest

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "datasets"))  # noqa
import datasets  # noqa
import hl7v2_messages  # noqa
import hl7v2_stores  # noqa


location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = f"test_dataset_{uuid.uuid4()}"
hl7v2_store_id = f"test_hl7v2_store-{uuid.uuid4()}"
hl7v2_message_file = "resources/hl7-sample-ingest.json"
label_key = "PROCESSED"
label_value = "TRUE"


@pytest.fixture(scope="module")
def test_dataset():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            datasets.create_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(f"Got exception {err.resp.status} while creating dataset")
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            datasets.delete_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def test_hl7v2_store():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            hl7v2_stores.create_hl7v2_store(
                project_id, location, dataset_id, hl7v2_store_id
            )
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(
                    "Got exception {} while creating HL7v2 store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            hl7v2_stores.delete_hl7v2_store(
                project_id, location, dataset_id, hl7v2_store_id
            )
        except HttpError as err:
            # The API returns 403 when the HL7v2 store doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting HL7v2 store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


def test_CRUD_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.create_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_file
    )

    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def run_eventually_consistent_test():
        hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
            project_id, location, dataset_id, hl7v2_store_id
        )

        assert len(hl7v2_messages_list) > 0
        hl7v2_message_name = hl7v2_messages_list[0].get("name")
        elms = hl7v2_message_name.split("/", 9)
        assert len(elms) >= 10
        hl7v2_message_id = elms[9]
        return hl7v2_message_id

    hl7v2_message_id = run_eventually_consistent_test()

    hl7v2_messages.get_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    hl7v2_messages.delete_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created HL7v2 message" in out
    assert "Name" in out
    assert "Deleted HL7v2 message" in out


def test_ingest_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.ingest_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_file
    )

    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def run_eventually_consistent_test():
        hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
            project_id, location, dataset_id, hl7v2_store_id
        )

        assert len(hl7v2_messages_list) > 0
        hl7v2_message_name = hl7v2_messages_list[0].get("name")
        elms = hl7v2_message_name.split("/", 9)
        assert len(elms) >= 10
        hl7v2_message_id = elms[9]
        return hl7v2_message_id

    hl7v2_message_id = run_eventually_consistent_test()

    hl7v2_messages.get_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    hl7v2_messages.delete_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    out, _ = capsys.readouterr()

    # Check that ingest/get/list/delete worked
    assert "Ingested HL7v2 message" in out
    assert "Name" in out
    assert "Deleted HL7v2 message" in out


def test_patch_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.create_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_file
    )

    @backoff.on_exception(backoff.expo, (AssertionError, HttpError), max_time=60)
    def run_eventually_consistent_test():
        hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
            project_id, location, dataset_id, hl7v2_store_id
        )

        assert len(hl7v2_messages_list) > 0
        hl7v2_message_name = hl7v2_messages_list[0].get("name")
        elms = hl7v2_message_name.split("/", 9)
        assert len(elms) >= 10
        hl7v2_message_id = elms[9]
        return hl7v2_message_id

    hl7v2_message_id = run_eventually_consistent_test()

    hl7v2_messages.patch_hl7v2_message(
        project_id,
        location,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id,
        label_key,
        label_value,
    )

    hl7v2_messages.delete_hl7v2_message(
        project_id, location, dataset_id, hl7v2_store_id, hl7v2_message_id
    )

    out, _ = capsys.readouterr()

    # Check that patch worked
    assert "Patched HL7v2 message" in out
