#!/usr/bin/env python

# Copyright 2019 Google, Inc.
#
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

import sys

# [START storage_get_requester_pays_status]
from google.cloud import storage


def get_requester_pays_status(bucket_name):
    """Get a bucket's requester pays metadata"""
    # bucket_name = "my-bucket"
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    requester_pays_status = bucket.requester_pays

    if requester_pays_status:
        print("Requester Pays is enabled for {}".format(bucket_name))
    else:
        print("Requester Pays is disabled for {}".format(bucket_name))


# [END storage_get_requester_pays_status]

if __name__ == "__main__":
    get_requester_pays_status(bucket_name=sys.argv[1])
