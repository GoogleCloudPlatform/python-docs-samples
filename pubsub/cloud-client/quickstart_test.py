# Copyright 2016 Google Inc. All Rights Reserved.
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

from google.cloud import pubsub
import pytest

import quickstart


# Must match the dataset listed in quickstart.py (there's no easy way to
# extract this).
TOPIC_NAME = 'my-new-topic'


@pytest.fixture
def temporary_topic():
    """Fixture that ensures the test dataset does not exist before or
    after a test."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(TOPIC_NAME)

    if topic.exists():
        topic.delete()

    yield

    if topic.exists():
        topic.delete()


def test_quickstart(capsys, temporary_topic):
    quickstart.run_quickstart()
    out, _ = capsys.readouterr()
    assert TOPIC_NAME in out
