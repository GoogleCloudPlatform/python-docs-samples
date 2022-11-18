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

"""This does model predictions for different locations at a range of years."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
import csv
from typing import List, NamedTuple, Optional

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems
from apache_beam.ml.inference.base import KeyedModelHandler
from apache_beam.ml.inference.base import ModelHandler
from apache_beam.ml.inference.base import RunInference
from apache_beam.options.pipeline_options import PipelineOptions
import numpy as np

from serving import data

# Default values.
PATCH_SIZE = 512
LOCATIONS_FILE = "predict-locations.csv"
MAX_REQUESTS = 20  # default EE request quota

# Constants.
YEARS = [2016, 2017, 2018, 2019, 2020, 2021]


class Location(NamedTuple):
    name: str
    year: int
    point: tuple[float, float]  # (lon, lat)


def get_inputs(
    location: Location,
    patch_size: int = PATCH_SIZE,
    predictions_path: str = "predictions",
) -> tuple[str, np.ndarray]:
    """Get an inputs patch to predict.

    Args:
        location: A name, year, and (longitude, latitude) point.
        patch_size: Size in pixels of the surrounding square patch.
        predictions_path: Directory path to save prediction results.

    Returns: A (file_path_name, inputs_patch) pair.
    """
    data.ee_init()
    path = FileSystems.join(predictions_path, location.name, str(location.year))
    inputs = data.get_input_patch(location.year, location.point, patch_size)
    return (path, inputs)


def write_numpy(path: str, data: np.ndarray, label: str = "data") -> str:
    """Writes the prediction results into a compressed NumPy file (*.npz).

    Args:
        path: File path prefix to save to.
        data: NumPy array holding the data.
        label: Used as a suffix to the filename, and a key for the NumPy file.

    Returns: The file name where the data was saved to.
    """
    filename = f"{path}-{label}.npz"
    with FileSystems.create(filename) as f:
        np.savez_compressed(f, **{label: data})
    logging.info(filename)
    return filename


def run_tensorflow(
    locations: Iterable[Location],
    model_path: str,
    predictions_path: str,
    patch_size: int = PATCH_SIZE,
    max_requests: int = MAX_REQUESTS,
    beam_args: Optional[List[str]] = None,
) -> None:
    """Runs an Apache Beam pipeline to do batch predictions.

    This fetches data from Earth Engine and does batch prediction on the data.
    We use `max_requests` to limit the number of concurrent requests to Earth Engine
    to avoid quota issues. You can request for an increas of quota if you need it.

    Args:
        locations: A collection of name, point, and year.
        model_path: Directory path to load the trained model from.
        predictions_path: Directory path to save prediction results.
        patch_size: Size in pixels of the surrounding square patch.
        max_requests: Limit the number of concurrent requests to Earth Engine.
        beam_args: Apache Beam command line arguments to parse as pipeline options.
    """
    import tensorflow as tf

    class LandCoverModel(ModelHandler[np.ndarray, np.ndarray, tf.keras.Model]):
        def load_model(self) -> tf.keras.Model:
            return tf.keras.models.load_model(model_path)

        def run_inference(
            self,
            batch: Sequence[np.ndarray],
            model: tf.keras.Model,
            inference_args: Optional[dict] = None,
        ) -> Iterable[np.ndarray]:
            probabilities = model.predict(np.stack(batch))
            predictions = probabilities.argmax(axis=-1).astype(np.uint8)
            return predictions[:, :, :, None]

    model_handler = KeyedModelHandler(LandCoverModel())

    # Run the batch prediction pipeline.
    beam_options = PipelineOptions(
        beam_args,
        save_main_session=True,
        setup_file="./setup.py",
        max_num_workers=max_requests,  # distributed runners
        direct_num_workers=max(max_requests, 20),  # direct runner
        disk_size_gb=50,
    )
    with beam.Pipeline(options=beam_options) as pipeline:
        inputs = (
            pipeline
            | "Locations" >> beam.Create(locations)
            | "Get inputs" >> beam.Map(get_inputs, patch_size, predictions_path)
        )
        predictions = inputs | "RunInference" >> RunInference(model_handler)

        # Write the input and prediction files.
        inputs | "Write inputs" >> beam.MapTuple(write_numpy, "inputs")
        predictions | "Write predictions" >> beam.MapTuple(write_numpy, "predictions")


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("framework", choices=["tensorflow"])
    parser.add_argument(
        "--model-path",
        required=True,
        help="Directory path to load the trained model from.",
    )
    parser.add_argument(
        "--predictions-path",
        required=True,
        help="Directory path to save prediction results.",
    )
    parser.add_argument(
        "--locations-file",
        default=LOCATIONS_FILE,
        help="CSV file with the location names and points to predict.",
    )
    parser.add_argument(
        "--patch-size",
        default=PATCH_SIZE,
        type=int,
        help="Size in pixels of the surrounding square patch.",
    )
    parser.add_argument(
        "--max-requests",
        default=MAX_REQUESTS,
        type=int,
        help="Limit the number of concurrent requests to Earth Engine.",
    )
    args, beam_args = parser.parse_known_args()

    # Load the points of interest from the CSV file.
    with open(args.locations_file) as f:
        locations = [
            Location(row["name"], year, (float(row["lon"]), float(row["lat"])))
            for row in csv.DictReader(f)
            for year in YEARS
        ]

    if args.framework == "tensorflow":
        run_tensorflow(
            locations=locations,
            model_path=args.model_path,
            predictions_path=args.predictions_path,
            patch_size=args.patch_size,
            max_requests=args.max_requests,
            beam_args=beam_args,
        )
    else:
        raise ValueError(f"framework not supported: {args.framework}")
