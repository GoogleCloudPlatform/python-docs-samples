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

"""This does model predictions for a batch of images."""

import csv
import io
from typing import Dict, List, Optional

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems
from apache_beam.options.pipeline_options import PipelineOptions
import ee
from google.api_core import exceptions, retry
import google.auth
import numpy as np
import requests


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
        lat: Latitde of the point of interest.
        lon: Longitude of the point of interest.
        bands: List of bands to extract from the Earth Engine image.
        patch_size: Size in pixels of the surrounding square patch to use.
        scale: Number of meters per pixel.
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


def get_prediction_patch(
    region: Dict, bands: List[str] = [], patch_size: int = 256
) -> np.ndarray:
    """Fetches a prediction data patch including only inputs.

    The region dictionary must include: "name", "lat", "lon", and "year".

    Args:
        region: Dictionary with information of the point of interest.
        bands: List of bands to extract from the Earth Engine image.
        patch_size: Size in pixels of the surrounding square patch to use.

    Returns: A tuple of (filename, patch).
    """

    ee_init()
    lat = float(region["lat"])
    lon = float(region["lon"])
    year = int(region["year"])

    filename = f"{region['name']}/{year}"
    image = sentinel2_image(f"{year}-1-1", f"{year + 1}-1-1")
    patch = get_patch(image, lat, lon, bands, patch_size, scale=10)
    return (filename, patch)


def predict(filename: str, patch: np.ndarray, model_path: str = "model") -> Dict:
    """Gets a prediction from the model.

    Args:
        filename: Base file name to save the results to.
        patch: Input patch pixel data as a NumPy array.
        model_path: Local or Cloud Storage path to load the model to use.

    Returns:
        A dictionary containing the results of the prediction:
            filename: Base file name to save the results to.
            inputs: Input patch as a NumPy array.
            outputs: Output patch as a NumPy array.
    """
    import tensorflow as tf

    # Load the model and get the predictions. If the model is hosted
    # somewhere else, this is where we would send a request.
    model = tf.keras.models.load_model(model_path)

    # Create an input dictionary with a batch containing a single patch.
    inputs_batch = {name: np.stack([patch[name]]) for name in patch.dtype.names}

    # Get the first (and only) element in the predictions batch.
    probabilities = model.predict(inputs_batch)[0]

    # Get discrete classification values from the probability distribution.
    outputs = np.argmax(probabilities, axis=-1)

    return {
        "filename": filename,
        "inputs": patch,
        "outputs": outputs,
    }


def write_to_numpy(results: Dict, predictions_prefix: str = "predictions") -> str:
    """Writes the prediction results into a compressed NumPy file.

    The results dictionary must include: "filename", "inputs", and "outputs".

    Args:
        results: The prediction results to write.
        predictions_prefix: Local or Cloud Storage path prefix to write to.
    """
    filename = f"{predictions_prefix}/{results['filename']}.npz"
    with FileSystems.create(filename) as f:
        np.savez_compressed(f, inputs=results["inputs"], outputs=results["outputs"])
    return filename


def run(
    regions_file: str = "data/prediction-locations.csv",
    model_path: str = "model",
    predictions_prefix: str = "predictions",
    patch_size: int = 256,
    beam_args: Optional[List[str]] = None,
) -> None:
    """Runs an Apache Beam pipeline to do batch predictions.

    Args:
        regions_file: CSV file with the locations and years to predict.
        model_path: Local or Cloud Storage path of the trained model to use.
        predictions_prefix: Local or Cloud Storage path prefix to save the results.
        patch_size: Size in pixels of the surrounding square patch to use.
    """

    import trainer

    # Load the points of interest from the CSV file.
    with open(regions_file) as f:
        regions = [dict(row) for row in csv.DictReader(f)]

    # Run the batch prediction pipeline.
    bands = trainer.INPUT_BANDS
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
    parser.add_argument(
        "--regions-file",
        default="data/prediction-locations.csv",
        help="CSV file with the locations and years to predict.",
    )
    parser.add_argument(
        "--model-path",
        default="model",
        help="Local or Cloud Storage path of the trained model to use.",
    )
    parser.add_argument(
        "--predictions-prefix",
        default="predictions",
        help="Local or Cloud Storage path prefix to save the results.",
    )
    parser.add_argument(
        "--patch-size",
        default=256,
        type=int,
        help="Size in pixels of the surrounding square patch to use.",
    )
    args, beam_args = parser.parse_known_args()

    run(**vars(args), beam_args=beam_args)
