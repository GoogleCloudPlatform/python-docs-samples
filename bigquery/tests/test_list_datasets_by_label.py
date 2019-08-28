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


from .. import list_datasets_by_label


def test_list_datasets_by_label(capsys, client, dataset_id):

    dataset = client.get_dataset(dataset_id)
    dataset.labels = {"color": "green"}
    dataset = client.update_dataset(dataset, ["labels"])
    list_datasets_by_label.list_datasets_by_label(client)
    out, err = capsys.readouterr()
    assert "{}".format(dataset_id) in out
