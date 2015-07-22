# Copyright 2015, Google, Inc.
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
#
import json
import logging

import create_client

# Edit these values with desired parameters.
PROJECT_ID = 'YOUR_PROJECT_ID'
JOB_NAME = 'YOUR_JOB_NAME'


def check_operation(transfer_service_client, project_id, job_name):
    """Review the transfer operations associated with a transfer job."""
    filterString = (
        '{{"project_id": "{project_id}", '
        '"job_names": ["{job_name}"]}}').format(
        project_id=project_id, job_name=job_name)
    return transfer_service_client.transferOperations().list(
        name="transferOperations",
        filter=filterString).execute()


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    transfer_service_client = create_client.create_transfer_client()

    result = check_operation(transfer_service_client, PROJECT_ID, JOB_NAME)
    logging.info('Result of transferOperations/list: %s',
                 json.dumps(result, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
