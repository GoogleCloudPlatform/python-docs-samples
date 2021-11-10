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

"""Sample that creates a notification configuration for a bucket.
This sample is used on this page:
    https://cloud.google.com/storage/docs/reporting-changes
For more information, see README.md.
"""

# [START storage_create_bucket_notifications]
from google.cloud import storage


def create_bucket_notifications(bucket_name, topic_name):
    """Creates a notification configuration for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The name of a topic
    # topic_name = "your-topic-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    notification = bucket.notification(topic_name=topic_name)
    notification.create()

    print(f"Successfully created notification with ID {notification.notification_id} for bucket {bucket_name}")

# [END storage_create_bucket_notifications]


if __name__ == "__main__":
    create_bucket_notifications(bucket_name=sys.argv[1], topic_name=sys.argv[2])
