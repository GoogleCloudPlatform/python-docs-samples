# Copyright 2021 Google LLC
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

from datetime import datetime, timedelta
import os
import random
import time
from typing import Dict, Iterable, List, Optional, Tuple

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import numpy as np
import pandas as pd
import tensorflow as tf

import trainer


# Duration of a time step in the timeseries.
# Training and prediction data must be resampled to this time step delta.
TIME_STEP_DELTA = timedelta(hours=1)


def to_unix_time(timestamp: datetime) -> int:
    return time.mktime(timestamp.timetuple())


def read_data(file_path: str, time_step_delta: timedelta) -> pd.DataFrame:
    mmsi = os.path.splitext(os.path.basename(file_path))[0]
    with tf.io.gfile.GFile(file_path, "rb") as f:
        ship_time_steps = (
            pd.DataFrame(np.load(f)["x"])
            .assign(timestamp=lambda df: df["timestamp"].map(datetime.utcfromtimestamp))
            .resample(time_step_delta, on="timestamp")
            .mean()
            .reset_index()
            .interpolate()
            .assign(
                mmsi=lambda df: df["mmsi"].map(lambda _: int(mmsi)),
                timestamp=lambda df: df["timestamp"].map(to_unix_time),
            )
        )
        return ship_time_steps


def read_labels_file(file_path: str) -> pd.DataFrame:
    with tf.io.gfile.GFile(file_path, "r") as f:
        return (
            pd.read_csv(f, parse_dates=["start_time", "end_time"])
            .astype({"mmsi": int})
            .assign(
                start_time=lambda df: df["start_time"].map(to_unix_time),
                end_time=lambda df: df["end_time"].map(to_unix_time),
            )
        )


def read_labels(file_pattern: str) -> pd.DataFrame:
    return pd.concat(
        [read_labels_file(filename) for filename in tf.io.gfile.glob(file_pattern)]
    ).sort_values("start_time")


def label_data(data: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    data_with_labels = (
        pd.merge_asof(
            left=data,
            right=labels,
            left_on="timestamp",
            right_on="start_time",
            by="mmsi",
        )
        .query("timestamp <= end_time")
        .drop(columns=["start_time", "end_time"])
    )

    labeled_data = data.assign(is_fishing=lambda _: np.nan)
    labeled_data.update(data_with_labels)
    return labeled_data.sort_values(["mmsi", "timestamp"]).drop(
        columns=["mmsi", "timestamp"]
    )


def generate_training_points(
    labeled_data: pd.DataFrame,
    padding: int,
) -> Iterable[Dict[str, np.ndarray]]:
    midpoints = (
        labeled_data[padding:-padding].query("is_fishing == is_fishing").index.tolist()
    )
    for midpoint in midpoints:
        inputs = (
            labeled_data.drop(columns=["distance_from_shore", "is_fishing"])
            .loc[midpoint - padding : midpoint + padding]
            .to_dict("list")
        )
        outputs = (
            labeled_data[["is_fishing"]]
            .loc[midpoint:midpoint]
            .astype("int8")
            .to_dict("list")
        )
        yield {
            name: np.reshape(values, (len(values), 1))
            for name, values in {**inputs, **outputs}.items()
        }


@beam.ptransform_fn
@beam.typehints.with_input_types(beam.pvalue.PBegin)
@beam.typehints.with_output_types(Dict[str, np.ndarray])
def GenerateData(pipeline, input_data_pattern: str, labels: pd.DataFrame):
    return (
        pipeline
        | "Input file pattern" >> beam.Create([input_data_pattern])
        | "Expand pattern" >> beam.FlatMap(tf.io.gfile.glob)
        | "Read data" >> beam.Map(read_data, TIME_STEP_DELTA)
        | "Label data" >> beam.Map(label_data, labels)
        | "Get training points"
        >> beam.FlatMap(generate_training_points, trainer.PADDING)
    )


def run(
    input_data: str,
    input_labels: str,
    output_datasets_path: str,
    train_eval_split: Tuple[int, int] = [80, 20],
    beam_args: Optional[List[str]] = None,
) -> Tuple[str, str]:
    labels = read_labels(input_labels)

    beam_options = PipelineOptions(beam_args, type_check_additional="all")
    with beam.Pipeline(options=beam_options) as pipeline:
        training_data, evaluation_data = (
            pipeline
            | "Generate data" >> GenerateData(input_data, labels)
            | "Serialize TFRecords" >> beam.Map(trainer.serialize)
            | "Train/eval split"
            >> beam.Partition(
                lambda _, n: random.choices([0, 1], train_eval_split)[0], 2
            )
        )

        train_files_prefix = f"{output_datasets_path}/train/data"
        (
            training_data
            | "Write train TFRecords"
            >> beam.io.WriteToTFRecord(
                train_files_prefix,
                file_name_suffix=".tfrecords.gz",
                compression_type=beam.io.filesystems.CompressionTypes.GZIP,
            )
        )

        eval_files_prefix = f"{output_datasets_path}/eval/data"
        (
            evaluation_data
            | "Write eval TFRecords"
            >> beam.io.WriteToTFRecord(
                eval_files_prefix,
                file_name_suffix=".tfrecords.gz",
                compression_type=beam.io.filesystems.CompressionTypes.GZIP,
            )
        )

    return f"{train_files_prefix}*", f"{eval_files_prefix}*"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-data",
        required=True,
        help="File pattern for input data.",
    )
    parser.add_argument(
        "--input-labels",
        required=True,
        help="File pattern for data labels.",
    )
    parser.add_argument(
        "--output-datasets-path",
        required=True,
        help="Output path prefix for training and evaluation dataset files.",
    )
    parser.add_argument(
        "--train-eval-split",
        type=int,
        default=[80, 20],
        nargs=2,
        help="The ratio to split the data into training and evaluation datasets.",
    )
    args, beam_args = parser.parse_known_args()

    train_files, eval_files = run(
        input_data=args.input_data,
        input_labels=args.input_labels,
        output_datasets_path=args.output_datasets_path,
        train_eval_split=args.train_eval_split,
        beam_args=beam_args,
    )

    print(f"train_files: {train_files}")
    print(f"eval_files: {eval_files}")
