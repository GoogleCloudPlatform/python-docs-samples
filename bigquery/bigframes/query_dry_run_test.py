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

import bigframes.pandas as bpd
import pytest

import query_dry_run


def test_query_dry_run(project_id: str, capsys: pytest.CaptureFixture) -> None:
    bpd.close_session()

    sql_stats, df_stats = query_dry_run.query_dry_run(project_id=project_id)
    out, _ = capsys.readouterr()

    assert sql_stats["totalBytesProcessed"] > 0
    assert df_stats["totalBytesProcessed"] > 0
    assert "bytes" in out
