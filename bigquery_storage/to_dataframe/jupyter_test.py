# Copyright 2019 Google LLC
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

import IPython
from IPython.terminal import interactiveshell
from IPython.testing import tools
import pytest

# Ignore semicolon lint warning because semicolons are used in notebooks
# flake8: noqa E703


@pytest.fixture(scope="session")
def ipython():
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture()
def ipython_interactive(request, ipython):
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """
    with ipython.builtin_trap:
        yield ipython


def _strip_region_tags(sample_text):
    """Remove blank lines and region tags from sample text"""
    magic_lines = [
        line for line in sample_text.split("\n") if len(line) > 0 and "# [" not in line
    ]
    return "\n".join(magic_lines)


def test_jupyter_small_query(ipython):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    # Include a small query to demonstrate that it falls back to the
    # tabledata.list API when the BQ Storage API cannot be used.
    sample = """
    # [START bigquerystorage_jupyter_tutorial_fallback]
    %%bigquery stackoverflow --use_bqstorage_api
    SELECT
      CONCAT(
        'https://stackoverflow.com/questions/',
        CAST(id as STRING)) as url,
      view_count
    FROM `bigquery-public-data.stackoverflow.posts_questions`
    WHERE tags like '%google-bigquery%'
    ORDER BY view_count DESC
    LIMIT 10
    # [END bigquerystorage_jupyter_tutorial_fallback]
    """

    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.
    if "stackoverflow" not in ip.user_ns:
        raise AssertionError


@pytest.mark.skipif(
    "TRAVIS" in os.environ, reason="Not running long-running queries on Travis"
)
def test_jupyter_tutorial(ipython):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    # This code sample intentionally queries a lot of data to demonstrate the
    # speed-up of using the BigQuery Storage API to download the results.
    sample = """
    # [START bigquerystorage_jupyter_tutorial_query]
    %%bigquery nodejs_deps --use_bqstorage_api
    SELECT
        dependency_name,
        dependency_platform,
        project_name,
        project_id,
        version_number,
        version_id,
        dependency_kind,
        optional_dependency,
        dependency_requirements,
        dependency_project_id
    FROM
        `bigquery-public-data.libraries_io.dependencies`
    WHERE
        LOWER(dependency_platform) = 'npm'
    LIMIT 2500000
    # [END bigquerystorage_jupyter_tutorial_query]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    if "nodejs_deps" not in ip.user_ns:
        raise AssertionError
    nodejs_deps = ip.user_ns["nodejs_deps"]

    # [START bigquerystorage_jupyter_tutorial_results]
    nodejs_deps.head()
    # [END bigquerystorage_jupyter_tutorial_results]

    # [START bigquerystorage_jupyter_tutorial_context]
    import google.cloud.bigquery.magics

    google.cloud.bigquery.magics.context.use_bqstorage_api = True
    # [END bigquerystorage_jupyter_tutorial_context]

    sample = """
    # [START bigquerystorage_jupyter_tutorial_query_default]
    %%bigquery java_deps
    SELECT
        dependency_name,
        dependency_platform,
        project_name,
        project_id,
        version_number,
        version_id,
        dependency_kind,
        optional_dependency,
        dependency_requirements,
        dependency_project_id
    FROM
        `bigquery-public-data.libraries_io.dependencies`
    WHERE
        LOWER(dependency_platform) = 'maven'
    LIMIT 2500000
    # [END bigquerystorage_jupyter_tutorial_query_default]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    if "java_deps" not in ip.user_ns:
        raise AssertionError
