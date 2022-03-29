# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from .. import client_query_dry_run

if typing.TYPE_CHECKING:
    import pytest


def test_client_query_dry_run(capsys: "pytest.CaptureFixture[str]") -> None:

    query_job = client_query_dry_run.client_query_dry_run()
    out, err = capsys.readouterr()
    assert "This query will process" in out
    assert query_job.state == "DONE"
    assert query_job.dry_run
    assert query_job.total_bytes_processed > 0
