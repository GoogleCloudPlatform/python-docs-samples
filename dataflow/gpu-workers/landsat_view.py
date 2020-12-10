#!/usr/bin/env python

import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import numpy as np
from PIL import Image
import rasterio as rio
import tensorflow as tf

DEFAULT_RGB_BANDS = ["B4", "B3", "B2"]
DEFAULT_MIN_BAND_VALUE = 0.0
DEFAULT_MAX_BAND_VALUE = 12000.0
DEFAULT_GAMMA = 0.5

DEFAULT_SCENES = [
    "LC08_L1TP_001067_20200727_20200807_01_T1",  # Brazil-Bolivia boundary
    "LC08_L1TP_019024_20190621_20190704_01_T1",  # Nottaway river delta, Quebec
    "LC08_L1TP_019046_20191214_20191226_01_T1",  # Yucatan peninsula
    "LC08_L1TP_037035_20191212_20191212_01_T1",  # Grand canyon, Arizona
    "LC08_L1TP_045031_20200715_20200722_01_T1",  # Mount Shasta, California
    "LC08_L1TP_064011_20200618_20200625_01_T1",  # Mackenzie river delta, Canada
    "LC08_L1TP_073087_20200516_20200527_01_T1",  # Mt. Taranaki, New Zealand
    "LC08_L1TP_083074_20180805_20180814_01_T1",  # Nouvelle-Calédonie
    "LC08_L1TP_098063_20200703_20200708_01_T1",  # Manam volcano, Papua New Guinea
    "LC08_L1TP_109078_20200411_20200422_01_T1",  # Lake Carnegie, West Australia
    "LC08_L1TP_110036_20191009_20191018_01_T1",  # Osaka 大阪市, Japan
    "LC08_L1TP_115078_20200608_20200625_01_T1",  # Sediment deposits, West Australia
    "LC08_L1TP_119038_20191109_20191115_01_T1",  # Lake Tai 太湖, China
    "LC08_L1TP_135040_20190314_20190325_01_T1",  # Arunachal Pradesh, India
    "LC08_L1TP_137045_20200211_20200225_01_T1",  # Ganges river delta, India
    "LC08_L1TP_166075_20180608_20180615_01_T1",  # Bazaruto island, Mozambique
    "LC08_L1TP_169034_20200720_20200807_01_T1",  # Lake Urmia دریاچه ارومیه, Iran
    "LC08_L1TP_170059_20200101_20200113_01_T1",  # Mount Elgon, Uganda
    "LC08_L1TP_175079_20200511_20200526_01_T1",  # Sand dunes, South Africa
    "LC08_L1TP_178069_20200804_20200821_01_T1",  # Angola
    "LC08_L1TP_178078_20200804_20200821_01_T1",  # Sand dunes, Namibia
    "LC08_L1TP_191020_20200815_20200822_01_T1",  # Phytoplankton at Gotland, Sweden
    "LC08_L1TP_195028_20200116_20200127_01_T1",  # Swiss Alps
    "LC08_L1TP_203045_20200108_20200114_01_T1",  # Eye of the Sahara, Mauritania
    "LC08_L1TP_231094_20190906_20190917_01_T1",  # Patagonia, South America
]

SCENE_RE = re.compile(
    r"(?P<sensor>L[COTEM]0[78])_"
    r"(?P<correction_level>L1TP|L1GT|L1GS)_"
    r"(?P<wrs_path>\d\d\d)"
    r"(?P<wrs_row>\d\d\d)_"
    r"(?P<year>\d\d\d\d)"
    r"(?P<month>\d\d)"
    r"(?P<day>\d\d)_"
    r"(?P<processing_year>\d\d\d\d)"
    r"(?P<processing_month>\d\d)"
    r"(?P<processing_day>\d\d)_"
    r"(?P<collection>\d\d)_"
    r"(?P<category>RT|T1|T2)"
)


def get_valid_band_paths(scene: str, bands: List[str]) -> List[str]:
    """Gets the Cloud Storage paths for each band in a Landsat scene."""
    try:
        return [get_band_path(scene, band) for band in bands]
    except Exception as e:
        # If it fails, don't crash the entire pipeline.
        # Instead, log the error and skip this scene.
        logging.error(e, exc_info=True)
        return []


def get_band_path(scene: str, band: str) -> Tuple[str, Tuple[str, str]]:
    """Gets the Cloud Storage path for a single band in a Landsat scene."""
    # Extract the metadata from the scene ID using a regular expression.
    m = SCENE_RE.match(scene)
    if m:
        g = m.groupdict()
        scene_dir = "gs://gcp-public-data-landsat/{}/{}/{}/{}/{}".format(
            g["sensor"], g["collection"], g["wrs_path"], g["wrs_row"], scene
        )

        path = "{}/{}_{}.TIF".format(scene_dir, scene, band)
        if not tf.io.gfile.exists(path):
            raise ValueError(
                'failed to load band "{}", GCS path not found: {}'.format(band, path)
            )

        logging.info("{}: get_band_path({}): {}".format(scene, band, path))
        return scene, (band, path)

    raise ValueError("invalid scene ID: {}".format(scene))


def load_band(
    scene: str, band_path: Tuple[str, str]
) -> Tuple[str, Tuple[str, np.array]]:
    """Loads a band's data as a numpy array."""
    band, path = band_path

    # Use rasterio to read the GeoTIFF values from Cloud Storage.
    with tf.io.gfile.GFile(path, "rb") as f, rio.open(f) as data:
        logging.info("{}: load_band({})".format(scene, band))
        return scene, (band, data.read(1))


def preprocess_pixels(
    scene: str,
    values: np.array,
    min_value: float = 0.0,
    max_value: float = 1.0,
    gamma: float = 1.0,
) -> Tuple[str, tf.Tensor]:
    """Prepares the band data into a pixel-ready format for an RGB image."""
    values = np.array(values, np.float32)
    logging.info(
        "{}: preprocess_pixels({}, min={}, max={}, gamma={})".format(
            scene, values.shape, min_value, max_value, gamma
        )
    )

    # Make sure we have a GPU available.
    gpu_devices = tf.config.list_physical_devices("GPU")
    logging.info("GPU devices: {}".format(gpu_devices))
    if len(gpu_devices) == 0:
        logging.warning("No GPUs found, defaulting to CPU")

    # Reshape (band, width, height) into (width, height, band).
    pixels = tf.transpose(values, (1, 2, 0))

    # Rescale to values from 0.0 to 1.0 and clamp them into that range.
    pixels -= min_value
    pixels /= max_value
    pixels = tf.clip_by_value(pixels, 0.0, 1.0)

    # Apply gamma correction.
    pixels **= 1.0 / gamma

    # Return the pixel values as int8 in the range from 0 to 255,
    # which is what PIL.Image expects.
    return scene, tf.cast(pixels * 255.0, dtype=tf.uint8)


def save_to_gcs(
    scene: str, image: Image.Image, output_path_prefix: str, format: str = "JPEG"
) -> None:
    """Saves a PIL.Image as a JPEG file in the desired path."""
    filename = os.path.join(output_path_prefix, scene + "." + format.lower())
    with tf.io.gfile.GFile(filename, "w") as f:
        image.save(f, format)


def run(
    scenes: List[str],
    output_path_prefix: str,
    vis_params: Dict[str, Any],
    beam_args: Optional[List[str]] = None,
) -> None:
    """Load multiple Landsat scenes and render them as JPEG files."""
    bands = vis_params["bands"]
    min_value = vis_params["min"]
    max_value = vis_params["max"]
    gamma = vis_params["gamma"]

    options = PipelineOptions(beam_args, save_main_session=True)
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "Create scene IDs" >> beam.Create(scenes)
            | "Get band paths" >> beam.FlatMap(get_valid_band_paths, bands)
            | "Load bands" >> beam.MapTuple(load_band)
            | "Group bands per scene" >> beam.GroupByKey()
            | "Combine bands to dict"
            >> beam.MapTuple(lambda scene, bands: (scene, dict(bands)))
            | "Create RGB pixels"
            >> beam.MapTuple(lambda scene, bands: (scene, [bands[b] for b in bands]))
            | "Preprocess pixels"
            >> beam.MapTuple(preprocess_pixels, min_value, max_value, gamma)
            | "Convert to image"
            >> beam.MapTuple(
                lambda scene, rgb_pixels: (
                    scene,
                    Image.fromarray(rgb_pixels.numpy(), mode="RGB"),
                )
            )
            | "Save to Cloud Storage" >> beam.MapTuple(save_to_gcs, output_path_prefix)
        )


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-path-prefix",
        required=True,
        help="Path prefix for output image files. "
        "This can be a Google Cloud Storage path.",
    )
    parser.add_argument(
        "--scene",
        dest="scenes",
        action="append",
        help="One or more Landsat scene IDs to process, for example "
        "LC08_L1TP_109078_20200411_20200422_01_T1. "
        "They must be in the format: "
        "https://www.usgs.gov/faqs/what-naming-convention-landsat-collections-level-1-scenes",
    )
    parser.add_argument(
        "--bands",
        nargs=3,
        default=DEFAULT_RGB_BANDS,
        help="List of three band names to be mapped to RGB",
    )
    parser.add_argument(
        "--min",
        type=float,
        default=DEFAULT_MIN_BAND_VALUE,
        help="Minimum value of the band value range.",
    )
    parser.add_argument(
        "--max",
        type=float,
        default=DEFAULT_MAX_BAND_VALUE,
        help="Maximum value of the band value range.",
    )
    parser.add_argument(
        "--gamma", type=float, default=DEFAULT_GAMMA, help="Gamma correction factor."
    )
    args, beam_args = parser.parse_known_args()

    scenes = args.scenes or DEFAULT_SCENES
    vis_params = {
        "bands": args.bands,
        "min": args.min,
        "max": args.max,
        "gamma": args.gamma,
    }
    run(scenes, args.output_path_prefix, vis_params, beam_args)
