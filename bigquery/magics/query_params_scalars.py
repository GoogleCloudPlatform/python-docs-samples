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

import typing

import IPython

from . import _helpers

if typing.TYPE_CHECKING:
    import pandas


def query_with_parameters() -> "pandas.DataFrame":
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    sample = """
    # [START bigquery_jupyter_query_params_scalars]
    %%bigquery --params {"corpus_name": "hamlet", "limit": 10}
    SELECT word, SUM(word_count) as count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus_name
    GROUP BY word
    ORDER BY count DESC
    LIMIT @limit
    # [END bigquery_jupyter_query_params_scalars]
    """
    result = ip.run_cell(_helpers.strip_region_tags(sample))
    result.raise_error()  # Throws an exception if the cell failed.
    df = ip.user_ns["_"]  # Retrieves last returned object in notebook session
    return df
