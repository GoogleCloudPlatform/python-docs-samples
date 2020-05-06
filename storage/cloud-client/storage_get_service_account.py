#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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


# [START storage_get_service_account]
from google.cloud import storage


def get_service_account():
    """Get the service account email"""
    storage_client = storage.Client()

    email = storage_client.get_service_account_email()
    print(
        "The GCS service account for project {} is: {} ".format(
            storage_client.project, email
        )
    )


# [END storage_get_service_account]

if __name__ == "__main__":
    get_service_account()
