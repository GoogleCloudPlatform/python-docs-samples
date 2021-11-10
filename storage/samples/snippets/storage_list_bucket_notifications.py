#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
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

import sys

"""Sample that lists notification configurations for a bucket.
This sample is used on this page:
    https://cloud.google.com/storage/docs/reporting-changes
For more information, see README.md.
"""

# [START storage_list_bucket_notifications]
from google.cloud import storage


def list_bucket_notifications(bucket_name):
    """Lists notification configurations for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    notifications = bucket.list_notifications()

    for notification in notifications:
        print(f"Notification ID: {notification.notification_id}")

# [END storage_list_bucket_notifications]


if __name__ == "__main__":
    list_bucket_notifications(bucket_name=sys.argv[1])
