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

# [START storage_download_file_requester_pays]
from google.cloud import storage


def download_file_requester_pays(
    bucket_name, project_id, source_blob_name, destination_file_name
):
    """Download file using specified project as the requester"""
    # bucket_name = "your-bucket-name"
    # project_id = "your-project-id"
    # source_blob_name = "source-blob-name"
    # destination_file_name = "local-destination-file-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name, user_project=project_id)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {} using a requester-pays request.".format(
            source_blob_name, destination_file_name
        )
    )


# [END storage_download_file_requester_pays]

if __name__ == "__main__":
    download_file_requester_pays(
        bucket_name=sys.argv[1],
        project_id=sys.argv[2],
        source_blob_name=sys.argv[3],
        destination_file_name=sys.argv[4],
    )
