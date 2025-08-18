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

import datetime

from . import quickstart


def now_millis():
    return int(
        (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        * 1000
    )


def test_quickstart_wo_snapshot(capsys, project_id):
    quickstart.main(project_id)
    out, _ = capsys.readouterr()
    assert "unique names in states: WA" in out


def test_quickstart_with_snapshot(capsys, project_id):
    quickstart.main(project_id, now_millis() - 5000)
    out, _ = capsys.readouterr()
    assert "unique names in states: WA" in out
