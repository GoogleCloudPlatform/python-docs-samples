# Copyright 2018 Google LLC
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

from __future__ import print_function

import random
import string

import backoff
from google.api_core.exceptions import DeadlineExceeded
import pytest

import snippets


def random_name(length):
    return "".join([random.choice(string.ascii_lowercase) for i in range(length)])


class UptimeFixture:
    """A test fixture that creates uptime check config."""

    def __init__(self):
        self.project_id = snippets.project_id()
        self.project_name = snippets.project_name()

    def __enter__(self):
        # Create an uptime check config (GET request).
        self.config_get = snippets.create_uptime_check_config_get(
            self.project_name, display_name=random_name(10)
        )
        # Create an uptime check config (POST request).
        self.config_post = snippets.create_uptime_check_config_post(
            self.project_name, display_name=random_name(10)
        )
        return self

    def __exit__(self, type, value, traceback):
        # Delete the config.
        snippets.delete_uptime_check_config(self.config_get.name)
        snippets.delete_uptime_check_config(self.config_post.name)


@pytest.fixture(scope="session")
def uptime():
    with UptimeFixture() as uptime:
        yield uptime


def test_create_and_delete() -> None:
    # create and delete happen in uptime fixture.
    with UptimeFixture():
        pass


def test_update_uptime_config() -> None:
    # create and delete happen in uptime fixture.
    new_display_name = random_name(10)
    new_uptime_check_path = "/" + random_name(10)
    with UptimeFixture() as fixture:
        # We sometimes see the permission error saying the resource
        # may not exist. Weirdly DeadlineExceeded instance is raised
        # in this case.
        @backoff.on_exception(backoff.expo, DeadlineExceeded, max_time=120)
        def call_sample():
            return snippets.update_uptime_check_config(
                fixture.config_get.name, new_display_name, new_uptime_check_path
            )

        result = call_sample()

        assert new_display_name == result.display_name
        assert new_uptime_check_path == result.http_check.path


def test_get_uptime_check_config(uptime) -> None:
    config = snippets.get_uptime_check_config(uptime.config_get.name)
    assert uptime.config_get.display_name == config.display_name


def test_list_uptime_check_configs(uptime) -> None:
    result = snippets.list_uptime_check_configs(uptime.project_name)
    assert any(item.display_name == uptime.config_get.display_name for item in result)


def test_list_uptime_check_ips() -> None:
    result = snippets.list_uptime_check_ips()
    assert any(item.location == "Singapore" for item in result)
