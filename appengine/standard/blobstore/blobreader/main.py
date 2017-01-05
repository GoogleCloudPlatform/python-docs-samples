"""A sample app that operates on GCS files with blobstore API's BlobReader."""

import cloudstorage
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
import webapp2


class BlobreaderHandler(webapp2.RequestHandler):
    def get(self):
        # Get the default Cloud Storage Bucket name and create a file name for
        # the object in Cloud Storage.
        bucket = app_identity.get_default_gcs_bucket_name()

        # Cloud Storage file names are in the format /bucket/object.
        filename = '/{}/blobreader_demo'.format(bucket)

        # Create a file in Google Cloud Storage and write something to it.
        with cloudstorage.open(filename, 'w') as filehandle:
            filehandle.write('abcde\n')

        # In order to read the contents of the file using the Blobstore API,
        # you must create a blob_key from the Cloud Storage file name.
        # Blobstore expects the filename to be in the format of:
        # /gs/bucket/object
        blobstore_filename = '/gs{}'.format(filename)
        blob_key = blobstore.create_gs_key(blobstore_filename)

        # [START blob_reader]
        # Instantiate a BlobReader for a given Blobstore blob_key.
        blob_reader = blobstore.BlobReader(blob_key)

        # Instantiate a BlobReader for a given Blobstore blob_key, setting the
        # buffer size to 1 MB.
        blob_reader = blobstore.BlobReader(blob_key, buffer_size=1048576)

        # Instantiate a BlobReader for a given Blobstore blob_key, setting the
        # initial read position.
        blob_reader = blobstore.BlobReader(blob_key, position=0)

        # Read the entire value into memory. This may take a while depending
        # on the size of the value and the size of the read buffer, and is not
        # recommended for large values.
        blob_reader_data = blob_reader.read()

        # Write the contents to the response.
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(blob_reader_data)

        # Set the read position back to 0, then read and write 3 bytes.
        blob_reader.seek(0)
        blob_reader_data = blob_reader.read(3)
        self.response.write(blob_reader_data)
        self.response.write('\n')

        # Set the read position back to 0, then read and write one line (up to
        # and including a '\n' character) at a time.
        blob_reader.seek(0)
        for line in blob_reader:
            self.response.write(line)
        # [END blob_reader]

        # Delete the file from Google Cloud Storage using the blob_key.
        blobstore.delete(blob_key)


app = webapp2.WSGIApplication([
    ('/', BlobreaderHandler),
    ('/blobreader', BlobreaderHandler)], debug=True)
