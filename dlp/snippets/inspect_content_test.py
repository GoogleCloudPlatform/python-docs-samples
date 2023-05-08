# Copyright 2023 Google LLC
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

import os
import time
import uuid

import backoff
import google.api_core.exceptions
from google.api_core.exceptions import ServiceUnavailable
import google.cloud.bigquery
import google.cloud.datastore
import google.cloud.dlp_v2
import google.cloud.exceptions
import google.cloud.pubsub
import google.cloud.storage
import pytest

import inspect_content

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
RESOURCE_FILE_NAMES = ["test.txt", "test.png", "harmless.txt", "accounts.txt"]
TOPIC_ID = "dlp-test" + UNIQUE_STRING
SUBSCRIPTION_ID = "dlp-test-subscription" + UNIQUE_STRING
DATASTORE_KIND = "DLP test kind"
DATASTORE_NAME = "DLP test object" + UNIQUE_STRING
BIGQUERY_DATASET_ID = "dlp_test_dataset" + UNIQUE_STRING
BIGQUERY_TABLE_ID = "dlp_test_table" + UNIQUE_STRING

TIMEOUT = 900  # 15 minutes

DLP_CLIENT = google.cloud.dlp_v2.DlpServiceClient()


@pytest.fixture(scope="module")
def bucket():
    # Creates a GCS bucket, uploads files required for the test, and tears down
    # the entire bucket afterwards.

    client = google.cloud.storage.Client()
    try:
        bucket = client.get_bucket(TEST_BUCKET_NAME)
    except google.cloud.exceptions.NotFound:
        bucket = client.create_bucket(TEST_BUCKET_NAME)

    # Upoad the blobs and keep track of them in a list.
    blobs = []
    for name in RESOURCE_FILE_NAMES:
        path = os.path.join(RESOURCE_DIRECTORY, name)
        blob = bucket.blob(name)
        blob.upload_from_filename(path)
        blobs.append(blob)

    # Yield the object to the test; lines after this execute as a teardown.
    yield bucket

    # Delete the files.
    for blob in blobs:
        try:
            blob.delete()
        except google.cloud.exceptions.NotFound:
            print("Issue during teardown, missing blob")

    # Attempt to delete the bucket; this will only work if it is empty.
    bucket.delete()


@pytest.fixture(scope="module")
def topic_id():
    # Creates a pubsub topic, and tears it down.
    publisher = google.cloud.pubsub.PublisherClient()
    topic_path = publisher.topic_path(GCLOUD_PROJECT, TOPIC_ID)
    try:
        publisher.create_topic(request={"name": topic_path})
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield TOPIC_ID

    publisher.delete_topic(request={"topic": topic_path})


@pytest.fixture(scope="module")
def subscription_id(topic_id):
    # Subscribes to a topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(GCLOUD_PROJECT, topic_id)
    subscription_path = subscriber.subscription_path(GCLOUD_PROJECT, SUBSCRIPTION_ID)
    try:
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield SUBSCRIPTION_ID

    subscriber.delete_subscription(request={"subscription": subscription_path})


@pytest.fixture(scope="module")
def datastore_project():
    # Adds test Datastore data, yields the project ID and then tears down.
    datastore_client = google.cloud.datastore.Client()

    kind = DATASTORE_KIND
    name = DATASTORE_NAME
    key = datastore_client.key(kind, name)
    item = google.cloud.datastore.Entity(key=key)
    item["payload"] = "My name is Gary Smith and my email is gary@example.com"

    datastore_client.put(item)

    yield GCLOUD_PROJECT

    @backoff.on_exception(backoff.expo, ServiceUnavailable, max_time=120)
    def cleanup():
        datastore_client.delete(key)

    cleanup()


@pytest.fixture(scope="module")
def bigquery_project():
    # Adds test Bigquery data, yields the project ID and then tears down.
    bigquery_client = google.cloud.bigquery.Client()

    dataset_ref = bigquery_client.dataset(BIGQUERY_DATASET_ID)
    dataset = google.cloud.bigquery.Dataset(dataset_ref)
    try:
        dataset = bigquery_client.create_dataset(dataset)
    except google.api_core.exceptions.Conflict:
        dataset = bigquery_client.get_dataset(dataset)

    table_ref = dataset_ref.table(BIGQUERY_TABLE_ID)
    table = google.cloud.bigquery.Table(table_ref)

    # DO NOT SUBMIT: trim this down once we find out what works
    table.schema = (
        google.cloud.bigquery.SchemaField("Name", "STRING"),
        google.cloud.bigquery.SchemaField("Comment", "STRING"),
    )

    try:
        table = bigquery_client.create_table(table)
        time.sleep(30)
    except google.api_core.exceptions.Conflict:
        table = bigquery_client.get_table(table)

    rows_to_insert = [("Gary Smith", "My email is gary@example.com")]

    bigquery_client.insert_rows(table, rows_to_insert)

    yield GCLOUD_PROJECT

    @backoff.on_exception(backoff.expo, ServiceUnavailable, max_time=120)
    def cleanup():
        bigquery_client.delete_dataset(dataset_ref, delete_contents=True)

    cleanup()


def test_inspect_string_basic(capsys):
    test_string = "String with a phone number: 234-555-6789"

    inspect_content.inspect_string_basic(GCLOUD_PROJECT, test_string)

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Quote: 234-555-6789" in out


def test_inspect_string(capsys):
    test_string = "My name is Gary Smith and my email is gary@example.com"

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: FIRST_NAME" in out
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_table(capsys):
    test_tabular_data = {
        "header": ["email", "phone number"],
        "rows": [
            ["robertfrost@xyz.com", "4232342345"],
            ["johndoe@pqr.com", "4253458383"],
        ],
    }

    inspect_content.inspect_table(
        GCLOUD_PROJECT,
        test_tabular_data,
        ["PHONE_NUMBER", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_string_with_custom_info_types(capsys):
    test_string = "My name is Gary Smith and my email is gary@example.com"
    dictionaries = ["Gary Smith"]
    regexes = ["\\w+@\\w+.com"]

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        [],
        custom_dictionaries=dictionaries,
        custom_regexes=regexes,
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: CUSTOM_DICTIONARY_0" in out
    assert "Info type: CUSTOM_REGEX_0" in out


def test_inspect_string_no_results(capsys):
    test_string = "Nothing to see here"

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_file_with_custom_info_types(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.txt")
    dictionaries = ["gary@somedomain.com"]
    regexes = ["\\(\\d{3}\\) \\d{3}-\\d{4}"]

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        [],
        custom_dictionaries=dictionaries,
        custom_regexes=regexes,
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: CUSTOM_DICTIONARY_0" in out
    assert "Info type: CUSTOM_REGEX_0" in out


def test_inspect_file_no_results(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "harmless.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_image_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out


def test_inspect_image_file_all_infotypes(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_image_file_all_infotypes(
        GCLOUD_PROJECT,
        test_filepath
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Info type: EMAIL_ADDRESS" in out


def delete_dlp_job(out):
    for line in str(out).split("\n"):
        if "Job name" in line:
            job_name = line.split(":")[1].strip()
            DLP_CLIENT.delete_dlp_job(name=job_name)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_file(bucket, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_gcs_file(
            GCLOUD_PROJECT,
            bucket.name,
            "test.txt",
            topic_id,
            subscription_id,
            ["EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()
        assert "Info type: EMAIL_ADDRESS" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_file_with_custom_info_types(
    bucket, topic_id, subscription_id, capsys
):
    out = ""
    try:
        dictionaries = ["gary@somedomain.com"]
        regexes = ["\\(\\d{3}\\) \\d{3}-\\d{4}"]

        inspect_content.inspect_gcs_file(
            GCLOUD_PROJECT,
            bucket.name,
            "test.txt",
            topic_id,
            subscription_id,
            [],
            custom_dictionaries=dictionaries,
            custom_regexes=regexes,
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()

        assert "Info type: EMAIL_ADDRESS" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_file_no_results(bucket, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_gcs_file(
            GCLOUD_PROJECT,
            bucket.name,
            "harmless.txt",
            topic_id,
            subscription_id,
            ["EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()

        assert "No findings" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_image_file(bucket, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_gcs_file(
            GCLOUD_PROJECT,
            bucket.name,
            "test.png",
            topic_id,
            subscription_id,
            ["EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()
        assert "Info type: EMAIL_ADDRESS" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_multiple_files(bucket, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_gcs_file(
            GCLOUD_PROJECT,
            bucket.name,
            "*",
            topic_id,
            subscription_id,
            ["EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()

        assert "Info type: EMAIL_ADDRESS" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_datastore(datastore_project, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_datastore(
            GCLOUD_PROJECT,
            datastore_project,
            DATASTORE_KIND,
            topic_id,
            subscription_id,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()
        assert "Info type: EMAIL_ADDRESS" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_datastore_no_results(
    datastore_project, topic_id, subscription_id, capsys
):
    out = ""
    try:
        inspect_content.inspect_datastore(
            GCLOUD_PROJECT,
            datastore_project,
            DATASTORE_KIND,
            topic_id,
            subscription_id,
            ["PHONE_NUMBER"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()
        assert "No findings" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.skip(reason="Table not found error. Should be inspected.")
@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_bigquery(bigquery_project, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_bigquery(
            GCLOUD_PROJECT,
            bigquery_project,
            BIGQUERY_DATASET_ID,
            BIGQUERY_TABLE_ID,
            topic_id,
            subscription_id,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            timeout=1,
        )

        out, _ = capsys.readouterr()
        assert "Inspection operation started" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)


@pytest.mark.flaky(max_runs=2, min_passes=1)
def test_inspect_gcs_with_sampling(bucket, topic_id, subscription_id, capsys):
    out = ""
    try:
        inspect_content.inspect_gcs_with_sampling(
            GCLOUD_PROJECT,
            bucket.name,
            topic_id,
            subscription_id,
            ["EMAIL_ADDRESS", "PHONE_NUMBER"],
            ["TEXT_FILE"],
            timeout=TIMEOUT,
        )

        out, _ = capsys.readouterr()
        assert "Inspection operation started:" in out
        assert "Job name:" in out
    finally:
        delete_dlp_job(out)
