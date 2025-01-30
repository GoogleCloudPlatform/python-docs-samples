# Copyright 2020 Google, LLC.
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

import os

from flask import Flask
from flask import make_response
from google.cloud import storage

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get():
    bucket_name = os.environ["CLOUD_STORAGE_BUCKET"]
    blob_name = os.environ["BLOB_NAME"]

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    response_text = ""

    text_to_store = b"abcde\n" + b"f" * 1024 * 4 + b"\n"
    blob.upload_from_string(text_to_store)
    response_text += "Stored text in a blob.\n\n"

    stored_contents = blob.download_as_bytes()
    if stored_contents == text_to_store:
        response_text += "Downloaded text matches uploaded text.\n\n"
    else:
        response_text += "Downloaded text DOES NOT MATCH uploaded text!\n\n"

    bucket.delete_blob(blob_name)
    response_text += "Blob " + blob_name + " deleted.\n"

    response = make_response(response_text, 200)
    response.mimetype = "text/plain"
    return response


if __name__ == "__main__":
    # This is used when running locally.
    app.run(host="127.0.0.1", port=8080, debug=True)
