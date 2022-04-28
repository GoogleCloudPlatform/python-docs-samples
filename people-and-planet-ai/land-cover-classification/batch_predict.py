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

import csv
import io
from typing import Dict, List, Optional

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems
from apache_beam.options.pipeline_options import PipelineOptions
import ee
import google.auth
import numpy as np
import requests
from requests.adapters import HTTPAdapter, Retry


def ee_init() -> None:
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(
        credentials,
        project=project,
        # opt_url="https://earthengine-highvolume.googleapis.com",
    )


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


def get_patch(
    image: ee.Image,
    lat: float,
    lon: float,
    bands: List[str],
    patch_size: int,
    scale: int,
    max_retries: int = 50,
    retry_exp_backoff: float = 1.0,
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

    # We use exponential backoff as a retry strategy:
    #   https://en.wikipedia.org/wiki/Exponential_backoff
    # For more information on Earth Engine request quotas, see
    #   https://developers.google.com/earth-engine/cloud/highvolume
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429],  # Too many requests error
        backoff_factor=retry_exp_backoff,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    response = session.get(url)
    response.raise_for_status()
    print(f"Got patch for {(lat, lon)}")

    return np.load(io.BytesIO(response.content), allow_pickle=True)


def get_prediction_patch(
    region: Dict, bands: List[str] = [], patch_size: int = 256
) -> np.ndarray:
    ee_init()
    lat = float(region["lat"])
    lon = float(region["lon"])
    year = int(region["year"])
    name = f"{region['name']}/{year}"
    image = sentinel2_image(f"{year}-1-1", f"{year + 1}-1-1")
    patch = get_patch(image, lat, lon, bands, patch_size, scale=10)
    return (name, patch)


def predict(name: str, input_patch: np.ndarray, model_path: str = "model") -> Dict:
    import tensorflow as tf

    model = tf.keras.models.load_model(model_path)
    inputs = np.stack([input_patch[name] for name in input_patch.dtype.names], axis=-1)
    probabilities = model.predict(np.stack([inputs]))[0]
    return {
        "name": name,
        "inputs": input_patch,
        "outputs": probabilities,
    }


def write_to_numpy(results: Dict, predictions_prefix: str = "predictions") -> None:
    filename = f"{predictions_prefix}/{results['name']}.npz"
    with FileSystems.create(filename) as f:
        np.savez_compressed(f, inputs=results["inputs"], outputs=results["outputs"])


def run(
    regions_file: str = "data/prediction-locations.csv",
    model_path: str = "model",
    predictions_prefix: str = "predictions",
    patch_size: int = 256,
    beam_args: Optional[List[str]] = None,
) -> None:
    import train_model

    with open(regions_file) as f:
        regions = [dict(row) for row in csv.DictReader(f)]

    bands = train_model.INPUT_BANDS
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    with beam.Pipeline(options=beam_options) as pipeline:
        (
            pipeline
            | "Create regions" >> beam.Create(regions)
            | "Get patch" >> beam.Map(get_prediction_patch, bands, patch_size)
            | "Predict" >> beam.MapTuple(predict, model_path)
            | "Write to NumPy" >> beam.Map(write_to_numpy, predictions_prefix)
        )


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--regions-file", default="data/prediction-locations.csv")
    parser.add_argument("--model-path", default="model")
    parser.add_argument("--predictions-prefix", default="predictions")
    parser.add_argument("--patch-size", default=256, type=int)
    args, beam_args = parser.parse_known_args()

    run(**vars(args), beam_args=beam_args)
