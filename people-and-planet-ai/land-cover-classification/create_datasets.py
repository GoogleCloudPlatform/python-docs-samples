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
import tensorflow as tf
import requests
from requests.adapters import HTTPAdapter, Retry


# https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
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

# https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100
OUTPUT_BANDS = ["landcover"]

# There is an Earth Engine quota that if exceeded will
# return us "status code 429: Too Many Requests"
# If we get that status code, we can safely retry the request.
# We use exponential backoff as a retry strategy:
#   https://en.wikipedia.org/wiki/Exponential_backoff
# For more information on Earth Engine request quotas, see
#   https://developers.google.com/earth-engine/guides/usage
MAX_RETRIES = 10
RETRY_STATUS = [429]
EXPONENTIAL_BACKOFF_IN_SECONDS = 0.5


# https://beam.apache.org/documentation/transforms/python/elementwise/pardo/
class GetPatchFromEarthEngine(beam.DoFn):
    def __init__(self, bands: List[str], patch_size: int, scale: int) -> None:
        self.bands = bands
        self.patch_size = patch_size
        self.scale = scale
        self.http: Optional[requests.Session] = None

    def setup(self) -> None:
        # Add a retry strategy for our HTTP requests for Earth Engine.
        retry_strategy = Retry(
            total=MAX_RETRIES,
            status_forcelist=[429],
            backoff_factor=EXPONENTIAL_BACKOFF_IN_SECONDS,
        )
        self.http = requests.Session()
        self.http.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    def process(self, coords: Dict[str, float]) -> Iterable[np.ndarray]:
        credentials, project = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/earthengine",
            ]
        )
        ee.Initialize(credentials, project=project)

        sentinel2_image = get_sentinel2_image("2020-1-1", "2021-1-1")
        landcover_image = get_landcover_image()
        image = sentinel2_image.addBands(landcover_image)

        point = ee.Geometry.Point([coords["lon"], coords["lat"]])
        url = image.getDownloadURL(
            {
                "region": point.buffer(self.scale * self.patch_size / 2, 1).bounds(1),
                "dimensions": [self.patch_size, self.patch_size],
                "format": "NPY",
                "bands": self.bands,
            }
        )
        np_bytes = self.http.get(url).content
        yield np.load(io.BytesIO(np_bytes), allow_pickle=True)

    def teardown(self):
        return self.http.close()


def get_sentinel2_image(start_date: str, end_date: str) -> ee.Image:
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


def get_landcover_image() -> ee.Image:
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
    region: Dict[str, float], points_per_region: int = 100
) -> Iterable[Dict[str, float]]:
    for _ in range(points_per_region):
        yield {
            "lat": random.uniform(region["south"], region["north"]),
            "lon": random.uniform(region["west"], region["east"]),
        }


def serialize(patch: np.ndarray) -> bytes:
    features = {
        name: tf.train.Feature(
            float_list=tf.train.FloatList(value=patch[name].flatten())
        )
        for name in INPUT_BANDS + OUTPUT_BANDS
    }
    example = tf.train.Example(features=tf.train.Features(feature=features))
    return example.SerializeToString()


def run(
    training_file: str,
    validation_file: str,
    regions_file: str = "data/regions.csv",
    points_per_region: int = 500,
    patch_size: int = 64,
    training_validation_ratio: Tuple[int, int] = (90, 10),
    beam_options: Optional[PipelineOptions] = None,
) -> None:
    def split_dataset(element: bytes, num_partitions: int) -> int:
        return random.choices([0, 1], weights=training_validation_ratio)[0]

    with open(regions_file) as f:
        csv_reader = csv.DictReader(f)
        regions = [
            {key: float(value) for key, value in row.items()} for row in csv_reader
        ]

    pipeline = beam.Pipeline(options=beam_options)
    training_data, validation_data = (
        pipeline
        | "Create regions" >> beam.Create(regions)
        | "Sample random points"
        >> beam.FlatMap(sample_random_points, points_per_region)
        | "Get patch"
        >> beam.ParDo(
            GetPatchFromEarthEngine(INPUT_BANDS + OUTPUT_BANDS, patch_size, scale=10)
        )
        | "Serialize" >> beam.Map(serialize)
        | "Split dataset" >> beam.Partition(split_dataset, 2)
    )

    training_data | "Write training data" >> beam.io.tfrecordio.WriteToTFRecord(
        training_file, file_name_suffix=".tfrecord.gz"
    )
    validation_data | "Write validation data" >> beam.io.tfrecordio.WriteToTFRecord(
        validation_file, file_name_suffix=".tfrecord.gz"
    )
    pipeline.run()


if __name__ == "__main__":
    import argparse
    import logging
    import os

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--training-file", required=True)
    parser.add_argument("--validation-file", required=True)
    parser.add_argument("--regions-file", default="data/regions.csv")
    parser.add_argument("--points-per-region", default=500, type=int)
    parser.add_argument("--patch-size", default=64, type=int)
    parser.add_argument(
        "--training-validation-ratio", default=(90, 10), type=int, nargs=2
    )
    args, beam_args = parser.parse_known_args()

    job_name = os.environ.get("CREATE_DATASETS_JOB_NAME")
    if job_name:
        beam_args.append(f"--job_name={job_name}")

    run(**vars(args), beam_options=PipelineOptions(beam_args, save_main_session=True))
