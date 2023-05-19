# Copyright 2022 Google LLC
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

from flask import Flask, redirect, request
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


# This datastore model keeps track of uploaded photos.
class PhotoUpload(ndb.Model):
    blob_key = ndb.BlobKeyProperty()


# [START gae_blobstore_handler_flask]
class PhotoUploadHandler(blobstore.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads(request.environ)[0]
        photo = PhotoUpload(blob_key=upload.key())
        photo.put()

        return redirect("/view_photo/%s" % upload.key())


class ViewPhotoHandler(blobstore.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            return "Photo key not found", 404
        else:
            headers = self.send_blob(request.environ, photo_key)

            # Prevent Flask from setting a default content-type.
            # GAE sets it to a guessed type if the header is not set.
            headers["Content-Type"] = None
            return "", headers


@app.route("/view_photo/<photo_key>")
def view_photo(photo_key):
    """View photo given a key."""
    return ViewPhotoHandler().get(photo_key)


@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    """Upload handler called by blobstore when a blob is uploaded in the test."""
    return PhotoUploadHandler().post()


# [END gae_blobstore_handler_flask]


@app.route("/")
def upload():
    """Create the HTML form to upload a file."""
    upload_url = blobstore.create_upload_url("/upload_photo")

    response = """
  <html><body>
  <form action="{}" method="POST" enctype="multipart/form-data">
    Upload File: <input type="file" name="file"><br>
    <input type="submit" name="submit" value="Submit Now">
  </form>
  </body></html>""".format(
        upload_url
    )

    return response
