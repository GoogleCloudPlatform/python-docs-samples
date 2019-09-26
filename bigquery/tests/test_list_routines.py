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


from .. import list_routines


def test_list_routines(capsys, client, dataset_id, routine_id):

    list_routines.list_routines(client, dataset_id)
    out, err = capsys.readouterr()
    assert "Routines contained in dataset {}:".format(dataset_id) in out
    assert routine_id in out
