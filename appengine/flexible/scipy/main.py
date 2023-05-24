# Copyright 2016 Google LLC.
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

import logging
import os

from flask import Flask
from flask import request
import imageio
from PIL import Image

app = Flask(__name__)


@app.route("/")
def resize():
    """Demonstrates using Pillow to resize an image.

    This takes a predefined image, resizes it to 300x300 pixesls, and writes it on disk.

    Returns:
        A message stating that the image has been resized.
    """
    app_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(app_path, "assets/google_logo.jpg")
    img = Image.fromarray(imageio.imread(image_path))
    img_tinted = img.resize((300, 300))

    output_image_path = request.args.get("output_image_path")
    # Write the tinted image back to disk
    imageio.imwrite(output_image_path, img_tinted)
    return "Image resized."


@app.errorhandler(500)
def server_error(e):
    """Serves a formatted message on-error.

    Returns:
        The error message and a code 500 status.
    """
    logging.exception("An error occurred during a request.")
    return (
        f"An internal error occurred: <pre>{e}</pre><br>See logs for full stacktrace.",
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
