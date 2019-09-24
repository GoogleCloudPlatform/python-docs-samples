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
    assert "stackoverflow" in ip.user_ns  # verify that variable exists


def test_jupyter_tutorial(ipython):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    # This code sample intentionally queries a lot of data to demonstrate the
    # speed-up of using the BigQuery Storage API to download the results.
    sample = """
    # [START bigquerystorage_jupyter_tutorial_query]
    %%bigquery tax_forms --use_bqstorage_api
    SELECT * FROM `bigquery-public-data.irs_990.irs_990_2012`
    # [END bigquerystorage_jupyter_tutorial_query]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    assert "tax_forms" in ip.user_ns  # verify that variable exists
    tax_forms = ip.user_ns["tax_forms"]

    # [START bigquerystorage_jupyter_tutorial_results]
    tax_forms.head()
    # [END bigquerystorage_jupyter_tutorial_results]

    # [START bigquerystorage_jupyter_tutorial_context]
    import google.cloud.bigquery.magics

    google.cloud.bigquery.magics.context.use_bqstorage_api = True
    # [END bigquerystorage_jupyter_tutorial_context]

    sample = """
    # [START bigquerystorage_jupyter_tutorial_query_default]
    %%bigquery tax_forms
    SELECT * FROM `bigquery-public-data.irs_990.irs_990_2012`
    # [END bigquerystorage_jupyter_tutorial_query_default]
    """
    result = ip.run_cell(_strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.

    assert "tax_forms" in ip.user_ns  # verify that variable exists
