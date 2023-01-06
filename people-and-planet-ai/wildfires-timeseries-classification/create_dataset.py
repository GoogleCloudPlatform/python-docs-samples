from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, NamedTuple, Tuple
import io
import logging
import random
import requests
import uuid

import ee
from google.api_core import retry, exceptions
import google.auth
import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured

INPUTS = {
    'USGS/SRTMGL1_003': ["elevation"],
    'GRIDMET/DROUGHT': ["psdi"],
    'ECMWF/ERA5/DAILY': [
         'mean_2m_air_temperature',
         'total_precipitation',
         'u_component_of_wind_10m',
         'v_component_of_wind_10m'],
    'IDAHO_EPSCOR/GRIDMET': [
         'pr',
         'sph',
         'th',
         'tmmn',
         'tmmx',
         'vs',
         'erc'],
    'CIESIN/GPWv411/GPW_Population_Density': ['population_density'],
    'MODIS/006/MOD14A1': ['FireMask']
}

LABELS = {
    'MODIS/006/MOD14A1': ['FireMask'],
}

SCALE = 5000
WINDOW = timedelta(days=1)

START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2020, 1, 1)


class Bounds(NamedTuple):
    west: float
    south: float
    east: float
    north: float


class Point(NamedTuple):
    lat: float
    lon: float


class Example(NamedTuple):
    inputs: np.ndarray
    labels: np.ndarray


def ee_init() -> None:
    """Authenticate and initialize Earth Engine with the default credentials."""
    # Use the Earth Engine High Volume endpoint.
    #   https://developers.google.com/earth-engine/cloud/highvolume
    credentials, project = google.auth.default()
    ee.Initialize(
        credentials,
        project=project,
        opt_url="https://earthengine-highvolume.googleapis.com",
    )

@retry.Retry(deadline=60 * 20)  # seconds
def ee_fetch(url: str) -> bytes:
    # If we get "429: Too Many Requests" errors, it's safe to retry the request.
    # The Retry library only works with `google.api_core` exceptions.
    response = requests.get(url)
    if response.status_code == 429:
        raise exceptions.TooManyRequests(response.text)

    # Still raise any other exceptions to make sure we got valid data.
    response.raise_for_status()
    return response.content


def get_image(
    date: datetime, bands_schema: Dict[str, List[str]], window: timedelta
) -> ee.Image:
    ee_init()
    # if elevation dataset is part of bands_schema, deal with it separately
    if 'USGS/SRTMGL1_003' in bands_schema:
      elevation = ee.Image('USGS/SRTMGL1_003').select(bands_schema['USGS/SRTMGL1_003'])
      bands_schema.pop("USGS/SRTMGL1_003")
    else:
      elevation = None

    # if population dataset is part of bands_schema, deal with it separately
    if 'CIESIN/GPWv411/GPW_Population_Density' in bands_schema:
      population = [
          ee.ImageCollection('CIESIN/GPWv411/GPW_Population_Density')
        .filterDate(date.isoformat(), (date + window).isoformat())
        .select(bands_schema['CIESIN/GPWv411/GPW_Population_Density'])
        .median()
      ]
      bands_schema.pop("CIESIN/GPWv411/GPW_Population_Density")
    else:
      population = None

    images = [
        ee.ImageCollection(collection)
        .filterDate(date.isoformat(), (date + window).isoformat())
        .select(bands)
        .mosaic()
        for collection, bands in bands_schema.items()
    ]
    # add elevation to list
    if elevation:
      images.append(elevation)
    # add population to list
    if population:
      images.append(population)
    return ee.Image(images)

def get_input_image(date: datetime) -> ee.Image:
    return get_image(date, INPUTS, WINDOW)


def get_label_image(date: datetime) -> ee.Image:
    return get_image(date, LABELS, WINDOW)


def sample_labels(
    date: datetime, num_points: int, bounds: Bounds
) -> Iterable[Tuple[datetime, Point]]:
    image = get_label_image(date)
    for lat, lon in sample_points(image, num_points, bounds, SCALE):
        yield (date, Point(lat, lon))


def sample_points(
    image: ee.Image, num_points: int, bounds: Bounds, scale: int
) -> np.ndarray:
    def get_coordinates(point: ee.Feature) -> ee.Feature:
        coords = point.geometry().coordinates()
        return ee.Feature(None, {"lat": coords.get(1), "lon": coords.get(0)})

    points = image.int().stratifiedSample(
        num_points,
        region=ee.Geometry.Rectangle(bounds),
        scale=scale,
        geometries=True,
    )
    url = points.map(get_coordinates).getDownloadURL("CSV", ["lat", "lon"])
    return np.genfromtxt(io.BytesIO(ee_fetch(url)), delimiter=",", skip_header=1)


def get_input_sequence(
    date: datetime, point: Point, patch_size: int, num_days: int
) -> np.ndarray:
    dates = [date + timedelta(days=d) for d in range(1 - num_days, 1)]
    images = [get_input_image(d) for d in dates]
    return get_patch_sequence(images, point, patch_size, SCALE)


def get_label_sequence(
    date: datetime, point: Point, patch_size: int, num_days: int
) -> np.ndarray:
    dates = [date + timedelta(days=d) for d in range(1, num_days + 1)]
    images = [get_label_image(d) for d in dates]
    return get_patch_sequence(images, point, patch_size, SCALE)


def get_training_example(
    date: datetime, point: Point, patch_size: int = 64, num_days: int = 2
) -> Example:
    ee_init()
    return Example(
        get_input_sequence(date, point, patch_size, num_days + 1),
        get_label_sequence(date, point, patch_size, num_days),
    )

def try_get_training_example(
    date: datetime, point: Point, patch_size: int = 64, num_hours: int = 2
) -> Iterable[Example]:
    try:
        yield get_training_example(date, point, patch_size, num_hours)
    except Exception as e:
        logging.exception(e)

def get_patch_sequence(
    image_sequence: List[ee.Image], point: Point, patch_size: int, scale: int
) -> np.ndarray:
    def unpack(arr: np.ndarray, i: int) -> np.ndarray:
        names = [x for x in arr.dtype.names if x.startswith(f"{i}_")]
        return np.moveaxis(structured_to_unstructured(arr[names]), -1, 0)

    point = ee.Geometry.Point([point.lon, point.lat])
    image = ee.ImageCollection(image_sequence).toBands()
    url = image.getDownloadURL(
        {
            "region": point.buffer(scale * patch_size / 2, 1).bounds(1),
            "dimensions": [patch_size, patch_size],
            "format": "NPY",
        }
    )
    flat_seq = np.load(io.BytesIO(ee_fetch(url)), allow_pickle=True)
    return np.stack([unpack(flat_seq, i) for i, _ in enumerate(image_sequence)], axis=1)

def write_npz_file(example: Example, file_prefix: str) -> str:
    from apache_beam.io.filesystems import FileSystems

    filename = FileSystems.join(file_prefix, f"{uuid.uuid4()}.npz")
    with FileSystems.create(filename) as f:
        np.savez_compressed(f, inputs=example.inputs, labels=example.labels)
    return filename


def run(
    output_path: str,
    num_dates: int,
    num_points: int,
    bounds: Bounds,
    patch_size: int,
    max_requests: int,
    beam_args: Optional[List[str]] = None,
) -> None:
    import apache_beam as beam
    from apache_beam.options.pipeline_options import PipelineOptions

    random_dates = [
        START_DATE + (END_DATE - START_DATE) * random.random() for _ in range(num_dates)
    ]

    beam_options = PipelineOptions(
        beam_args,
        save_main_session=True,
        requirements_file="requirements.txt",
        max_num_workers=max_requests,
    )
    with beam.Pipeline(options=beam_options) as pipeline:
        (
            pipeline
            | "Random dates" >> beam.Create(random_dates)
            | "Sample labels" >> beam.FlatMap(sample_labels, num_points, bounds)
            | "Reshuffle" >> beam.Reshuffle()
            | "Get example" >> beam.FlatMapTuple(try_get_training_example, patch_size)
            | "Write NPZ files" >> beam.Map(write_npz_file, output_path)
            | "Log files" >> beam.Map(logging.info)
        )

if __name__ == "__main__":
    import argparse

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--num-dates", type=int, default=20)
    parser.add_argument("--num-points", type=int, default=10)
    parser.add_argument("--west", type=float, default=-125.3)
    parser.add_argument("--south", type=float, default=27.4)
    parser.add_argument("--east", type=float, default=-66.5)
    parser.add_argument("--north", type=float, default=49.1)
    parser.add_argument("--patch-size", type=int, default=64)
    parser.add_argument("--max-requests", type=int, default=20)
    args, beam_args = parser.parse_known_args()

    run(
        output_path=args.output_path,
        num_dates=args.num_dates,
        num_points=args.num_points,
        bounds=Bounds(args.west, args.south, args.east, args.north),
        patch_size=args.patch_size,
        max_requests=args.max_requests,
        beam_args=beam_args,
    )