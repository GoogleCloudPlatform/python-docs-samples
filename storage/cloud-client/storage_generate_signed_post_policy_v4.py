#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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

# [START storage_generate_signed_post_policy_v4]
from google.cloud import storage
import datetime


def generate_signed_post_policy_v4(bucket_name, blob_name):
    """Generates a v4 POST Policy and prints an HTML form."""
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()

    policy = storage_client.generate_signed_post_policy_v4(
        bucket_name,
        object_name,
        expiration=datetime.timedelta(minutes=10),
    )

    # Create an HTML form with the provided policy
    form_html = "<form action='{}' method='POST' enctype='multipart/form-data'>\n".format(policy["url"])

    # Include all fields returned in the HTML form as they're required
    for index, (key, value) in enumerate(policy["fields"].items()):
      form_html += "  <input name='{}' value='{}' type='hidden'/>\n".format(key, value)

    form_html += "  <input type='file' name='file'/><br />\n"
    form_html += "  <input type='submit' value='Upload File' name='submit'/><br />\n"
    form_html += "</form>"

    print(form_html)

    return form_html


# [END storage_generate_signed_post_policy_v4]

if __name__ == "__main__":
    generate_signed_post_policy_v4(
        bucket_name=sys.argv[1], blob_name=sys.argv[2]
    )
