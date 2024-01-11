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

"""Uses of the Data Loss Prevention API for deidentifying sensitive data."""

from __future__ import annotations

import argparse


# [START dlp_deidentify_cloud_storage]
import time
from typing import List

import google.cloud.dlp


def deidentify_cloud_storage(
    project: str,
    input_gcs_bucket: str,
    output_gcs_bucket: str,
    info_types: List[str],
    deid_template_id: str,
    structured_deid_template_id: str,
    image_redact_template_id: str,
    dataset_id: str,
    table_id: str,
    timeout: int = 300,
) -> None:
    """
    Uses the Data Loss Prevention API to de-identify files in a Google Cloud
    Storage directory.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        input_gcs_bucket: The name of google cloud storage bucket to inspect.
        output_gcs_bucket: The name of google cloud storage bucket where
            de-identified files would be stored.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        deid_template_id: The name of the de-identify template for
            unstructured and structured files.
        structured_deid_template_id: The name of the de-identify template
            for structured files.
        image_redact_template_id: The name of the image redaction template
            for images.
        dataset_id: The identifier of the BigQuery dataset where transformation
            details would be stored.
        table_id: The identifier of the BigQuery table where transformation
            details would be stored.
        timeout: The number of seconds to wait for a response from the API.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the configuration dictionary.
    # Specify the type of info the inspection will look for.
    # See https://cloud.google.com/dlp/docs/infotypes-reference for complete list of info types.
    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}

    # Construct cloud_storage_options dictionary with the bucket's URL.
    storage_config = {
        "cloud_storage_options": {"file_set": {"url": f"gs://{input_gcs_bucket}"}}
    }

    # Specify the big query table to store the transformation details.
    big_query_table = {
        "project_id": project,
        "dataset_id": dataset_id,
        "table_id": table_id,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}/locations/global"

    # Construct Transformation Configuration with de-identify Templates used
    # for transformation.
    transformation_config = {
        "deidentify_template": f"{parent}/deidentifyTemplates/{deid_template_id}",
        "structured_deidentify_template": f"{parent}/deidentifyTemplates/{structured_deid_template_id}",
        "image_redact_template": f"{parent}/deidentifyTemplates/{image_redact_template_id}",
    }

    # Tell the API where to send notification when the job is completed.
    actions = [
        {
            "deidentify": {
                "cloud_storage_output": f"gs://{output_gcs_bucket}",
                "transformation_config": transformation_config,
                "transformation_details_storage_config": {"table": big_query_table},
                "file_types_to_transform": ["IMAGE", "CSV", "TEXT_FILE"],
            }
        }
    ]

    # Construct the job definition.
    inspect_job = {
        "inspect_config": inspect_config,
        "storage_config": storage_config,
        "actions": actions,
    }

    # Call the API.
    response = dlp.create_dlp_job(
        request={
            "parent": parent,
            "inspect_job": inspect_job,
        }
    )

    job_name = response.name
    print(f"Inspection Job started : {job_name}")

    # Waiting for the job to get completed.
    job = dlp.get_dlp_job(request={"name": job_name})
    # Since the sleep time is kept as 30s, number of calls would be timeout/30.
    no_of_attempts = timeout // 30
    while no_of_attempts != 0:
        # Check if the job has completed.
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.DONE:
            break
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.FAILED:
            print("Job Failed, Please check the configuration.")
            break

        # Sleep for a short duration before checking the job status again.
        time.sleep(30)
        no_of_attempts -= 1

        # Get DLP job status.
        job = dlp.get_dlp_job(request={"name": job_name})

    if job.state != google.cloud.dlp_v2.DlpJob.JobState.DONE:
        print(f"Job did not complete within {timeout} minutes.")
        return

    # Print out the results.
    print(f"Job name: {job.name}")
    result = job.inspect_details.result
    print(f"Processed Bytes: {result.processed_bytes}")
    if result.info_type_stats:
        for stats in result.info_type_stats:
            print(f"Info type: {stats.info_type.name}")
            print(f"Count: {stats.count}")
    else:
        print("No findings.")


# [END dlp_deidentify_cloud_storage]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "input_gcs_bucket",
        help="The name of google cloud storage bucket to inspect.",
    )
    parser.add_argument(
        "output_gcs_bucket",
        help="The name of google cloud storage bucket where "
        "de-identified files would be stored.",
    )
    parser.add_argument(
        "deid_template_id",
        help="The name of the de-identify template for unstructured "
        "and structured files.",
    )
    parser.add_argument(
        "structured_deid_template_id",
        help="The name of the de-identify template for structured files.",
    )
    parser.add_argument(
        "image_redact_template_id",
        help="The name of the image redaction template for images.",
    )
    parser.add_argument(
        "dataset_id",
        help="The identifier of the BigQuery dataset where transformation "
        "details would be stored.",
    )
    parser.add_argument(
        "table_id",
        help="The identifier of the BigQuery table where transformation "
        "details would be stored.",
    )
    parser.add_argument(
        "timeout",
        help="The number of seconds to wait for a response from the API.",
    )

    args = parser.parse_args()

    deidentify_cloud_storage(
        args.project,
        args.input_gcs_bucket,
        args.output_gcs_bucket,
        args.info_types,
        args.deid_template_id,
        args.structured_deid_template_id,
        args.image_redact_template_id,
        args.dataset_id,
        args.table_id,
        args.timeout,
    )
