import csv
import io
from typing import Optional, Tuple
import random
import requests

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import ee
import numpy as np
import tensorflow as tf


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
OUTPUT_BANDS = ["landcover"]


def get_landcover_image() -> ee.Image:
    # Remap the ESA classifications into the Dynamic World classifications
    fromValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
    toValues = [1, 5, 2, 4, 6, 7, 8, 0, 3, 3, 7]
    return (
        ee.ImageCollection("ESA/WorldCover/v100")
        .map(
            lambda image: image.select("Map")
            .remap(fromValues, toValues)
            .rename("landcover")
        )
        .first()
    )


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


def get_patch(coords: Tuple[float, float], patch_size: int, scale: int) -> np.ndarray:
    # The land cover map we have is from year 2020, so that's what we use here.
    sentinel2_image = get_sentinel2_image("2020-1-1", "2021-1-1")
    landcover_image = get_landcover_image()
    image = sentinel2_image.addBands(landcover_image)

    point = ee.Geometry.Point(coords)
    url = image.getDownloadUrl(
        {
            "region": point.buffer(scale * patch_size / 2, 1).bounds(1),
            "dimensions": [patch_size, patch_size],
            "format": "NPY",
            "bands": INPUT_BANDS + OUTPUT_BANDS,
        }
    )
    np_bytes = requests.get(url).content
    return np.load(io.BytesIO(np_bytes))


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
    patch_size: int,
    points_file: str = "data/points.csv",
    training_validation_ratio: Tuple[int, int] = (80, 20),
    beam_options: Optional[PipelineOptions] = None,
) -> None:
    with open(points_file) as f:
        points = [(float(row["lon"]), float(row["lat"])) for row in csv.DictReader(f)]

    def split_dataset(element: bytes, num_partitions: int) -> int:
        return random.choices([0, 1], weights=training_validation_ratio)[0]

    pipeline = beam.Pipeline(options=beam_options)
    training_data, validation_data = (
        pipeline
        | "Create points" >> beam.Create(points)
        | "Get patch" >> beam.Map(get_patch, patch_size, scale=10)
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
    import google.auth
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--training-file", required=True)
    parser.add_argument("--validation-file", required=True)
    parser.add_argument("--patch-size", default=8, type=int)
    parser.add_argument("--points-file", default="data/points.csv")
    parser.add_argument(
        "--training-validation-ratio", default=(90, 10), type=int, nargs=2
    )
    args, beam_args = parser.parse_known_args()

    beam_options = PipelineOptions(beam_args, save_main_session=True)
    project = beam_options.get_all_options().get("project")

    try:
        # When running locally, as a one-time set up you need to run:
        # ee.Authenticate()
        ee.Initialize()
    except ee.EEException:
        import google.auth

        # For Colab and service accounts we use the default credentials.
        credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        assert project, "You must pass --project to authenticate to Earth Engine"
        ee.Initialize(credentials, project=project)

    run(
        training_file=args.training_file,
        validation_file=args.validation_file,
        patch_size=args.patch_size,
        points_file=args.points_file,
        training_validation_ratio=args.training_validation_ratio,
        beam_options=beam_options,
    )
