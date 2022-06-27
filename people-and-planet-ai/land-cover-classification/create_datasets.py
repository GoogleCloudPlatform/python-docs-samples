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

"""This creates training and validation datasets for the model.

As inputs it takes a Sentinel-2 image consisting of 13 bands.
Each band contains data for a specific range of the electromagnetic spectrum.
    https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2

As outputs it returns the probabilities of each classification for every pixel.
The land cover labels for the training dataset come from the ESA WorldCover.
    https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100
"""

import csv
import io
import random
from typing import Dict, Iterable, List, Optional, Tuple

import apache_beam as beam
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


def landcover_image() -> ee.Image:
    """Get the European Space Agency WorldCover image.

    This remaps the ESA classifications with the Dynamic World classifications.

    For more information, see:
        https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100

    Returns: An Earth Engine image with land cover classification as indices.
    """

    # Remap the ESA classifications into the Dynamic World classifications
    fromValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    toValues = [1, 5, 2, 4, 6, 7, 8, 0, 3, 3, 7]
    return (
        ee.ImageCollection("ESA/WorldCover/v100")
        .first()
        .select("Map")
        .remap(fromValues, toValues)
        .rename("landcover")
    )


def sample_random_points(
    region: Dict[str, str], points_per_region: int = 10
) -> Iterable[Tuple[float, float]]:
    """Yields random coordinate points bounded by a region.

    The region dictionary must include: "west", "south", "east", and "north".

    Args:
        region: Rectangle bounds from where to sample.
        points_per_region: Number of points to yield from the region.

    Returns: An iterator of (lat, lon) pairs.
    """
    for _ in range(points_per_region):
        lat = random.uniform(float(region["south"]), float(region["north"]))
        lon = random.uniform(float(region["west"]), float(region["east"]))
        yield (lat, lon)


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


def get_training_patch(
    lat: float, lon: float, bands: List[str] = [], patch_size: int = 16
) -> np.ndarray:
    """Fetches a training data patch including both inputs and outputs.

    Args:
        lat: Latitude of the point of interest.
        lon: Longitude of the point of interest.
        bands: List of bands to extract from the Earth Engine image.
        patch_size: Size in pixels of the surrounding square patch to use.

    Returns: The patch of interest as a NumPy array.
    """

    ee_init()
    image = sentinel2_image("2020-1-1", "2021-1-1").addBands(landcover_image())
    return get_patch(image, lat, lon, bands, patch_size, scale=10)


def serialize(patch: np.ndarray) -> bytes:
    """Serializes a NumPy structured array as a TFRecord example.

    This uses all the columns from the structured array.

    For more information on NumPy structured arrays, see:
        https://numpy.org/doc/stable/user/basics.rec.html

    Args:
        patch: A NumPy structured array.

    Returns: Bytes representing a serialized `tf.train.Example`.
    """
    import tensorflow as tf

    features = {
        name: tf.train.Feature(
            float_list=tf.train.FloatList(value=patch[name].flatten())
        )
        for name in patch.dtype.names
    }
    example = tf.train.Example(features=tf.train.Features(feature=features))
    return example.SerializeToString()


def run(
    bounds_file: str = "data/training-bounds.csv",
    training_prefix: str = "datasets/training",
    validation_prefix: str = "datasets/validation",
    points_per_region: int = 5,
    patch_size: int = 16,
    validation_ratio: float = 0.1,
    beam_args: Optional[List[str]] = None,
) -> None:
    """Runs an Apache Beam pipeline to create the model datasets.

    Args:
        bounds_file: CSV file with the region bounds of interest.
        training_prefix: Path prefix to save training data to.
        validation_prefix: Path prefix to save validation data to.
        points_per_region: Number of points to extract for each region.
        patch_size: Size in pixels of the surrounding square patch to use.
        validation_ratio: Ratio of data to use for the validation dataset.
    """
    import trainer

    def split_dataset(element: bytes, num_partitions: int) -> int:
        weights = [1 - validation_ratio, validation_ratio]
        return random.choices([0, 1], weights)[0]

    with open(bounds_file) as f:
        regions = [dict(row) for row in csv.DictReader(f)]

    bands = trainer.INPUT_BANDS + trainer.OUTPUT_BANDS
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    with beam.Pipeline(options=beam_options) as pipeline:
        training_data, validation_data = (
            pipeline
            | "Create regions" >> beam.Create(regions)
            | "Sample random points"
            >> beam.FlatMap(sample_random_points, points_per_region)
            | "Reshuffle" >> beam.Reshuffle()
            | "Get patch" >> beam.MapTuple(get_training_patch, bands, patch_size)
            | "Serialize" >> beam.Map(serialize)
            | "Split dataset" >> beam.Partition(split_dataset, 2)
        )

        training_data | "Write training data" >> beam.io.WriteToTFRecord(
            training_prefix, file_name_suffix=".tfrecord.gz"
        )
        validation_data | "Write validation data" >> beam.io.WriteToTFRecord(
            validation_prefix, file_name_suffix=".tfrecord.gz"
        )


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--bounds-file",
        default="data/training-bounds.csv",
        help="CSV file with the region bounds of interest.",
    )
    parser.add_argument(
        "--training-prefix",
        default="datasets/training",
        help="Local or Cloud Storage path prefix to save training data to.",
    )
    parser.add_argument(
        "--validation-prefix",
        default="datasets/validation",
        help="Local or Cloud Storage path prefix to save validation data to.",
    )
    parser.add_argument(
        "--points-per-region",
        default=5,
        type=int,
        help="Number of points to extract for each region.",
    )
    parser.add_argument(
        "--patch-size",
        default=16,
        type=int,
        help="Size in pixels of the surrounding square patch to use.",
    )
    parser.add_argument(
        "--validation-ratio",
        default=0.1,
        type=float,
        help="Ratio of data (between 0 and 1) to use for the validation dataset.",
    )
    args, beam_args = parser.parse_known_args()

    run(**vars(args), beam_args=beam_args)
