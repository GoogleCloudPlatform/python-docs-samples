# Copyright 2026 Google LLC
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

import bigframes_queries
import pytest


@pytest.mark.skip(
    reason="Placeholder project ID 'your-project-id' cannot be executed by pytest, but snippet is required for welcome page documentation."
)
def test_query_standard_sql():
    df = bigframes_queries.query_standard_sql()
    assert df is not None


@pytest.mark.skip(
    reason="Legacy SQL syntax is not supported for execution by BigQuery DataFrames, but snippet is required for welcome page documentation."
)
def test_query_legacy_sql():
    df = bigframes_queries.query_legacy_sql()
    assert df is not None


def test_query_bqstorage():
    pandas_df = bigframes_queries.query_bqstorage()
    assert pandas_df is not None


def test_query_parameters():
    df = bigframes_queries.query_parameters()
    assert df is not None


@pytest.mark.skip(
    reason="Requires a writable destination table so pytest skips execution, but snippet is required for welcome page documentation."
)
def test_upload_from_dataframe():
    bq_df = bigframes_queries.upload_from_dataframe()
    assert bq_df is not None
