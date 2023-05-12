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

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.cloud import logging

# Logging client in Python 3
logging_client = logging.Client()

# This log can be found in the Cloud Logging console under 'Custom Logs'.
logger = logging_client.logger("django-app-logs")


# This datastore model keeps track of which users uploaded which photos.
class UserPhoto(ndb.Model):
    blob_key = ndb.BlobKeyProperty()


# [START gae_blobstore_handler_django]
class PhotoUploadHandler(blobstore.BlobstoreUploadHandler):
    def post(self, environ):
        upload = self.get_uploads(environ)[0]
        photo_key = upload.key()
        user_photo = UserPhoto(blob_key=photo_key)
        user_photo.put()
        logger.log_text("Photo key: %s" % photo_key)
        return redirect("view_photo", key=photo_key)


class ViewPhotoHandler(blobstore.BlobstoreDownloadHandler):
    def get(self, environ, photo_key):
        if not blobstore.get(photo_key):
            return HttpResponse("Photo key not found", status=404)
        else:
            response = HttpResponse(headers=self.send_blob(environ, photo_key))

            # Prevent Django from setting a default content-type.
            # GAE sets it to a guessed type if the header is not set.
            response["Content-Type"] = None
            return response


# [END gae_blobstore_handler_django]


def upload_form(request):
    """Create the HTML form to upload a file."""
    upload_url = blobstore.create_upload_url("/upload_photo")

    response = """
  <html><body>
  <form action="{}" method="POST" enctype="multipart/form-data">
    Upload File: <input type="file" name="file"><br>
    <input type="submit" name="submit" value="Submit">
  </form>
  </body></html>""".format(
        upload_url
    )

    return HttpResponse(response)


def view_photo(request, key):
    """View photo given a key."""
    return ViewPhotoHandler().get(request.environ, key)


def upload_photo(request):
    """Upload handler called by blobstore when a blob is uploaded in the test."""
    return PhotoUploadHandler().post(request.environ)


# [START gae_blobstore_handler_django]
urlpatterns = (
    path("", upload_form, name="upload_form"),
    path("view_photo/<key>", view_photo, name="view_photo"),
    path("upload_photo", upload_photo, name="upload_photo"),
)
# [END gae_blobstore_handler_django]


settings.configure(
    DEBUG=True,
    SECRET_KEY="thisisthesecretkey",
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
    ALLOWED_HOSTS=["*"],
)

app = wrap_wsgi_app(get_wsgi_application())
