# Copyright 2020 Google LLC
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

from typing import Dict, Mapping, Optional, Sequence


def insert_wkt(
    override_values: Optional[Mapping[str, str]] = None
) -> Sequence[Dict[str, object]]:

    if override_values is None:
        override_values = {}

    # [START bigquery_insert_geography_wkt]
    from google.cloud import bigquery
    import shapely.geometry
    import shapely.wkt

    bigquery_client = bigquery.Client()

    # This example uses a table containing a column named "geo" with the
    # GEOGRAPHY data type.
    table_id = "my-project.my_dataset.my_table"
    # [END bigquery_insert_geography_wkt]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    table_id = override_values.get("table_id", table_id)
    # [START bigquery_insert_geography_wkt]

    # Use the Shapely library to generate WKT of a line from LAX to
    # JFK airports. Alternatively, you may define WKT data directly.
    my_geography = shapely.geometry.LineString(
        [(-118.4085, 33.9416), (-73.7781, 40.6413)]
    )
    rows = [
        # Convert data into a WKT string.
        {"geo": shapely.wkt.dumps(my_geography)},
    ]

    #  table already exists and has a column
    # named "geo" with data type GEOGRAPHY.
    errors = bigquery_client.insert_rows_json(table_id, rows)
    if errors:
        raise RuntimeError(f"row insert failed: {errors}")
    else:
        print(f"wrote 1 row to {table_id}")
    # [END bigquery_insert_geography_wkt]
    return errors
