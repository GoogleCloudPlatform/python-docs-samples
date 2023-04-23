#!/usr/bin/env python

# Copyright 2021 Google LLC

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

# [START storagetransfer_create_retry_handler_apiary]

"""Command-line sample that gets a transfer job using retries
"""

import googleapiclient.discovery


def get_transfer_job_with_retries(project_id, job_name, retries):
    """Check the latest transfer operation associated with a transfer job."""
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")

    transferJob = (
        storagetransfer.transferJobs()
        .get(projectId=project_id, jobName=job_name)
        .execute(num_retries=retries)
    )
    print(
        "Fetched transfer job: "
        + transferJob.get("name")
        + f" using {retries} retries"
    )
# [END storagetransfer_create_retry_handler_apiary]
