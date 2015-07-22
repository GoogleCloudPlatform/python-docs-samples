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
# [START all]
import json
import logging

import create_client


def main():
    """Transfer from standard Cloud Storage to Cloud Storage Nearline."""
    logging.getLogger().setLevel(logging.DEBUG)
    transfer_service_client = create_client.create_transfer_client()

    # Edit this template with desired parameters.
    # Specify times below using US Pacific Time Zone.
    transfer_job = '''
    {
        "description": "YOUR DESCRIPTION",
        "status": "ENABLED",
        "projectId": "YOUR_PROJECT_ID",
        "schedule": {
            "scheduleStartDate": {
                "day": 1,
                "month": 1,
                "year": 2015
            },
            "startTimeOfDay": {
                "hours": 1,
                "minutes": 1
            }
        },
        "transferSpec": {
            "gcsDataSource": {
                "bucketName": "YOUR_SOURCE_BUCKET"
            },
            "gcsDataSink": {
                "bucketName": "YOUR_SINK_BUCKET"
            },
            "objectConditions": {
                "minTimeElapsedSinceLastModification": "2592000s"
            },
            "transferOptions": {
                "deleteObjectsFromSourceAfterTransfer": true
            }
        }
    }
    '''
    result = transfer_service_client.transferJobs().create(body=json.loads(
        transfer_job)).execute()
    logging.info('Returned transferJob: %s', json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
# [END all]
