# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START bigtable_quickstart]
# Imports the Google Cloud client library
from google.cloud import bigtable

# The ID of the Cloud Bigtable project
project_id = "my-project-id"
# The ID of the Cloud Bigtable instance
instance_id = 'my-bigtable-instance'
# The ID of the Cloud Bigtable table
table_id = 'my-table'

# Creates a Bigtable client
client = bigtable.Client(project=project_id)
# Connect to an existing instance:my-bigtable-instance
instance = client.instance(instance_id)
# Connect to an existing table:my-table
table = instance.table(table_id)
# Read a row from my-table using a row key
singleRow = table.read_row('r1')

# Print the row key and data (column value, labels, timestamp)
cf = singleRow.cells.keys()[0]
col = singleRow.cells[cf].keys()[0]
row = singleRow.cells[cf][col][0].value
timestamp = singleRow.cells[cf][col][0].timestamp

print "\nColumn Family:", cf, \
            "\nColumn id:", col, \
            "\nRow value:", row, \
            "\ntimestamp:", timestamp, \
            "\n"

# [END bigtable_quickstart]
