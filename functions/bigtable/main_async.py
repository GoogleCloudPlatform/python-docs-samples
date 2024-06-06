# Copyright 2024 Google LLC
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

# [START bigtable_functions_quickstart_asyncio]
import asyncio

import functions_framework
from google.cloud.bigtable.data import BigtableDataClientAsync, ReadRowsQuery, RowRange

event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)


# Setup: create a shared client within the context of the event loop
async def create_client():
    # create client in the asyncio event loop context to
    # give background tasks a chance to initialize
    return BigtableDataClientAsync()


client = event_loop.run_until_complete(create_client())


# Actual cloud functions entrypoint, will delegate to the async one
@functions_framework.http
def bigtable_read_data(request):
    return event_loop.run_until_complete(_bigtable_read_data_async(request))


# Actual handler
async def _bigtable_read_data_async(request):
    async with client.get_table(
        request.headers.get("instance_id"), request.headers.get("table_id")
    ) as table:

        prefix = "phone#"
        end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)

        outputs = []
        query = ReadRowsQuery(row_ranges=[RowRange(start_key=prefix, end_key=end_key)])

        async for row in await table.read_rows_stream(query):
            print("%s" % row)
            output = "Rowkey: {}, os_build: {}".format(
                row.row_key.decode("utf-8"),
                row.get_cells("stats_summary", b"os_build")[0].value.decode("utf-8"),
            )
            outputs.append(output)

        return "\n".join(outputs)


# [END bigtable_functions_quickstart_asyncio]
