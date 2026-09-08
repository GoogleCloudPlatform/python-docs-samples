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

import typing

if typing.TYPE_CHECKING:
    from google.cloud import bigquery


def get_routine(routine_id: str) -> "bigquery.Routine":
    # [START bigquery_get_routine]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set the fully-qualified ID for the routine.
    # routine_id = "my-project.my_dataset.my_routine"

    routine = client.get_routine(routine_id)  # Make an API request.

    print("Routine '{}':".format(routine.reference))
    print("\tType: '{}'".format(routine.type_))
    print("\tLanguage: '{}'".format(routine.language))
    print("\tArguments:")

    for argument in routine.arguments:
        print("\t\tName: '{}'".format(argument.name))
        print("\t\tType: '{}'".format(argument.data_type))
    # [END bigquery_get_routine]
    return routine
