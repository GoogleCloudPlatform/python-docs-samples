# Copyright 2021 Google LLC
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

import create_table_external_hive_partitioned


def test_create_table_external_hive_partitioned(capsys, random_table_id):
    table = create_table_external_hive_partitioned.create_table_external_hive_partitioned(
        random_table_id
    )

    out, _ = capsys.readouterr()
    hive_partioning = table.external_data_configuration.hive_partitioning
    assert "Created table {}".format(random_table_id) in out
    assert (
        hive_partioning.source_uri_prefix
        == "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/"
    )
    assert hive_partioning.require_partition_filter is True
    assert hive_partioning.mode == "AUTO"
