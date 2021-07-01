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
import logging
import os
import random
import time
from typing import Dict, Iterable, Tuple

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


def read_data(data_file: str) -> pd.DataFrame:
    mmsi = os.path.splitext(os.path.basename(data_file))[0]
    with tf.io.gfile.GFile(data_file, "rb") as f:
        ship_time_steps = (
            pd.DataFrame(np.load(f)["x"])
            .assign(timestamp=lambda df: df["timestamp"].map(datetime.utcfromtimestamp))
            .resample(TIME_STEP_DELTA, on="timestamp")
            .mean()
            .reset_index()
            .interpolate()
            .assign(
                mmsi=lambda df: df["mmsi"].map(lambda _: int(mmsi)),
                timestamp=lambda df: df["timestamp"].map(to_unix_time),
            )
        )
        return ship_time_steps


def read_labels(labels_file: str) -> pd.DataFrame:
    with tf.io.gfile.GFile(labels_file, "r") as f:
        return (
            pd.read_csv(f, parse_dates=["start_time", "end_time"])
            .astype({"mmsi": int})
            .assign(
                start_time=lambda df: df["start_time"].map(to_unix_time),
                end_time=lambda df: df["end_time"].map(to_unix_time),
            )
        )


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


def generate_training_points(data: pd.DataFrame) -> Iterable[Dict[str, np.ndarray]]:
    padding = trainer.PADDING
    midpoints = data[padding:-padding].query("is_fishing == is_fishing").index.tolist()
    for midpoint in midpoints:
        inputs = (
            data.drop(columns=["distance_from_shore", "is_fishing"])
            .loc[midpoint - padding : midpoint + padding]
            .to_dict("list")
        )
        outputs = (
            data[["is_fishing"]].loc[midpoint:midpoint].astype("int8").to_dict("list")
        )
        yield {
            name: np.reshape(values, (len(values), 1))
            for name, values in {**inputs, **outputs}.items()
        }


def run(
    raw_data_dir: str,
    raw_labels_dir: str,
    train_data_dir: str,
    eval_data_dir: str,
    train_eval_split: Tuple[int, int] = [80, 20],
    **pipeline_options,
) -> str:

    labels = pd.concat(
        [
            read_labels(filename)
            for filename in tf.io.gfile.glob(f"{raw_labels_dir}/*.csv")
        ]
    ).sort_values(by="start_time")

    beam_options = PipelineOptions(
        flags=[],
        type_check_additional="all",
        save_main_session=True,
        **pipeline_options,
    )
    pipeline = beam.Pipeline(options=beam_options)

    training_data, evaluation_data = (
        pipeline
        | "Data files" >> beam.Create([f"{raw_data_dir}/*.npz"])
        | "Expand pattern" >> beam.FlatMap(tf.io.gfile.glob)
        | "Reshuffle files" >> beam.Reshuffle()
        | "Read data" >> beam.Map(read_data)
        | "Label data" >> beam.Map(label_data, labels)
        | "Get training points" >> beam.FlatMap(generate_training_points)
        | "Serialize TFRecords" >> beam.Map(trainer.serialize)
        | "Train-eval split"
        >> beam.Partition(lambda x, n: random.choices([0, 1], train_eval_split)[0], 2)
    )

    (
        training_data
        | "Write train files"
        >> beam.io.WriteToTFRecord(
            f"{train_data_dir}/part",
            file_name_suffix=".tfrecords.gz",
            compression_type=beam.io.filesystems.CompressionTypes.GZIP,
        )
    )

    (
        evaluation_data
        | "Write eval files"
        >> beam.io.WriteToTFRecord(
            f"{eval_data_dir}/part",
            file_name_suffix=".tfrecords.gz",
            compression_type=beam.io.filesystems.CompressionTypes.GZIP,
        )
    )

    result = pipeline.run()
    logging.info(result)
    logging.info(result._job)
    return result._job.id
