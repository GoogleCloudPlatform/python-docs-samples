#!/usr/bin/env python

# Copyright 2019, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START bigtable_writes_conditional]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import row_filters


def write_conditional(project_id, instance_id, table_id):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    timestamp = datetime.datetime.utcnow()
    column_family_id = "stats_summary"

    row_key = "phone#4c410523#20190501"

    row_filter = row_filters.RowFilterChain(
        filters=[row_filters.FamilyNameRegexFilter(column_family_id),
                 row_filters.ColumnQualifierRegexFilter('os_build'),
                 row_filters.ValueRegexFilter("PQ2A\\..*")])
    row = table.row(row_key, filter_=row_filter)
    row.set_cell(column_family_id,
                 "os_name",
                 "android",
                 timestamp)
    row.commit()

    print('Successfully updated row\'s os_name.')
# [END bigtable_writes_conditional]
