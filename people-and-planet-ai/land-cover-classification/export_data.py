import csv
import io
from typing import Any, Iterable, List, Optional, Tuple
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


def get_coordinates(feature: ee.Feature) -> ee.Feature:
    coords = feature.geometry().coordinates()
    return ee.Feature(None, {"lon": coords.get(0), "lat": coords.get(1)})


def get_points(url: str) -> Iterable[ee.Geometry]:
    points_csv = requests.get(url).text
    for coords in csv.DictReader(io.StringIO(points_csv)):
        lon = float(coords["lon"])
        lat = float(coords["lat"])
        yield ee.Geometry.Point([lon, lat])


def get_patch(
    point: ee.Geometry, image: ee.Image, patch_size: int, scale: int = 10
) -> np.ndarray:
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
    points_per_class: int,
    patch_size: int,
    regions_file: str = "data/regions-small.csv",
    training_validation_ratio: Tuple[int, int] = (80, 20),
    beam_args: Optional[List[str]] = None,
) -> None:
    with open(regions_file) as f:
        polygons = [
            ee.Geometry.Rectangle([float(x) for x in row.values()])
            for row in csv.DictReader(f)
        ]
    region = ee.Geometry.MultiPolygon(polygons)

    # The land cover map we have is from year 2020, so that's what we use here.
    sentinel2_image = get_sentinel2_image("2020-1-1", "2021-1-1")
    landcover_image = get_landcover_image()
    image = sentinel2_image.addBands(landcover_image)

    points_url = (
        landcover_image.stratifiedSample(
            points_per_class, "landcover", region, scale=10, geometries=True
        )
        .map(get_coordinates)
        .randomColumn("random")
        .sort("random")
        .getDownloadURL(selectors=["lon", "lat"])
    )

    def split_dataset(element: Any, num_partitions: int) -> int:
        return random.choices([0, 1], weights=training_validation_ratio)[0]

    beam_options = PipelineOptions(beam_args, save_main_session=True)
    with beam.Pipeline(options=beam_options) as pipeline:
        training_examples, validation_examples = (
            pipeline
            | "Create URL" >> beam.Create([points_url])
            | "Get points" >> beam.FlatMap(get_points)
            | "Reshuffle" >> beam.Reshuffle()
            | "Get patch" >> beam.Map(lambda point: get_patch(point, image, patch_size))
            | "Serialize" >> beam.Map(serialize)
            | "Split dataset" >> beam.Partition(split_dataset, 2)
        )

        training_examples | "Write training data" >> beam.io.tfrecordio.WriteToTFRecord(
            training_file, file_name_suffix=".tfrecord.gz"
        )
        validation_examples | "Write validation data" >> beam.io.tfrecordio.WriteToTFRecord(
            validation_file, file_name_suffix=".tfrecord.gz"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--training-file", required=True)
    parser.add_argument("--validation-file", required=True)
    parser.add_argument("--points-per-class", default=10, type=int)
    parser.add_argument("--patch-size", default=8, type=int)
    parser.add_argument("--regions-file", default="data/regions-small.csv")
    parser.add_argument(
        "--training-validation-ratio", default=(90, 10), type=int, nargs=2
    )
    args, beam_args = parser.parse_known_args()

    ee.Initialize()
    run(**vars(args), beam_args=beam_args)
