# Copyright 2019 Google LLC
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

import multiprocessing as mp
import os
import pytest
import subprocess as sp
import tempfile
import time
import uuid

import apache_beam as beam
from google.cloud import pubsub_v1


PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
TOPIC = 'test-topic'
UUID = uuid.uuid4().hex


@pytest.fixture
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture
def topic_path(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.delete_topic(topic_path)
    except Exception:
        pass

    response = publisher_client.create_topic(topic_path)
    yield response.name


def _infinite_publish_job(publisher_client, topic_path):
    while True:
        future = publisher_client.publish(
            topic_path, data='Hello World!'.encode('utf-8'))
        future.result()
        time.sleep(10)


def test_run(publisher_client, topic_path):
    """This is an integration test that runs `PubSubToGCS.py` in its entirety.
    It checks for output files on GCS.
    """

    # Use one process to publish messages to a topic.
    publish_process = mp.Process(
        target=lambda: _infinite_publish_job(publisher_client, topic_path))

    # Use another process to run the streaming pipeline that should write one
    # file to GCS every minute (according to the default window size).
    pipeline_process = mp.Process(
        target=lambda: sp.call([
            'python', 'PubSubToGCS.py',
            '--project', PROJECT,
            '--runner', 'DirectRunner',
            '--temp_location', tempfile.mkdtemp(),
            '--input_topic', topic_path,
            '--output_path', 'gs://{}/pubsub/{}/output'.format(BUCKET, UUID),
        ])
    )

    publish_process.start()
    pipeline_process.start()

    # Times out the streaming pipeline after 90 seconds.
    pipeline_process.join(timeout=90)
    # Immediately kills the publish process after the pipeline shuts down.
    publish_process.join(timeout=0)

    pipeline_process.terminate()
    publish_process.terminate()

    # Check for output files on GCS.
    gcs_client = beam.io.gcp.gcsio.GcsIO()
    # This returns a dictionary.
    files = gcs_client.list_prefix('gs://{}/pubsub/{}'.format(BUCKET, UUID))
    assert len(files) > 0

    # Clean up. Delete topic. Delete files.
    publisher_client.delete_topic(topic_path)
    gcs_client.delete_batch(list(files))
