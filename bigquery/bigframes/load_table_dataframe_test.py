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

import load_table_dataframe


def test_load_table_dataframe(project_id: str, dataset_id: str) -> None:
    table_id = f"{project_id}.{dataset_id}.load_table_dataframe"
    import bigframes.pandas as bpd

    bq_df = load_table_dataframe.load_table_dataframe(table_id=table_id)
    assert bq_df is not None

    # Verify that the rows were actually written to BigQuery
    df_loaded = bpd.read_gbq(table_id)
    assert len(df_loaded) == 4
