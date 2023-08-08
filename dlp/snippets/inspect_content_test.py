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
import random
import time
from typing import Iterator

from unittest import mock
from unittest.mock import MagicMock

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
def bucket() -> Iterator[google.cloud.storage.bucket.Bucket]:
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
def topic_id() -> Iterator[str]:
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
def subscription_id(topic_id: str) -> Iterator[str]:
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
def datastore_project() -> Iterator[str]:
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
    def cleanup() -> None:
        datastore_client.delete(key)

    cleanup()


@pytest.fixture(scope="module")
def bigquery_project() -> Iterator[str]:
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
    def cleanup() -> None:
        bigquery_client.delete_dataset(dataset_ref, delete_contents=True)

    cleanup()


def test_inspect_phone_number(capsys: pytest.CaptureFixture) -> None:
    test_string = "String with a phone number: 234-555-6789"

    inspect_content.inspect_phone_number(GCLOUD_PROJECT, test_string)

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Quote: 234-555-6789" in out


def test_inspect_string(capsys: pytest.CaptureFixture) -> None:
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


def test_inspect_string_augment_infotype(capsys: pytest.CaptureFixture) -> None:
    inspect_content.inspect_string_augment_infotype(
        GCLOUD_PROJECT,
        "The patient's name is Quasimodo",
        "PERSON_NAME",
        ["quasimodo"],
    )
    out, _ = capsys.readouterr()
    assert "Quote: Quasimodo" in out
    assert "Info type: PERSON_NAME" in out


def test_inspect_table(capsys: pytest.CaptureFixture) -> None:
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


def test_inspect_column_values_w_custom_hotwords(capsys):
    table_data = {
        "header": ["Fake Social Security Number", "Real Social Security Number"],
        "rows": [
            ["111-11-1111", "222-22-2222"],
            ["987-23-1234", "333-33-3333"],
            ["678-12-0909", "444-44-4444"],
        ],
    }
    inspect_content.inspect_column_values_w_custom_hotwords(
        GCLOUD_PROJECT,
        table_data["header"],
        table_data["rows"],
        ["US_SOCIAL_SECURITY_NUMBER"],
        "Fake Social Security Number",
    )
    out, _ = capsys.readouterr()
    assert "Info type: US_SOCIAL_SECURITY_NUMBER" in out
    assert "222-22-2222" in out
    assert "111-11-1111" not in out


def test_inspect_string_with_custom_info_types(capsys: pytest.CaptureFixture) -> None:
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


def test_inspect_string_no_results(capsys: pytest.CaptureFixture) -> None:
    test_string = "Nothing to see here"

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_file(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_file_with_custom_info_types(capsys: pytest.CaptureFixture) -> None:
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


def test_inspect_file_no_results(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "harmless.txt")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "No findings" in out


def test_inspect_image_file(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
        include_quote=True,
    )

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out


def test_inspect_image_file_all_infotypes(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_image_file_all_infotypes(GCLOUD_PROJECT, test_filepath)

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_image_file_default_infotypes(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_image_file(GCLOUD_PROJECT, test_filepath)

    out, _ = capsys.readouterr()
    assert "Info type: PHONE_NUMBER" in out
    assert "Info type: EMAIL_ADDRESS" in out


def test_inspect_image_file_listed_infotypes(capsys: pytest.CaptureFixture) -> None:
    test_filepath = os.path.join(RESOURCE_DIRECTORY, "test.png")

    inspect_content.inspect_image_file_listed_infotypes(
        GCLOUD_PROJECT,
        test_filepath,
        ["EMAIL_ADDRESS"],
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out


def delete_dlp_job(out: str) -> None:
    for line in str(out).split("\n"):
        if "Job name" in line:
            job_name = line.split(":")[1].strip()
            DLP_CLIENT.delete_dlp_job(name=job_name)


def mock_job_and_subscriber(
    mock_dlp_instance: MagicMock,
    mock_subscriber_instance: MagicMock,
    dlp_job_path: str,
    finding_name: str = None,
    finding_count: int = None,
):
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = dlp_job_path

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = dlp_job_path
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    # mock result of GetDlpJob DLP method.
    if finding_name:
        finding = mock_job.inspect_details.result.info_type_stats.info_type
        finding.name = finding_name
        mock_job.inspect_details.result.info_type_stats = [
            MagicMock(info_type=finding, count=finding_count),
        ]
    else:
        mock_job.inspect_details.result.info_type_stats = None

    # Mock class for google.cloud.pubsub.subscriber.message.Message
    class MockMessage:
        def __init__(self, data, attributes=None):
            self.data = data
            self.attributes = attributes or {}

        def ack(self):
            pass

    # Replace the real subscribe logic with a custom side effect
    def mock_subscribe(*args, **kwargs):
        # Get the callback function from the arguments.
        callback = kwargs.get("callback")

        # In this example, we'll call the callback function with a mock message
        message = MockMessage(args, {"DlpJobName": dlp_job_path})
        callback(message)

    # Patch the original method with the mock function
    mock_subscriber_instance.subscribe = mock_subscribe


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_file(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        1,
    )

    # Call the sample.
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        "MY_BUCKET",
        "test.txt",
        "topic_id",
        "subscription_id",
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Job name:" in out
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_file_with_custom_info_types(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        1,
    )

    dictionaries = ["gary@somedomain.com"]
    regexes = ["\\(\\d{3}\\) \\d{3}-\\d{4}"]

    # Call the sample.
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        "MY_BUCKET",
        "test.txt",
        "topic_id",
        "subscription_id",
        [],
        custom_dictionaries=dictionaries,
        custom_regexes=regexes,
        timeout=1,
    )

    out, _ = capsys.readouterr()

    assert "Info type: EMAIL_ADDRESS" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_file_no_results(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
    )

    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        "MY_BUCKET",
        "harmless.txt",
        "topic_id",
        "subscription_id",
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=TIMEOUT,
    )

    out, _ = capsys.readouterr()

    assert "No findings" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_image_file(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        1,
    )

    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        "MY_BUCKET",
        "test.png",
        "topic_id",
        "subscription_id",
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_multiple_files(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        random.randint(0, 1000),
    )

    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        "MY_BUCKET",
        "*",
        "topic_id",
        "subscription_id",
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=1,
    )

    out, _ = capsys.readouterr()

    assert "Info type: EMAIL_ADDRESS" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_gcs_with_sampling(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        random.randint(0, 1000),
    )

    # Call the sample
    inspect_content.inspect_gcs_with_sampling(
        GCLOUD_PROJECT,
        "GCS_BUCKET",
        "topic_id",
        "subscription_id",
        ["EMAIL_ADDRESS", "PHONE_NUMBER"],
        ["TEXT_FILE"],
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Inspection operation started:" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_datastore(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:
    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        random.randint(0, 1000),
    )

    inspect_content.inspect_datastore(
        GCLOUD_PROJECT,
        "datastore_project",
        "DATASTORE_KIND",
        "topic_id",
        "subscription_id",
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=TIMEOUT,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@backoff.on_exception(backoff.expo, TimeoutError, max_time=60)
def test_inspect_datastore_no_results(
    datastore_project: str,
    topic_id: str,
    subscription_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
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
    except AssertionError as e:
        if "No event received before the timeout" in str(e):
            raise TimeoutError
        raise e
    finally:
        delete_dlp_job(out)


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_bigquery(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "EMAIL_ADDRESS",
        random.randint(0, 1000),
    )

    # Call the sample.
    inspect_content.inspect_bigquery(
        GCLOUD_PROJECT,
        "BIGQUERY_PROJECT",
        "BIGQUERY_DATASET_ID",
        "BIGQUERY_TABLE_ID",
        "topic_id",
        "subscription_id",
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Inspection operation started" in out
    assert "Job name:" in out
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_bigquery_with_sampling(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job',
        "PERSON_NAME",
        random.randint(0, 1000),
    )

    # Call the sample.
    inspect_content.inspect_bigquery_table_with_sampling(
        GCLOUD_PROJECT,
        "topic_id",
        "subscription_id",
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Inspection operation started" in out
    assert "Job name:" in out
    assert "Info type: PERSON_NAME" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_data_to_hybrid_job_trigger(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock ActivateJobTrigger DLP method and its behavior.
    mock_dlp_instance.activate_job_trigger.return_value.name = "test_job"

    # Configure the mock HybridInspectJobTrigger DLP method and its behavior.
    mock_dlp_instance.hybrid_inspect_job_trigger.return_value = ""

    # The string to inspect.
    content_string = "My email is test@example.org"

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = "test_job"
    mock_job.inspect_details.result.processed_bytes = len(content_string)
    mock_job.inspect_details.result.info_type_stats.info_type.name = "EMAIL_ADDRESS"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the method.
    inspect_content.inspect_data_to_hybrid_job_trigger(
        GCLOUD_PROJECT,
        "test_trigger_id",
        content_string,
    )

    out, _ = capsys.readouterr()
    assert "Job name:" in out
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.hybrid_inspect_job_trigger.assert_called_once()
    mock_dlp_instance.activate_job_trigger.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_gcs_send_to_scc(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = (
        f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    )

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    file = open(os.path.join(RESOURCE_DIRECTORY, "test.txt"), "r")
    # read the content of file
    data = file.read()
    # get the length of the data
    number_of_characters = len(data)

    mock_job.inspect_details.result.processed_bytes = number_of_characters
    mock_job.inspect_details.result.info_type_stats.info_type.name = "EMAIL_ADDRESS"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the sample.
    inspect_content.inspect_gcs_send_to_scc(
        GCLOUD_PROJECT,
        f"{TEST_BUCKET_NAME}//test.txt",
        ["EMAIL_ADDRESS"],
        100,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_bigquery_send_to_scc(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = (
        f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    )

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"

    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    mock_job.inspect_details.result.info_type_stats.info_type.name = "PERSON_NAME"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the sample.
    inspect_content.inspect_bigquery_send_to_scc(
        GCLOUD_PROJECT,
        ["PERSON_NAME"],
    )

    out, _ = capsys.readouterr()
    assert "Info type: PERSON_NAME" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_datastore_send_to_scc(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = (
        f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    )

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    mock_job.inspect_details.result.info_type_stats.info_type.name = "EMAIL_ADDRESS"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the sample.
    inspect_content.inspect_datastore_send_to_scc(
        GCLOUD_PROJECT,
        GCLOUD_PROJECT,
        DATASTORE_KIND,
        ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
