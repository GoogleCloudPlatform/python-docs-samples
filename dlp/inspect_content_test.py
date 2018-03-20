# Copyright 2017 Google Inc.
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

from gcp_devrel.testing import eventually_consistent
from gcp_devrel.testing.flaky import flaky
import google.api_core.exceptions
import google.cloud.bigquery
import google.cloud.datastore
import google.cloud.exceptions
import google.cloud.pubsub
import google.cloud.storage

import pytest

import inspect_content


GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_BUCKET_NAME = GCLOUD_PROJECT + '-dlp-python-client-test'
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCE_FILE_NAMES = ['test.txt', 'test.png', 'harmless.txt', 'accounts.txt']
TOPIC_ID = 'dlp-test'
SUBSCRIPTION_ID = 'dlp-test-subscription'
DATASTORE_KIND = 'DLP test kind'
BIGQUERY_DATASET_ID = 'dlp_test_dataset'
BIGQUERY_TABLE_ID = 'dlp_test_table'


@pytest.fixture(scope='module')
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
        blob.delete()

    # Attempt to delete the bucket; this will only work if it is empty.
    bucket.delete()


@pytest.fixture(scope='module')
def topic_id():
    # Creates a pubsub topic, and tears it down.
    publisher = google.cloud.pubsub.PublisherClient()
    topic_path = publisher.topic_path(GCLOUD_PROJECT, TOPIC_ID)
    try:
        publisher.create_topic(topic_path)
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield TOPIC_ID

    publisher.delete_topic(topic_path)


@pytest.fixture(scope='module')
def subscription_id(topic_id):
    # Subscribes to a topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(GCLOUD_PROJECT, topic_id)
    subscription_path = subscriber.subscription_path(
        GCLOUD_PROJECT, SUBSCRIPTION_ID)
    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield SUBSCRIPTION_ID

    subscriber.delete_subscription(subscription_path)


@pytest.fixture(scope='module')
def datastore_project():
    # Adds test Datastore data, yields the project ID and then tears down.
    datastore_client = google.cloud.datastore.Client()

    kind = DATASTORE_KIND
    name = 'DLP test object'
    key = datastore_client.key(kind, name)
    item = google.cloud.datastore.Entity(key=key)
    item['payload'] = 'My name is Gary Smith and my email is gary@example.com'

    datastore_client.put(item)

    yield GCLOUD_PROJECT

    datastore_client.delete(key)


@pytest.fixture(scope='module')
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
        google.cloud.bigquery.SchemaField('Name', 'STRING'),
        google.cloud.bigquery.SchemaField('Comment', 'STRING'),
    )

    try:
        table = bigquery_client.create_table(table)
    except google.api_core.exceptions.Conflict:
        table = bigquery_client.get_table(table)

    rows_to_insert = [
        (u'Gary Smith', u'My email is gary@example.com',)
    ]

    bigquery_client.insert_rows(table, rows_to_insert)

    yield GCLOUD_PROJECT

    bigquery_client.delete_dataset(dataset_ref, delete_contents=True)


def test_inspect_string(capsys):
    test_string = 'My name is Gary Smith and my email is gary@example.com'

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ['FIRST_NAME', 'EMAIL_ADDRESS'],
        include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: FIRST_NAME' in out
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_string_no_results(capsys):
    test_string = 'Nothing to see here'

    inspect_content.inspect_string(
        GCLOUD_PROJECT,
        test_string,
        ['FIRST_NAME', 'EMAIL_ADDRESS'],
        include_quote=True)

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'test.txt')

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ['FIRST_NAME', 'EMAIL_ADDRESS'],
        include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_file_no_results(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'harmless.txt')

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ['FIRST_NAME', 'EMAIL_ADDRESS'],
        include_quote=True)

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_image_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'test.png')

    inspect_content.inspect_file(
        GCLOUD_PROJECT,
        test_filepath,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'],
        include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out


@flaky
def test_inspect_gcs_file(bucket, topic_id, subscription_id, capsys):
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        bucket.name,
        'test.txt',
        topic_id,
        subscription_id,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


@flaky
def test_inspect_gcs_file_no_results(
        bucket, topic_id, subscription_id, capsys):
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        bucket.name,
        'harmless.txt',
        topic_id,
        subscription_id,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'No findings' in out


@pytest.mark.skip(reason='nondeterministically failing')
def test_inspect_gcs_image_file(bucket, topic_id, subscription_id, capsys):
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        bucket.name,
        'test.png',
        topic_id,
        subscription_id,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


@flaky
def test_inspect_gcs_multiple_files(bucket, topic_id, subscription_id, capsys):
    inspect_content.inspect_gcs_file(
        GCLOUD_PROJECT,
        bucket.name,
        '*',
        topic_id,
        subscription_id,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out
    assert 'Info type: PHONE_NUMBER' in out


@flaky
def test_inspect_datastore(
        datastore_project, topic_id, subscription_id, capsys):
    @eventually_consistent.call
    def _():
        inspect_content.inspect_datastore(
            GCLOUD_PROJECT,
            datastore_project,
            DATASTORE_KIND,
            topic_id,
            subscription_id,
            ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

        out, _ = capsys.readouterr()
        assert 'Info type: EMAIL_ADDRESS' in out


@flaky
def test_inspect_datastore_no_results(
        datastore_project, topic_id, subscription_id, capsys):
    inspect_content.inspect_datastore(
        GCLOUD_PROJECT,
        datastore_project,
        DATASTORE_KIND,
        topic_id,
        subscription_id,
        ['PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'No findings' in out


@pytest.mark.skip(reason='unknown issue')
def test_inspect_bigquery(
        bigquery_project, topic_id, subscription_id, capsys):
    inspect_content.inspect_bigquery(
        GCLOUD_PROJECT,
        bigquery_project,
        BIGQUERY_DATASET_ID,
        BIGQUERY_TABLE_ID,
        topic_id,
        subscription_id,
        ['FIRST_NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER'])

    out, _ = capsys.readouterr()
    assert 'Info type: FIRST_NAME' in out
