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

import os
import uuid

import backoff
from google.api_core.exceptions import NotFound
from google.cloud import logging
import pytest

import snippets

TEST_LOGGER_NAME = "example_log_{}".format(uuid.uuid4().hex)
TEST_TEXT = "Hello, world."
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
DEFAULT_LOGGER = f"projects/{GOOGLE_CLOUD_PROJECT}/logs/python"


@pytest.fixture
def example_log():
    client = logging.Client()
    logger = client.logger(TEST_LOGGER_NAME)
    text = "Hello, world."
    logger.log_text(text)
    return text


def test_list(example_log, capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def eventually_consistent_test():
        snippets.list_entries(TEST_LOGGER_NAME)
        out, _ = capsys.readouterr()
        assert example_log in out

    eventually_consistent_test()


def test_write(capsys):

    snippets.write_entry()

    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def eventually_consistent_test():
        # retrieve logs
        client = logging.Client()

        log_filter = DEFAULT_LOGGER

        entries = client.list_entries(
            filter_=log_filter, order_by=logging.DESCENDING, max_results=3
        )

        retrieved_entries = list(entries)

        assert retrieved_entries[0].payload["message"] == "This is a JSON log."
        assert retrieved_entries[1].payload == "Goodbye, world!"
        assert retrieved_entries[2].payload == "Hello, world!"

    eventually_consistent_test()


def test_delete(example_log, capsys):
    @backoff.on_exception(backoff.expo, NotFound, max_time=120)
    def eventually_consistent_test():
        snippets.delete_logger(TEST_LOGGER_NAME)
        out, _ = capsys.readouterr()
        assert TEST_LOGGER_NAME in out

    eventually_consistent_test()
