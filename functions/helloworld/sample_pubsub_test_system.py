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

# [START functions_pubsub_system_test]
from datetime import datetime
from os import getenv
import subprocess
import time
import uuid

from google.cloud import pubsub_v1
import pytest

PROJECT = getenv('GCP_PROJECT')
TOPIC = getenv('FUNCTIONS_TOPIC')

assert PROJECT is not None
assert TOPIC is not None


@pytest.fixture(scope='module')
def publisher_client():
    yield pubsub_v1.PublisherClient()


def test_print_name(publisher_client):
    start_time = datetime.utcnow().isoformat()
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    # Publish the message
    name = uuid.uuid4()
    data = str(name).encode('utf-8')
    publisher_client.publish(topic_path, data=data).result()

    # Wait for logs to become consistent
    time.sleep(15)

    # Check logs after a delay
    log_process = subprocess.Popen([
        'gcloud',
        'alpha',
        'functions',
        'logs',
        'read',
        'hello_pubsub',
        '--start-time',
        start_time
    ], stdout=subprocess.PIPE)
    logs = str(log_process.communicate()[0])
    assert f'Hello {name}!' in logs
# [END functions_pubsub_system_test]
