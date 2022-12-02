# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setup_cleanup import create_bq_dataset, create_bq_table, \
    upload_data_to_bq_table

dataset = "user_events"
valid_events_table = "events"
invalid_events_table = "events_some_invalid"
events_schema = "../resources/events_schema.json"
valid_events_source_file = "../resources/user_events.json"
invalid_events_source_file = "../resources/user_events_some_invalid.json"

create_bq_dataset(dataset)
create_bq_table(dataset, valid_events_table, events_schema)
upload_data_to_bq_table(dataset, valid_events_table, valid_events_source_file,
                        events_schema)
create_bq_table(dataset, invalid_events_table, events_schema)
upload_data_to_bq_table(dataset, invalid_events_table,
                        invalid_events_source_file, events_schema)
