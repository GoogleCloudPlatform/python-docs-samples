# Copyright 2021 Google LLC
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


def delete_job_metadata(job_id: str, location: str) -> None:
    orig_job_id = job_id
    orig_location = location
    # [START bigquery_delete_job]
    from google.api_core import exceptions
    from google.cloud import bigquery

    # TODO(developer): Set the job ID to the ID of the job whose metadata you
    #                  wish to delete.
    job_id = "abcd-efgh-ijkl-mnop"

    # TODO(developer): Set the location to the region or multi-region
    #                  containing the job.
    location = "us-east1"

    # [END bigquery_delete_job]
    job_id = orig_job_id
    location = orig_location

    # [START bigquery_delete_job]
    client = bigquery.Client()

    client.delete_job_metadata(job_id, location=location)

    try:
        client.get_job(job_id, location=location)
    except exceptions.NotFound:
        print(f"Job metadata for job {location}:{job_id} was deleted.")
    # [END bigquery_delete_job]
