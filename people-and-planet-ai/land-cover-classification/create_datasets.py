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
import random
from typing import Dict, Iterable, List, Optional, Tuple

import apache_beam as beam
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
        opt_url="https://earthengine-highvolume.googleapis.com",
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


def landcover_image() -> ee.Image:
    # Remap the ESA classifications into the Dynamic World classifications
    # https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100
    fromValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    toValues = [1, 5, 2, 4, 6, 7, 8, 0, 3, 3, 7]
    return (
        ee.ImageCollection("ESA/WorldCover/v100")
        .first()
        .select("Map")
        .remap(fromValues, toValues)
        .rename("landcover")
    )


def get_patch(
    image: ee.Image,
    lat: float,
    lon: float,
    bands: List[str],
    patch_size: int,
    scale: int,
    max_retries: int = 10,
    retry_exp_backoff: float = 0.5,
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

    return np.load(io.BytesIO(response.content), allow_pickle=True)


def get_training_patch(
    lat: float, lon: float, bands: List[str] = [], patch_size: int = 64
) -> np.ndarray:
    ee_init()
    image = sentinel2_image("2020-1-1", "2021-1-1").addBands(landcover_image())
    return get_patch(image, lat, lon, bands, patch_size, scale=10)


def sample_random_points(
    region: Dict[str, float], points_per_region: int = 10
) -> Iterable[Tuple[float, float]]:
    for _ in range(points_per_region):
        lat = random.uniform(region["south"], region["north"])
        lon = random.uniform(region["west"], region["east"])
        yield (lat, lon)


def serialize(patch: np.ndarray) -> bytes:
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
    training_file: str,
    validation_file: str,
    regions_file: str = "data/training-regions.csv",
    points_per_region: int = 500,
    patch_size: int = 64,
    validation_ratio: float = 0.1,
    beam_args: Optional[List[str]] = None,
) -> None:
    import train_model

    def split_dataset(element: bytes, num_partitions: int) -> int:
        weights = [1 - validation_ratio, validation_ratio]
        return random.choices([0, 1], weights)[0]

    with open(regions_file) as f:
        csv_reader = csv.DictReader(f)
        regions = [
            {key: float(value) for key, value in row.items()} for row in csv_reader
        ]

    bands = train_model.INPUT_BANDS + train_model.OUTPUT_BANDS
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

        training_data | "Write training data" >> beam.io.tfrecordio.WriteToTFRecord(
            training_file, file_name_suffix=".tfrecord.gz"
        )
        validation_data | "Write validation data" >> beam.io.tfrecordio.WriteToTFRecord(
            validation_file, file_name_suffix=".tfrecord.gz"
        )


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--training-file", required=True)
    parser.add_argument("--validation-file", required=True)
    parser.add_argument("--regions-file", default="data/training-regions.csv")
    parser.add_argument("--points-per-region", default=10, type=int)
    parser.add_argument("--patch-size", default=16, type=int)
    parser.add_argument("--validation-ratio", default=0.1, type=float)
    args, beam_args = parser.parse_known_args()

    run(
        training_file=args.training_file,
        validation_file=args.validation_file,
        regions_file=args.regions_file,
        points_per_region=args.points_per_region,
        patch_size=args.patch_size,
        validation_ratio=args.validation_ratio,
        beam_args=beam_args,
    )
