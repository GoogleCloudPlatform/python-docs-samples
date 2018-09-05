# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START functions_imagemagick_setup]
import os
import subprocess

from google.cloud import storage, vision


storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
# [END functions_imagemagick_setup]


# [START functions_imagemagick_analyze]
# Blurs uploaded images that are flagged as Adult or Violence.
def blur_offensive_images(data, context):
    file = data

    # Exit if this is a deletion or a deploy event.
    if 'name' not in file:
        print('This is a deploy event.')
        return
    elif file.get('resource_state', None) == 'not_exists':
        print('This is a deletion event.')
        return

    file_name = file['name']
    blob = storage_client.bucket(file['bucket']).get_blob(file_name)
    blob_uri = 'gs://%s/%s' % (file['bucket'], file_name)
    blob_source = {'source': {'image_uri': blob_uri}}

    print('Analyzing %s.' % file_name)

    result = vision_client.safe_search_detection(blob_source)
    detected = result.safe_search_annotation

    if detected.adult == 5 or detected.violence == 5:
        print('The image %s was detected as inappropriate.' % file_name)
        return __blur_image(blob)
    else:
        print('The image %s was detected as OK.' % file_name)
# [END functions_imagemagick_analyze]


# [START functions_imagemagick_blur]
# Blurs the given file using ImageMagick.
def __blur_image(blob):
    print(blob)

    file_name = blob.name
    temp_local_filename = '/tmp/%s' % os.path.basename(file_name)

    # Download file from bucket.
    blob.download_to_filename(temp_local_filename)
    print('Image %s was downloaded to %s.' % (file_name, temp_local_filename))

    # Blur the image using ImageMagick.
    subprocess.check_call([
        'convert', temp_local_filename,
        '-channel', 'RGBA',
        '-blur', '0x24',
        temp_local_filename
    ])
    print('Image %s was blurred.' % file_name)

    # Upload the Blurred image back into the bucket.
    blob.upload_from_filename(temp_local_filename)
    print('Blurred image was uploaded to %s.' % file_name)

    # Delete the temporary file.
    os.remove(temp_local_filename)
# [END functions_imagemagick_blur]
