# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bigtable_functions_quickstart]
from google.cloud import bigtable
from google.cloud.bigtable.row_set import RowSet

client = bigtable.Client()


def bigtable_read_data(request):
    instance = client.instance(request.headers.get("instance_id"))
    table = instance.table(request.headers.get("table_id"))

    prefix = 'phone#'
    end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)

    outputs = []
    row_set = RowSet()
    row_set.add_row_range_from_keys(prefix.encode("utf-8"),
                                    end_key.encode("utf-8"))

    rows = table.read_rows(row_set=row_set)
    for row in rows:
        output = 'Rowkey: {}, os_build: {}'.format(
            row.row_key.decode('utf-8'),
            row.cells["stats_summary"][b"os_build"][0]
            .value.decode('utf-8'))
        outputs.append(output)

    return '\n'.join(outputs)

# [END bigtable_functions_quickstart]
