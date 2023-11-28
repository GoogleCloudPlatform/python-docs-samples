# Copyright 2023 Google LLC
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

"""Sample app that uses the Data Loss Prevent API to perform risk anaylsis."""


import argparse


# [START dlp_k_anonymity_with_entity_id]
import time
from typing import List

import google.cloud.dlp_v2
from google.cloud.dlp_v2 import types


def k_anonymity_with_entity_id(
    project: str,
    source_table_project_id: str,
    source_dataset_id: str,
    source_table_id: str,
    entity_id: str,
    quasi_ids: List[str],
    output_table_project_id: str,
    output_dataset_id: str,
    output_table_id: str,
) -> None:
    """Uses the Data Loss Prevention API to compute the k-anonymity using entity_id
        of a column set in a Google BigQuery table.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        source_table_project_id: The Google Cloud project id where the BigQuery table
            is stored.
        source_dataset_id: The id of the dataset to inspect.
        source_table_id: The id of the table to inspect.
        entity_id: The column name of the table that enables accurately determining k-anonymity
         in the common scenario wherein several rows of dataset correspond to the same sensitive
         information.
        quasi_ids: A set of columns that form a composite key.
        output_table_project_id: The Google Cloud project id where the output BigQuery table
            is stored.
        output_dataset_id: The id of the output BigQuery dataset.
        output_table_id: The id of the output BigQuery table.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Location info of the source BigQuery table.
    source_table = {
        "project_id": source_table_project_id,
        "dataset_id": source_dataset_id,
        "table_id": source_table_id,
    }

    # Specify the bigquery table to store the findings.
    # The output_table_id in the given BigQuery dataset will be created if it doesn't
    # already exist.
    dest_table = {
        "project_id": output_table_project_id,
        "dataset_id": output_dataset_id,
        "table_id": output_table_id,
    }

    # Convert quasi id list to Protobuf type
    def map_fields(field: str) -> dict:
        return {"name": field}

    #  Configure column names of quasi-identifiers to analyze
    quasi_ids = map(map_fields, quasi_ids)

    # Tell the API where to send a notification when the job is complete.
    actions = [{"save_findings": {"output_config": {"table": dest_table}}}]

    # Configure the privacy metric to compute for re-identification risk analysis.
    # Specify the unique identifier in the source table for the k-anonymity analysis.
    privacy_metric = {
        "k_anonymity_config": {
            "entity_id": {"field": {"name": entity_id}},
            "quasi_ids": quasi_ids,
        }
    }

    # Configure risk analysis job.
    risk_job = {
        "privacy_metric": privacy_metric,
        "source_table": source_table,
        "actions": actions,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Call API to start risk analysis job.
    response = dlp.create_dlp_job(
        request={
            "parent": parent,
            "risk_job": risk_job,
        }
    )
    job_name = response.name
    print(f"Inspection Job started : {job_name}")

    # Waiting for a maximum of 15 minutes for the job to be completed.
    job = dlp.get_dlp_job(request={"name": job_name})
    no_of_attempts = 30
    while no_of_attempts > 0:
        # Check if the job has completed
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.DONE:
            break
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.FAILED:
            print("Job Failed, Please check the configuration.")
            return

        # Sleep for a short duration before checking the job status again
        time.sleep(30)
        no_of_attempts -= 1

        # Get the DLP job status
        job = dlp.get_dlp_job(request={"name": job_name})

    if job.state != google.cloud.dlp_v2.DlpJob.JobState.DONE:
        print("Job did not complete within 15 minutes.")
        return

    # Create helper function for unpacking values
    def get_values(obj: types.Value) -> str:
        return str(obj.string_value)

    # Print out the results.
    print(f"Job name: {job.name}")
    histogram_buckets = (
        job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets
    )
    # Print bucket stats
    for i, bucket in enumerate(histogram_buckets):
        print(f"Bucket {i}:")
        if bucket.equivalence_class_size_lower_bound:
            print(
                f"Bucket size range: [{bucket.equivalence_class_size_lower_bound}, "
                f"{bucket.equivalence_class_size_upper_bound}]"
            )
            for value_bucket in bucket.bucket_values:
                print(
                    f"Quasi-ID values: {get_values(value_bucket.quasi_ids_values[0])}"
                )
                print(f"Class size: {value_bucket.equivalence_class_size}")
        else:
            print("No findings.")


# [END dlp_k_anonymity_with_entity_id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "source_table_project_id",
        help="The Google Cloud project id where the BigQuery table is stored.",
    )
    parser.add_argument(
        "source_dataset_id",
        help="The id of the dataset to inspect.",
    )
    parser.add_argument(
        "source_table_id",
        help="The id of the table to inspect.",
    )
    parser.add_argument(
        "entity_id",
        help="The column name of the table that enables accurately "
        "determining k-anonymity",
    )
    parser.add_argument(
        "quasi_ids",
        nargs="+",
        help="A set of columns that form a composite key.",
    )
    parser.add_argument(
        "output_table_project_id",
        help="The Google Cloud project id where the output BigQuery table "
        "would be stored.",
    )
    parser.add_argument(
        "output_dataset_id",
        help="The id of the output BigQuery dataset.",
    )
    parser.add_argument(
        "output_table_id",
        help="The id of the output BigQuery table.",
    )

    args = parser.parse_args()

    k_anonymity_with_entity_id(
        args.project,
        args.source_table_project_id,
        args.source_dataset_id,
        args.source_table_id,
        args.entity_id,
        args.quasi_ids,
        args.output_table_project_id,
        args.output_dataset_id,
        args.output_table_id,
    )
