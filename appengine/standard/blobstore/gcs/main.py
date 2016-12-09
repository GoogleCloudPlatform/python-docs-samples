"""A sample app that operates on GCS files with blobstore API."""

import cloudstorage
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2


# This handler creates a file in Cloud Storage using the cloudstorage
# client library and then reads the data back using the Blobstore API.
class CreateAndReadFileHandler(webapp2.RequestHandler):
    def get(self):
        # Get the default Cloud Storage Bucket name and create a file name for
        # the object in Cloud Storage.
        bucket = app_identity.get_default_gcs_bucket_name()

        # Cloud Storage file names are in the format /bucket/object.
        filename = '/{}/blobstore_demo'.format(bucket)

        # Create a file in Google Cloud Storage and write something to it.
        with cloudstorage.open(filename, 'w') as filehandle:
            filehandle.write('abcde\n')

        # In order to read the contents of the file using the Blobstore API,
        # you must create a blob_key from the Cloud Storage file name.
        # Blobstore expects the filename to be in the format of:
        # /gs/bucket/object
        blobstore_filename = '/gs{}'.format(filename)
        blob_key = blobstore.create_gs_key(blobstore_filename)

        # Read the file's contents using the Blobstore API.
        # The last two parameters specify the start and end index of bytes we
        # want to read.
        data = blobstore.fetch_data(blob_key, 0, 6)

        # Write the contents to the response.
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(data)

        # Delete the file from Google Cloud Storage using the blob_key.
        blobstore.delete(blob_key)


# This handler creates a file in Cloud Storage using the cloudstorage
# client library and then serves the file back using the Blobstore API.
class CreateAndServeFileHandler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self):
        # Get the default Cloud Storage Bucket name and create a file name for
        # the object in Cloud Storage.
        bucket = app_identity.get_default_gcs_bucket_name()

        # Cloud Storage file names are in the format /bucket/object.
        filename = '/{}/blobstore_serving_demo'.format(bucket)

        # Create a file in Google Cloud Storage and write something to it.
        with cloudstorage.open(filename, 'w') as filehandle:
            filehandle.write('abcde\n')

        # In order to read the contents of the file using the Blobstore API,
        # you must create a blob_key from the Cloud Storage file name.
        # Blobstore expects the filename to be in the format of:
        # /gs/bucket/object
        blobstore_filename = '/gs{}'.format(filename)
        blob_key = blobstore.create_gs_key(blobstore_filename)

        # BlobstoreDownloadHandler serves the file from Google Cloud Storage to
        # your computer using blob_key.
        self.send_blob(blob_key)


app = webapp2.WSGIApplication([
    ('/', CreateAndReadFileHandler),
    ('/blobstore/read', CreateAndReadFileHandler),
    ('/blobstore/serve', CreateAndServeFileHandler)], debug=True)
