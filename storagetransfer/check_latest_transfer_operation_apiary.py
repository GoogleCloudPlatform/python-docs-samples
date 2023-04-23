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

# [START storagetransfer_get_latest_transfer_operation_apiary]

"""Command-line sample that checks the latest operation of a transfer.
This sample is used on this page:
    https://cloud.google.com/storage/transfer/create-transfer
For more information, see README.md.
"""

import argparse
import json

import googleapiclient.discovery


def check_latest_transfer_operation(project_id, job_name):
    """Check the latest transfer operation associated with a transfer job."""
    storagetransfer = googleapiclient.discovery.build("storagetransfer", "v1")

    transferJob = (
        storagetransfer.transferJobs()
        .get(projectId=project_id, jobName=job_name)
        .execute()
    )
    latestOperationName = transferJob.get("latestOperationName")

    if latestOperationName:
        result = (
            storagetransfer.transferOperations().get(name=latestOperationName).execute()
        )
        print(
            "The latest operation for job"
            + job_name
            + f" is: {json.dumps(result, indent=4, sort_keys=True)}"
        )

    else:
        print(
            "Transfer job "
            + job_name
            + " does not have an operation scheduled yet, "
            + "try again once the job starts running."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID.")
    parser.add_argument("job_name", help="Your job name.")

    args = parser.parse_args()

    check_latest_transfer_operation(args.project_id, args.job_name)
# [END storagetransfer_get_latest_transfer_operation_apiary]
