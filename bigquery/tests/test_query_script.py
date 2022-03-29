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

from .. import query_script


def test_query_script(
    capsys,
):

    query_script.query_script()
    out, _ = capsys.readouterr()
    assert "Script created 2 child jobs." in out
    assert (
        "53 of the top 100 names from year 2000 also appear in Shakespeare's works."
        in out
    )
    assert "produced 53 row(s)" in out
    assert "produced 1 row(s)" in out
