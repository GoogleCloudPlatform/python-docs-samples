#!/usr/bin/env python

# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_authorized_view_tutorial(override_values={}):
    # Note to user: This is a group email for testing purposes. Replace with
    # your own group email address when running this code.
    analyst_group_email = "example-analyst-group@google.com"

    # [START bigquery_authorized_view_tutorial]
    # Create a source dataset
    # [START bigquery_avt_create_source_dataset]
    from google.cloud import bigquery
    from google.cloud.bigquery.enums import EntityTypes

    client = bigquery.Client()
    source_dataset_id = "github_source_data"
    source_dataset_id_full = "{}.{}".format(client.project, source_dataset_id)

    # [END bigquery_authorized_view_tutorial]
    # [END bigquery_avt_create_source_dataset]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    source_dataset_id = override_values.get("source_dataset_id", source_dataset_id)
    source_dataset_id_full = "{}.{}".format(client.project, source_dataset_id)
    # [START bigquery_authorized_view_tutorial]
    # [START bigquery_avt_create_source_dataset]

    source_dataset = bigquery.Dataset(source_dataset_id_full)
    # Specify the geographic location where the dataset should reside.
    source_dataset.location = "US"
    source_dataset = client.create_dataset(source_dataset)  # API request
    # [END bigquery_avt_create_source_dataset]

    # Populate a source table
    # [START bigquery_avt_create_source_table]
    source_table_id = "github_contributors"
    job_config = bigquery.QueryJobConfig()
    job_config.destination = source_dataset.table(source_table_id)
    sql = """
        SELECT commit, author, committer, repo_name
        FROM `bigquery-public-data.github_repos.commits`
        LIMIT 1000
    """
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location="US",
        job_config=job_config,
    )  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    # [END bigquery_avt_create_source_table]

    # Create a separate dataset to store your view
    # [START bigquery_avt_create_shared_dataset]
    shared_dataset_id = "shared_views"
    shared_dataset_id_full = "{}.{}".format(client.project, shared_dataset_id)

    # [END bigquery_authorized_view_tutorial]
    # [END bigquery_avt_create_shared_dataset]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    shared_dataset_id = override_values.get("shared_dataset_id", shared_dataset_id)
    shared_dataset_id_full = "{}.{}".format(client.project, shared_dataset_id)
    # [START bigquery_authorized_view_tutorial]
    # [START bigquery_avt_create_shared_dataset]

    shared_dataset = bigquery.Dataset(shared_dataset_id_full)
    shared_dataset.location = "US"
    shared_dataset = client.create_dataset(shared_dataset)  # API request
    # [END bigquery_avt_create_shared_dataset]

    # Create the view in the new dataset
    # [START bigquery_avt_create_view]
    shared_view_id = "github_analyst_view"
    view = bigquery.Table(shared_dataset.table(shared_view_id))
    sql_template = """
        SELECT
            commit, author.name as author,
            committer.name as committer, repo_name
        FROM
            `{}.{}.{}`
    """
    view.view_query = sql_template.format(
        client.project, source_dataset_id, source_table_id
    )
    view = client.create_table(view)  # API request
    # [END bigquery_avt_create_view]

    # Assign access controls to the dataset containing the view
    # [START bigquery_avt_shared_dataset_access]
    # analyst_group_email = 'data_analysts@example.com'
    access_entries = shared_dataset.access_entries
    access_entries.append(
        bigquery.AccessEntry("READER", EntityTypes.GROUP_BY_EMAIL, analyst_group_email)
    )
    shared_dataset.access_entries = access_entries
    shared_dataset = client.update_dataset(
        shared_dataset, ["access_entries"]
    )  # API request
    # [END bigquery_avt_shared_dataset_access]

    # Authorize the view to access the source dataset
    # [START bigquery_avt_source_dataset_access]
    access_entries = source_dataset.access_entries
    access_entries.append(
        bigquery.AccessEntry(None, EntityTypes.VIEW, view.reference.to_api_repr())
    )
    source_dataset.access_entries = access_entries
    source_dataset = client.update_dataset(
        source_dataset, ["access_entries"]
    )  # API request
    # [END bigquery_avt_source_dataset_access]
    # [END bigquery_authorized_view_tutorial]


if __name__ == "__main__":
    run_authorized_view_tutorial()
