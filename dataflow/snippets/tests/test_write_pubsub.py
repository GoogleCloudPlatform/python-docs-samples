# !/usr/bin/env python
#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys
import uuid

from _pytest.capture import CaptureFixture
from google.cloud import pubsub_v1

import pytest

from ..write_pubsub import write_to_pubsub


topic_id = f'test-topic-{uuid.uuid4()}'
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

publisher = pubsub_v1.PublisherClient()


@pytest.fixture(scope="function")
def setup_and_teardown():
    topic_path = publisher.topic_path(project_id, topic_id)
    try:
        publisher.create_topic(request={"name": topic_path})
        yield
    finally:
        publisher.delete_topic(request={"topic": topic_path})


def test_write_to_pubsub(setup_and_teardown, capsys: CaptureFixture[str]):
    sys.argv = [
        '',
        '--streaming',
        f'--project={project_id}',
        f'--topic={topic_id}'
    ]
    write_to_pubsub()

    out, _ = capsys.readouterr()
    assert 'Pipeline ran successfully' in out
