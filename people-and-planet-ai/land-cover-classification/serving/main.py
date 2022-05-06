# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This does model predictions for incoming HTTP GET requests."""

import io
import logging
import os
from typing import List

import ee
import flask
from google.api_core import exceptions, retry
import google.auth
import numpy as np
import requests
import tensorflow as tf

app = flask.Flask(__name__)


INPUT_BANDS = [
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B8A",
    "B9",
    "B10",
    "B11",
    "B12",
]

DEFAULT_MODEL_PATH = os.environ["MODEL_PATH"]


@app.route("/predict/<float(signed=True):lat>/<float(signed=True):lon>/<int:year>")
def predict(lat: float, lon: float, year: int) -> flask.Response:
    """Gets a prediction from the model.

    Args:
        lat: Latitude of the point of interest.
        lon: Longitude of the point of interest.
        year: Year of interest, the model takes the median of that year.

    Optional request parameters:
        patch-size: Size in pixels of the surrounding square patch to use.
        model-path: Cloud Storage path to load the model to use.

    Returns:
        The bytes of a compressed numpy file with the results if successful,
        or the error with a 500 status code otherwise.
    """

    # Optional HTTP request parameters.
    #   https://en.wikipedia.org/wiki/Query_string
    patch_size = flask.request.args.get("patch-size", 256, type=int)
    model_path = flask.request.args.get("model-path", DEFAULT_MODEL_PATH)

    # If anything fails, send a more descriptive error message instead of
    # a generic "500: Internal Server Error" message.
    try:
        ee_init()

        # Fetch the input patch.
        patch = get_patch(
            image=sentinel2_image(f"{year}-01-01", f"{year}-12-31"),
            lat=lat,
            lon=lon,
            bands=INPUT_BANDS,
            patch_size=patch_size,
            scale=10,
        )

        # Load the model and get the predictions. If the model is hosted
        # somewhere else, this is where we would send a request.
        model = tf.keras.models.load_model(model_path)

        # Create an input dictionary with a batch containing a single patch.
        inputs_batch = {name: np.stack([patch[name]]) for name in patch.dtype.names}

        # Get the first (and only) element in the predictions batch.
        probabilities = model.predict(inputs_batch)[0]

        # Get discrete classification values from the probability distribution.
        outputs = np.argmax(probabilities, axis=-1)

        # Serialize the results into a compressed NumPy file.
        with io.BytesIO() as f:
            np.savez_compressed(f, inputs=patch, outputs=outputs)
            return f.getvalue()

    except Exception as e:
        # If something didn't go well, log the error with the stack trace
        # and return a more descriptive error message to the client.
        logging.error(e, exc_info=True)
        return (f"{type(e).__name__}: {e}", 500)


def ee_init() -> None:
    """Authenticate and initialize Earth Engine with the default credentials."""
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )

    # Use the Earth Engine High Volume endpoint.
    #   https://developers.google.com/earth-engine/cloud/highvolume
    ee.Initialize(
        credentials,
        project=project,
        opt_url="https://earthengine-highvolume.googleapis.com",
    )


def sentinel2_image(start_date: str, end_date: str) -> ee.Image:
    """Get a Sentinel-2 Earth Engine image.

    This filters clouds and returns the median for the selected time range.

    For more information, see:
        https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2

    Args:
        start_date: Beginning of the time range to consider for the median.
        end_date: End of the time range to consider for the median.

    Returns: An Earth Engine image with the median Sentinel-2 values.
    """

    def mask_sentinel2_clouds(image: ee.Image) -> ee.Image:
        CLOUD_BIT = 10
        CIRRUS_CLOUD_BIT = 11
        bit_mask = (1 << CLOUD_BIT) | (1 << CIRRUS_CLOUD_BIT)
        mask = image.select("QA60").bitwiseAnd(bit_mask).eq(0)
        return image.updateMask(mask)

    return (
        ee.ImageCollection("COPERNICUS/S2")
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_sentinel2_clouds)
        .median()
    )


@retry.Retry()
def get_patch(
    image: ee.Image,
    lat: float,
    lon: float,
    bands: List[str],
    patch_size: int,
    scale: int,
) -> np.ndarray:
    """Fetches a patch of pixels from Earth Engine as a NumPy array.

    Args:
        image: Earth Engine image to fetch from.
        lat: Latitude of the point of interest.
        lon: Longitude of the point of interest.
        bands: List of bands to extract from the Earth Engine image.
        patch_size: Size in pixels of the surrounding square patch to use.
        scale: Number of meters per pixel.

    Returns: The patch of interest as a NumPy array.
    """

    # Create the URL to download the band values of the patch of pixels.
    point = ee.Geometry.Point([lon, lat])
    region = point.buffer(scale * patch_size / 2, 1).bounds(1)
    try:
        url = image.getDownloadURL(
            {
                "region": region,
                "dimensions": [patch_size, patch_size],
                "format": "NPY",
                "bands": bands or image.bandNames().getInfo(),
            }
        )
    except ee.ee_exception.EEException:
        raise exceptions.TooManyRequests("image.getDownloadURL")

    # Download the pixel data. If we get "429: Too Many Requests" errors,
    # it's safe to retry the request.
    response = requests.get(url)
    if response.status_code == 429:
        # The retry.Retry library only works with `google.api_core` exceptions.
        raise exceptions.TooManyRequests(response.text)
    # Still raise any other exceptions to make sure we got valid data.
    response.raise_for_status()

    # Load the NumPy file data and return it as a NumPy array.
    print(f"Got patch for {(lat, lon)}")
    return np.load(io.BytesIO(response.content), allow_pickle=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
