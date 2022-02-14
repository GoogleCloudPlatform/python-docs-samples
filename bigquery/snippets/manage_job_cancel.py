# Copyright 2016-2022 Google LLC
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

# [START bigquery_cancel_job]
from google.cloud import bigquery


def cancel_job(
    client: bigquery.Client, location: str = "us", job_id: str = "abcd-efgh-ijkl-mnop",
):
    job = client.cancel_job(job_id, location=location)
    print(f"{job.location}:{job.job_id} cancelled")


# [END bigquery_cancel_job]
