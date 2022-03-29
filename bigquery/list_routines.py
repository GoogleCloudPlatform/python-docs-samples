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


def list_routines(dataset_id: str) -> None:

    # [START bigquery_list_routines]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset that contains
    #                  the routines you are listing.
    # dataset_id = 'your-project.your_dataset'

    routines = client.list_routines(dataset_id)  # Make an API request.

    print("Routines contained in dataset {}:".format(dataset_id))
    for routine in routines:
        print(routine.reference)
    # [END bigquery_list_routines]
