# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import NoReturn, TypeVar

from click.testing import CliRunner
from unittest.mock import MagicMock, patch
import pytest

from check_status import cli

a = TypeVar("a")

MOCK_SERVICE_NAME = "myservice"
MOCK_GH_TOKEN = "aaaaa"
MOCK_REPO_NAME = "foocorp/bar"
MOCK_PR_NUMBER = 1
MOCK_COMMIT_SHA = "f000bee"
MOCK_PROJECT_ID = "foocorp"


runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_settings_env_vars() -> NoReturn:
    with patch.dict(os.environ, {"GITHUB_TOKEN": MOCK_GH_TOKEN}):
        yield


def test_help() -> NoReturn:
    response = runner.invoke(cli, ["--help"])
    assert response.exit_code == 0
    assert "Usage" in response.output


def test_set_no_project() -> NoReturn:
    response = runner.invoke(cli, ["set"])
    assert response.exit_code == 2
    assert "Missing option '--project-id'" in response.output


def service_data(name: str, tags: list[str]) -> dict:
    traffic = [
        {
            "revisionName": f"{name}-00001-aaa",
            "percent": 100,
        }
    ]
    for t in tags:
        tag = f"pr-{t}"
        traffic.append(
            {
                "tag": tag,
                "revisionName": f"{name}-00002-bbb",
                "url": f"https://{tag}---{name}-yyyyyy-uc-a.run.app",
            }
        )
    return {"metadata": {"name": name}, "status": {"traffic": traffic}}


@patch("check_status.discovery")
def test_set_wrongtag(discovery_mock: a) -> NoReturn:
    service_mock = MagicMock()
    service_mock.projects = MagicMock(return_value=service_mock)
    service_mock.locations = MagicMock(return_value=service_mock)
    service_mock.services = MagicMock(return_value=service_mock)
    service_mock.get = MagicMock(return_value=service_mock)
    service_mock.execute = MagicMock(
        return_value=service_data(MOCK_SERVICE_NAME, [MOCK_PR_NUMBER])
    )
    discovery_mock.build = MagicMock(return_value=service_mock)

    invalid_pr = MOCK_PR_NUMBER + 1  # intentionally wrong

    response = runner.invoke(
        cli,
        [
            "set",
            "--project-id",
            MOCK_PROJECT_ID,
            "--region",
            "us-central1",
            "--service",
            MOCK_SERVICE_NAME,
            "--repo-name",
            MOCK_REPO_NAME,
            "--commit-sha",
            MOCK_COMMIT_SHA,
            "--pull-request",
            invalid_pr,
            "--dry-run",
        ],
    )
    print(response.output)
    assert response.exit_code == 1
    assert "Error finding revision" in response.output
    assert f"pr-{invalid_pr}" in response.output


@patch("check_status.discovery")
@patch("check_status.github")
def test_set_check_calls(github_mock: a, discovery_mock: a) -> NoReturn:
    service_mock = MagicMock()
    service_mock.projects = MagicMock(return_value=service_mock)
    service_mock.locations = MagicMock(return_value=service_mock)
    service_mock.services = MagicMock(return_value=service_mock)
    service_mock.get = MagicMock(return_value=service_mock)
    service_mock.execute = MagicMock(
        return_value=service_data(MOCK_SERVICE_NAME, [MOCK_PR_NUMBER])
    )
    discovery_mock.build = MagicMock(return_value=service_mock)

    gh_mock = MagicMock()
    gh_mock.get_repo = MagicMock(return_value=gh_mock)
    gh_mock.repo_name = MOCK_REPO_NAME
    gh_mock.get_commit = MagicMock(return_value=gh_mock)
    gh_mock.sha = MOCK_COMMIT_SHA
    gh_mock.create_status = MagicMock(return_value=True)
    github_mock.Github = MagicMock(return_value=gh_mock)

    # Test Status Dry-Run
    response = runner.invoke(
        cli,
        [
            "set",
            "--project-id",
            MOCK_PROJECT_ID,
            "--region",
            "us-central1",
            "--service",
            MOCK_SERVICE_NAME,
            "--repo-name",
            MOCK_REPO_NAME,
            "--commit-sha",
            MOCK_COMMIT_SHA,
            "--pull-request",
            MOCK_PR_NUMBER,
            "--dry-run",
        ],
    )
    assert response.exit_code == 0
    assert "Dry-run" in response.output

    assert MOCK_SERVICE_NAME in response.output
    assert MOCK_REPO_NAME in response.output
    assert MOCK_COMMIT_SHA in response.output

    # Test Status real-run
    response = runner.invoke(
        cli,
        [
            "set",
            "--project-id",
            MOCK_PROJECT_ID,
            "--region",
            "us-central1",
            "--service",
            MOCK_SERVICE_NAME,
            "--repo-name",
            MOCK_REPO_NAME,
            "--commit-sha",
            MOCK_COMMIT_SHA,
            "--pull-request",
            MOCK_PR_NUMBER,
        ],
    )

    assert response.exit_code == 0
    assert "Success" in response.output

    assert MOCK_SERVICE_NAME in response.output
    assert MOCK_REPO_NAME in response.output
    assert MOCK_COMMIT_SHA in response.output
