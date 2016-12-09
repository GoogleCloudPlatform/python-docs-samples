"""A sample app that operates on GCS files with blobstore API."""

from __future__ import with_statement

import cloudstorage as gcs

from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2


def CreateFile(filename):
    """Create a GCS file with GCS client lib.

    Args:
        filename: GCS filename.

    Returns:
        The corresponding string blobkey for this GCS file.

    """
    # Create a GCS file with GCS client.
    with gcs.open(filename, 'w') as f:
        f.write('abcde\n')

    # Blobstore API requires extra /gs to distinguish against blobstore files.
    blobstore_filename = '/gs' + filename
    # This blob_key works with blobstore APIs that do not expect a
    # corresponding BlobInfo in datastore.
    return blobstore.create_gs_key(blobstore_filename)


class GCSHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        default_gcs_bucket_name = app_identity.get_default_gcs_bucket_name()
        gcs_filename = '/' + default_gcs_bucket_name + '/blobstore_demo'
        blob_key = CreateFile(gcs_filename)

        # Fetch data.
        self.response.write('Fetched data %s\n' %
                            blobstore.fetch_data(blob_key, 0, 2))

        # Delete files.
        blobstore.delete(blob_key)


class GCSServingHandler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self):
        default_gcs_bucket = app_identity.get_default_gcs_bucket_name()
        gcs_filename = '/' + default_gcs_bucket + '/blobstore_serving_demo'
        blob_key = CreateFile(gcs_filename)
        self.send_blob(blob_key)


app = webapp2.WSGIApplication([('/blobstore/ops', GCSHandler),
                               ('/blobstore/serve', GCSServingHandler)],
                              debug=True)
