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


def get_routine(client, routine_id):

    # [START bigquery_get_routine]
    # TODO(developer): Import the client library.
    # from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set the fully-qualified ID for the routine.
    # routine_id = "my-project.my_dataset.my_routine"

    routine = client.get_routine(routine_id)

    print("Routine `{}`:".format(routine.reference))
    print("  Type: '{}'".format(routine.type_))
    print("  Language: '{}'".format(routine.language))
    print("  Arguments:")

    for argument in routine.arguments:
        print("    Name: '{}'".format(argument.name))
        print("    Type: '{}'".format(argument.type_))
    # [END bigquery_get_routine]
    return routine
