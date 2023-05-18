#!/usr/bin/env python

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

"""This Apache Beam pipeline processes Landsat 8 satellite images and renders
them as JPEG files.

A Landsat 8 image consists of 11 bands. Each band contains the data for a
specific range of the electromagnetic spectrum.

A JPEG image consists of three channels: Red, Green, and Blue. For Landsat 8
images, these correspond to Band 4 (red), Band 3 (green), and Band 2 (blue).

These bands contain the raw pixel data directly from the satellite sensors. The
values in each band can go from 0 to unbounded positive values. For a JPEG image
we need to clamp them into integers between 0 and 255 for each channel.

For this, we supply visualization parameters, commonly called `vis_params`.
These visualization parameters include:

- The bands for the RGB cannels, typically [B4, B3, B2] for Landsat 8.
- The minimum value in each band, typically 0 for Landsat 8.
- The maximum value in each band, this varies depending on the light exposure.
- A gamma value for gamma correction.

The Landsat data is read from the Landsat public dataset in Cloud Storage.
For more information on the Landsat dataset:
    https://cloud.google.com/storage/docs/public-datasets/landsat

The overall workflow of the pipeline is the following:

- Parse one or more Landsat scene IDs from user-provided flags..
- Get the Cloud Storage paths of all the RGB bands.
- Load the pixel values for each band from Cloud Storage.
- Preprocess pixels: clamp values and apply gamma correction.
- Create a JPEG image and save it to Cloud Storage.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
from typing import Any

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import numpy as np
from PIL import Image
import rasterio
import tensorflow as tf

DEFAULT_RGB_BAND_NAMES = ["B4", "B3", "B2"]
DEFAULT_MIN_BAND_VALUE = 0.0
DEFAULT_MAX_BAND_VALUE = 12000.0
DEFAULT_GAMMA = 0.5

# For more information on the available GPU types per location,
# see the "GPU availability" section in the documentation.
#   https://cloud.google.com/dataflow/docs/resources/locations#gpu_availability
DEFAULT_GPU_TYPE = "nvidia-tesla-t4"
DEFAULT_GPU_COUNT = 1

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


def check_gpus(_: None, gpus_optional: bool = False) -> None:
    """Validates that we are detecting GPUs, otherwise raise a RuntimeError."""
    gpu_devices = tf.config.list_physical_devices("GPU")
    if gpu_devices:
        logging.info(f"Using GPU: {gpu_devices}")
    elif gpus_optional:
        logging.warning("No GPUs found, defaulting to CPU.")
    else:
        raise RuntimeError("No GPUs found.")


def get_band_paths(scene: str, band_names: list[str]) -> tuple[str, list[str]]:
    """Gets the Cloud Storage paths for each band in a Landsat scene.

    Args:
        scene: Landsat 8 scene ID.
        band_names: list of the band names corresponding to [Red, Green, Blue] channels.

    Returns:
        A (scene, band_paths) pair.

    Raises:
        ValueError: If the scene or a band does not exist.
    """
    # Extract the metadata from the scene ID using a regular expression.
    m = SCENE_RE.match(scene)
    if not m:
        raise ValueError(f"invalid scene ID: {scene}")

    g = m.groupdict()
    scene_dir = f"gs://gcp-public-data-landsat/{g['sensor']}/{g['collection']}/{g['wrs_path']}/{g['wrs_row']}/{scene}"

    band_paths = [f"{scene_dir}/{scene}_{band_name}.TIF" for band_name in band_names]

    for band_path in band_paths:
        if not tf.io.gfile.exists(band_path):
            raise ValueError(f"failed to load: {band_path}")

    return scene, band_paths


def save_to_gcs(
    scene: str, pixels: np.ndarray, output_path_prefix: str, format: str = "JPEG"
) -> None:
    """Saves a PIL.Image as a JPEG file in the desired path.

    Args:
        scene: Landsat 8 scene ID.
        image: A PIL.Image object.
        output_path_prefix: Path prefix to save the output files.
        format: Image format to save files.
    """
    filename = os.path.join(output_path_prefix, scene + "." + format.lower())
    with tf.io.gfile.GFile(filename, "w") as f:
        Image.fromarray(pixels, mode="RGB").save(f, format)


def load_as_rgb(
    scene: str,
    band_paths: list[str],
    min_value: float = DEFAULT_MIN_BAND_VALUE,
    max_value: float = DEFAULT_MAX_BAND_VALUE,
    gamma: float = DEFAULT_GAMMA,
) -> tuple[str, np.ndarray]:
    """Loads a scene's bands data and converts it into a pixel-ready format
    for an RGB image.

    The input band values come in the shape (band, width, height) with
    unbounded positive numbers depending on the sensor's exposure.
    The values are reshaped into (width, height, band), the values are clamped
    to integers between 0 and 255, and a gamma correction value is applied.

    Args:
        scene: Landsat 8 scene ID.
        band_paths: A list of the [Red, Green, Blue] band paths.
        min_value: Minimum band value.
        max_value: Maximum band value.
        gamma: Gamma correction value.

    Returns:
        A (scene, pixels) pair.

        The pixel values are stored in a three-dimensional uint8 array with shape:
            (width, height, rgb_channels)
    """

    def read_band(band_path: str) -> np.ndarray:
        # Use rasterio to read the GeoTIFF values from the band files.
        with tf.io.gfile.GFile(band_path, "rb") as f, rasterio.open(f) as data:
            return data.read(1).astype(np.float32)

    logging.info(
        f"{scene}: load_as_image({band_paths}, min={min_value}, max={max_value}, gamma={gamma})"
    )

    # Read the GeoTIFF files.
    band_values = [read_band(band_path) for band_path in band_paths]

    # We get the band values into the shape (width, height, band).
    pixels = np.stack(band_values, axis=-1)

    # Rescale to values from 0.0 to 1.0 and clamp them into that range.
    pixels -= min_value
    pixels /= max_value
    pixels = tf.clip_by_value(pixels, 0.0, 1.0)

    # Apply gamma correction.
    pixels **= 1.0 / gamma

    # Return the pixel values as uint8 in the range from 0 to 255,
    # which is what PIL.Image expects.
    return scene, tf.cast(pixels * 255.0, dtype=tf.uint8).numpy()


def run(
    scenes: list[str],
    output_path_prefix: str,
    vis_params: dict[str, Any],
    gpu_type: str = DEFAULT_GPU_TYPE,
    gpu_count: int = DEFAULT_GPU_COUNT,
    beam_args: list[str] | None = None,
) -> None:
    """Load multiple Landsat scenes and render them as JPEG files.

    Args:
        scenes: list of Landsat 8 scene IDs.
        output_path_prefix: Path prefix to save the output files.
        vis_params: Visualization parameters including {rgb_bands, min, max, gamma}.
        beam_args: Optional list of arguments for Beam pipeline options.
    """
    rgb_band_names = vis_params.get("rgb_band_names", DEFAULT_RGB_BAND_NAMES)
    min_value = vis_params.get("min", DEFAULT_MIN_BAND_VALUE)
    max_value = vis_params.get("max", DEFAULT_MAX_BAND_VALUE)
    gamma = vis_params.get("gamma", DEFAULT_GAMMA)

    gpu_hint = f"type:{gpu_type};count:{gpu_count};install-nvidia-driver"
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    pipeline = beam.Pipeline(options=beam_options)
    (
        pipeline
        | "Create scene IDs" >> beam.Create(scenes)
        | "Check GPU availability"
        >> beam.Map(
            lambda x, unused_side_input: x,
            unused_side_input=beam.pvalue.AsSingleton(
                pipeline
                | beam.Create([None])
                | beam.Map(check_gpus).with_resource_hints(accelerator=gpu_hint)
            ),
        )
        | "Get RGB band paths" >> beam.Map(get_band_paths, rgb_band_names)
        # We reshuffle to prevent fusion and allow all I/O operations to happen in parallel.
        # For more information, see the "Preventing fusion" section in the documentation:
        #   https://cloud.google.com/dataflow/docs/guides/deploying-a-pipeline#preventing-fusion
        | "Reshuffle" >> beam.Reshuffle()
        | "Load bands as RGB"
        >> beam.MapTuple(load_as_rgb, min_value, max_value, gamma).with_resource_hints(
            accelerator=gpu_hint
        )
        | "Save to Cloud Storage" >> beam.MapTuple(save_to_gcs, output_path_prefix)
    )
    pipeline.run()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

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
    parser.add_argument("--gpu-type", default=DEFAULT_GPU_TYPE, help="GPU type to use.")
    parser.add_argument(
        "--gpu-count", type=int, default=DEFAULT_GPU_COUNT, help="GPU count to use."
    )
    parser.add_argument(
        "--rgb-band-names",
        nargs=3,
        default=DEFAULT_RGB_BAND_NAMES,
        help="List of three band names to be mapped to the RGB channels.",
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

    run(
        scenes=args.scenes or DEFAULT_SCENES,
        output_path_prefix=args.output_path_prefix,
        vis_params={
            "rgb_band_names": args.rgb_band_names,
            "min": args.min,
            "max": args.max,
            "gamma": args.gamma,
        },
        gpu_type=args.gpu_type,
        gpu_count=args.gpu_count,
        beam_args=beam_args,
    )
