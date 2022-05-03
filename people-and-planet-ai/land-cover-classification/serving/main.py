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

import io
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
def predict(lat: float, lon: float, year: int) -> List:
    patch_size = flask.request.args.get("patch-size", 256, type=int)
    model_path = flask.request.args.get("model-path", DEFAULT_MODEL_PATH)

    try:
        ee_init()

        patch = get_patch(
            image=sentinel2_image(f"{year}-01-01", f"{year}-12-31"),
            lat=lat,
            lon=lon,
            bands=INPUT_BANDS,
            patch_size=patch_size,
            scale=10,
        )

        model = tf.keras.models.load_model(model_path)
        model_inputs = np.stack([patch[name] for name in INPUT_BANDS], axis=-1)
        probabilities = model.predict(np.stack([model_inputs]))[0]
        outputs = np.argmax(probabilities, axis=-1).astype(np.uint8)

        with io.BytesIO() as f:
            np.savez_compressed(f, inputs=patch, outputs=outputs)
            return f.getvalue()
    except Exception as e:
        return (f"{type(e).__name__}: {e}", 500)


def ee_init() -> None:
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(credentials, project=project)


def sentinel2_image(start_date: str, end_date: str) -> ee.Image:
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
    point = ee.Geometry.Point([lon, lat])
    region = point.buffer(scale * patch_size / 2, 1).bounds(1)
    url = image.getDownloadURL(
        {
            "region": region,
            "dimensions": [patch_size, patch_size],
            "format": "NPY",
            "bands": bands or image.bandNames().getInfo(),
        }
    )

    response = requests.get(url)
    if response.status_code == 429:
        raise exceptions.TooManyRequests(response.text)

    print(f"Got patch for {(lat, lon)}")
    return np.load(io.BytesIO(response.content), allow_pickle=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
