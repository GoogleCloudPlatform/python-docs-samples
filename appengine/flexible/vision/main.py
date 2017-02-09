# Copyright 2015 Google Inc. All Rights Reserved.
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

# [START app]
from datetime import datetime

from google.cloud import vision
from google.cloud import storage
from google.cloud import datastore

from flask import Flask, request, redirect

CLOUD_STORAGE_BUCKET = 'ryans-bucket-2017'

HEADER_MESSAGE = (
    '<h1>Google Cloud Platform - Face Detection Sample</h1>'
    '<p>This Python Flask application demonstrates App Engine Flexible, Google'
    ' Cloud Storage, and the Cloud Vision API.</p><br>')

app = Flask(__name__)


@app.route('/')
def homepage():

    # Format the header message and a form to submit images.
    html_string = HEADER_MESSAGE
    html_string += """
<html><body>
<form action="upload_photo" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form> """

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get your Cloud Storage bucket.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Loop through all items in your Cloud Storage bucket.
    for blob in bucket.list_blobs():

        # Add HTML to display each image.
        blob_public_url = blob.public_url
        html_string += """<img src="{}" width=200 height=200>""".format(blob_public_url)

        # Use the Cloud Datastore client to fetch the timestamp of when this
        # image was uploaded and the face joy likelihood. Output the photo
        # name, the timestamp, and the joy likelihood to HTML.
        query = datastore_client.query(kind='PhotoTimestamps')
        query.add_filter('blob_name', '=', blob.name)
        image_entities = list(query.fetch())
        if len(image_entities) > 0:
            timestamp = image_entities[0]['timestamp']
            html_string += '<p>{} was uploaded {}.</p>'.format(
                blob.name, timestamp)
            face_joy = image_entities[0]['joy']
            html_string += """<p>Joy Likelihood for Face: {}</p>""".format(face_joy)

    html_string += """</body></html>"""
    return html_string

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    photo = request.files['file']

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(
            photo.read(), content_type=photo.content_type)

    # Make the blob publicly viewable.
    blob.make_public()

    # Create a Cloud Vision client.
    vision_client = vision.Client()

    # Use the Cloud Vision client to detect a face for our image.
    media_link = blob.media_link
    image = vision_client.image(source_uri=media_link)
    faces = image.detect_faces(limit=1)

    # If a face is detected, save to Datastore the likelihood that the face
    # displays 'joy,' as determined by Google's Machine Learning algorithm.
    if len(faces) > 0:
        face = faces[0]

        # Convert the face.emotions.joy enum type to a string, which will be
        # something like 'Likelihood.VERY_LIKELY'. Parse that string by the
        # period to extract only the 'VERY_LIKELY' portion.
        face_joy = str(face.emotions.joy).split('.')[1]
    else:
        face_joy = 'Unknown'

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = 'PhotoTimestamps'
    
    # The name/ID for the new entity.
    name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, timestamp, and joy.
    entity = datastore.Entity(key)
    entity['blob_name'] = blob.name
    entity['timestamp'] = current_datetime
    entity['joy'] = face_joy

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the home page.
    return redirect('/')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
