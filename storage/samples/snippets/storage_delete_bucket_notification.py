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

"""Sample that deletes a notification configuration for a bucket.
This sample is used on this page:
    https://cloud.google.com/storage/docs/reporting-changes
For more information, see README.md.
"""

# [START storage_delete_bucket_notification]
from google.cloud import storage


def delete_bucket_notification(bucket_name, notification_id):
    """Deletes a notification configuration for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of the notification
    # notification_id = "your-notification-id"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    notification = bucket.notification(notification_id=notification_id)
    notification.delete()

    print(f"Successfully deleted notification with ID {notification_id} for bucket {bucket_name}")

# [END storage_delete_bucket_notification]


if __name__ == "__main__":
    delete_bucket_notification(bucket_name=sys.argv[1], notification_id=sys.argv[2])
