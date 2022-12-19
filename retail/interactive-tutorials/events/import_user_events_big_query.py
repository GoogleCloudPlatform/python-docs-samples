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

import argparse

import google.auth

project_id = google.auth.default()[1]


def main(project_id, dataset_id, table_id):
    # TODO: Set project_id to your Google Cloud Platform project ID.
    # project_id = "my-project"

    # TODO: Set dataset_id
    # dataset_id = "user_events"

    # TODO: Set table_id
    # table_id = "events"

    # Import products into a catalog from big query table using Retail API
    import time

    from google.cloud.retail import (
        BigQuerySource,
        ImportUserEventsRequest,
        UserEventInputConfig,
        UserEventServiceClient,
    )

    default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog"

    # TO CHECK ERROR HANDLING USE THE TABLE OF INVALID USER EVENTS:
    # table_id = "events_some_invalid"

    # get import user events from big query request
    def get_import_events_big_query_request():
        # TO CHECK ERROR HANDLING PASTE THE INVALID CATALOG NAME HERE:
        # default_catalog = "invalid_catalog_name"
        big_query_source = BigQuerySource()
        big_query_source.project_id = project_id
        big_query_source.dataset_id = dataset_id
        big_query_source.table_id = table_id
        big_query_source.data_schema = "user_event"

        input_config = UserEventInputConfig()
        input_config.big_query_source = big_query_source

        import_request = ImportUserEventsRequest()
        import_request.parent = default_catalog
        import_request.input_config = input_config

        print("---import user events from BigQuery source request---")
        print(import_request)

        return import_request

    # call the Retail API to import user events
    def import_user_events_from_big_query():
        import_big_query_request = get_import_events_big_query_request()
        big_query_operation = UserEventServiceClient().import_user_events(
            import_big_query_request
        )

        print("---the operation was started:----")
        print(big_query_operation.operation.name)

        while not big_query_operation.done():
            print("---please wait till operation is done---")
            time.sleep(30)
        print("---import user events operation is done---")

        if big_query_operation.metadata is not None:
            print("---number of successfully imported events---")
            print(big_query_operation.metadata.success_count)
            print("---number of failures during the importing---")
            print(big_query_operation.metadata.failure_count)
        else:
            print("---operation.metadata is empty---")

        if big_query_operation.result is not None:
            print("---operation result:---")
            print(big_query_operation.result())
        else:
            print("---operation.result is empty---")

    import_user_events_from_big_query()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_id", nargs="?", default="user_events")
    parser.add_argument("table_id", nargs="?", default="events")
    args = parser.parse_args()
    main(project_id, args.dataset_id, args.table_id)
