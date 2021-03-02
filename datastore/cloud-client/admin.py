# Copyright 2016 Google, Inc.
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

# [START datastore_admin_client_create]
from google.cloud.datastore_admin_v1 import DatastoreAdminClient


def client_create():
    """Creates a new Datastore admin client."""
    client = DatastoreAdminClient()

    print("Admin client created\n")
    return client


# [END datastore_admin_client_create]


# [START datastore_admin_entities_export]
def export_entities(project_id, output_url_prefix):
    """
    Exports a copy of all or a subset of entities from
    Datastore to another storage system, such as Cloud Storage.
    """
    # project_id = "project-id"
    # output_url_prefix = "gs://bucket-name"
    client = DatastoreAdminClient()

    op = client.export_entities(
        {"project_id": project_id, "output_url_prefix": output_url_prefix}
    )
    response = op.result(timeout=300)

    print("Entities were exported\n")
    return response


# [END datastore_admin_entities_export]


# [START datastore_admin_entities_import]
def import_entities(project_id, input_url):
    """Imports entities into Datastore."""
    # project_id := "project-id"
    # input_url := "gs://bucket-name/overall-export-metadata-file"
    client = DatastoreAdminClient()

    op = client.import_entities(
        {"project_id": project_id, "input_url": input_url}
    )
    response = op.result(timeout=300)

    print("Entities were imported\n")
    return response


# [END datastore_admin_entities_import]


# [START datastore_admin_index_get]
def get_index(project_id, index_id):
    """Gets an index."""
    # project_id := "my-project-id"
    # index_id := "my-index"
    client = DatastoreAdminClient()
    index = client.get_index({"project_id": project_id, "index_id": index_id})

    print("Got index: %v\n", index.index_id)
    return index


# [END datastore_admin_index_get]


# [START datastore_admin_index_list]
def list_indexes(project_id):
    """Lists the indexes."""
    # project_id := "my-project-id"
    client = DatastoreAdminClient()

    indexes = []
    for index in client.list_indexes({"project_id": project_id}):
        indexes.append(index)
        print("Got index: %v\n", index.index_id)

    print("Got list of indexes\n")
    return indexes


# [END datastore_admin_index_list]
