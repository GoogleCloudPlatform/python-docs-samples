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

from typing import Dict, Iterable, List, Optional, Tuple, TypeVar

from apache_beam.options.pipeline_options import PipelineOptions
import ee
import numpy as np

a = TypeVar("a")

SENTINEL2_BANDS = [
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

# Define the input and output names for the model.
INPUT_NAMES = SENTINEL2_BANDS
OUTPUT_NAMES = ["landcover"]


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


def ee_auth() -> None:
    import google.auth

    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(credentials, project=project)


def sentinel2_image(start_date: str, end_date: str) -> ee.Image:
    # https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
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
        .select(SENTINEL2_BANDS)
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
    patch_size: int,
    scale: int,
    bands: Optional[List[str]] = None,
) -> np.ndarray:
    import io
    import requests
    from requests.adapters import HTTPAdapter, Retry

    # Prepare to download the patch of pixels as a numpy array.
    point = ee.Geometry.Point([lon, lat])
    url = image.getDownloadURL(
        {
            "region": point.buffer(scale * patch_size / 2, 1).bounds(1),
            "dimensions": [patch_size, patch_size],
            "format": "NPY",
            "bands": bands or image.bandNames().getInfo(),
        }
    )

    # Add a retry strategy to the HTTP requests.
    retry_strategy = Retry(
        total=MAX_RETRIES,
        status_forcelist=[429],
        backoff_factor=EXPONENTIAL_BACKOFF_IN_SECONDS,
    )
    http = requests.Session()
    http.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    # Fetch the data from Earth Engine and return it as a numpy array.
    np_bytes = http.get(url).content
    return np.load(io.BytesIO(np_bytes), allow_pickle=True)


def get_training_patch(lat: float, lon: float, patch_size: int = 16) -> np.ndarray:
    ee_auth()
    inputs = sentinel2_image("2020-1-1", "2021-1-1")
    outputs = landcover_image()
    image = inputs.addBands(outputs)
    return get_patch(image, lat, lon, patch_size, scale=10)


def get_prediction_patch(lat: float, lon: float, patch_size: int = 256) -> np.ndarray:
    ee_auth()
    image = sentinel2_image("2020-1-1", "2021-1-1")
    return get_patch(image, lat, lon, patch_size, scale=10)


def sample_random_points(
    region: Dict[str, float], points_per_region: int = 100
) -> Iterable[Tuple[float, float]]:
    import random

    for _ in range(points_per_region):
        lat = random.uniform(region["south"], region["north"])
        lon = random.uniform(region["west"], region["east"])
        yield (lat, lon)


def serialize(patch: np.ndarray, names: List[str]) -> bytes:
    import tensorflow as tf

    features = {
        name: tf.train.Feature(
            float_list=tf.train.FloatList(value=patch[name].flatten())
        )
        for name in names
    }
    example = tf.train.Example(features=tf.train.Features(feature=features))
    return example.SerializeToString()


def run(
    training_file: str,
    validation_file: str,
    regions_file: str = "data/regions.csv",
    points_per_region: int = 500,
    patch_size: int = 64,
    validation_ratio: float = 0.1,
    beam_options: Optional[PipelineOptions] = None,
) -> None:
    import apache_beam as beam
    import csv

    def split_dataset(element: a, num_partitions: int) -> int:
        import random

        weights = [1 - validation_ratio, validation_ratio]
        return random.choices([0, 1], weights)[0]

    with open(regions_file) as f:
        csv_reader = csv.DictReader(f)
        regions = [
            {key: float(value) for key, value in row.items()} for row in csv_reader
        ]

    with beam.Pipeline(options=beam_options) as pipeline:
        training_data, validation_data = (
            pipeline
            | "Create regions" >> beam.Create(regions)
            | "Sample random points"
            >> beam.FlatMap(sample_random_points, points_per_region)
            | "Reshuffle" >> beam.Reshuffle()
            | "Get patch" >> beam.MapTuple(get_training_patch, patch_size)
            | "Serialize" >> beam.Map(serialize, INPUT_NAMES + OUTPUT_NAMES)
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
    commands = parser.add_subparsers(dest="command", required=True)

    create_datasets = commands.add_parser("create-datasets")
    create_datasets.add_argument("--training-file", required=True)
    create_datasets.add_argument("--validation-file", required=True)
    create_datasets.add_argument("--regions-file", default="data/regions.csv")
    create_datasets.add_argument("--points-per-region", default=10, type=int)
    create_datasets.add_argument("--patch-size", default=16, type=int)
    create_datasets.add_argument("--validation-ratio", default=0.1, type=float)

    batch_predict = commands.add_parser("batch-predict")

    args, beam_args = parser.parse_known_args()

    print(args)
    if args.command == "create-datasets":
        run(
            training_file=args.training_file,
            validation_file=args.validation_file,
            regions_file=args.regions_file,
            points_per_region=args.points_per_region,
            patch_size=args.patch_size,
            validation_ratio=args.validation_ratio,
            beam_options=PipelineOptions(beam_args, save_main_session=True),
        )
    else:
        raise ValueError(f"unrecognized command: {args.command}")
