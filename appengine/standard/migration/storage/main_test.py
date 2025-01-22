# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

import os
import uuid

import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    if os.environ.get("CLOUD_STORAGE_BUCKET") is None:
        os.environ["CLOUD_STORAGE_BUCKET"] = "python-docs-samples-tests-public"
    os.environ["BLOB_NAME"] = "storage-migration-test-blob-{}".format(uuid.uuid4().hex)

    r = client.get("/")
    assert r.status_code == 200
    assert "Downloaded text matches uploaded text" in r.data.decode("utf-8")

    blob_name = os.environ["BLOB_NAME"]

    assert "Blob {} deleted.".format(blob_name) in r.data.decode("utf-8")
