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


from .. import get_routine


def test_get_routine(capsys, client, routine_id):

    get_routine.get_routine(client, routine_id)
    out, err = capsys.readouterr()
    assert "Routine '{}':".format(routine_id) in out
    assert "Type: 'SCALAR_FUNCTION'" in out
    assert "Language: 'SQL'" in out
    assert "Name: 'x'" in out
    assert "Type: 'type_kind: INT64\n'" in out
