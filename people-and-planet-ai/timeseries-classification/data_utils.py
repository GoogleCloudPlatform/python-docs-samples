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


from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta
import os
import time

import numpy as np
import pandas as pd
import tensorflow as tf

import trainer


# Duration of a time step interval in the timeseries.
# Training and prediction data must be resampled to this time step delta.
TIME_STEP_INTERVAL = timedelta(hours=1)


def to_unix_time(timestamp: datetime) -> int:
    return time.mktime(timestamp.timetuple())


def with_fixed_time_steps(input_data: dict[str, np.ndarray]) -> pd.DataFrame:
    return (
        pd.DataFrame(input_data)
        .assign(timestamp=lambda df: df["timestamp"].map(datetime.utcfromtimestamp))
        .resample(TIME_STEP_INTERVAL, on="timestamp")
        .mean()
        .reset_index()
        .assign(timestamp=lambda df: df["timestamp"].map(to_unix_time))
        .interpolate()
    )


def read_data(data_file: str) -> pd.DataFrame:
    mmsi = os.path.splitext(os.path.basename(data_file))[0]
    with tf.io.gfile.GFile(data_file, "rb") as f:
        return with_fixed_time_steps(np.load(f)["x"]).assign(
            mmsi=lambda df: df["mmsi"].map(lambda _: int(mmsi)),
        )


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
        columns=["mmsi", "timestamp", "distance_from_shore"]
    )


def generate_training_points(data: pd.DataFrame) -> Iterable[dict[str, np.ndarray]]:
    # Pandas assigns NaN (Not-a-Number) if a value is missing.
    # If is_fishing equals itself it means it's populated because (NaN != NaN).
    # For the training data points, we only get points where we have a label.
    padding = trainer.PADDING
    training_point_indices = (
        data[padding:].query("is_fishing == is_fishing").index.tolist()
    )
    for point_index in training_point_indices:
        # For the inputs, we grab the past data and the data point itself.
        inputs = (
            data.drop(columns=["is_fishing"])
            .loc[point_index - padding : point_index]
            .to_dict("list")
        )
        # For the outputs, we only grab the label from the data point itself.
        outputs = (
            data[["is_fishing"]]
            .loc[point_index:point_index]
            .astype("int8")
            .to_dict("list")
        )

        yield {
            name: np.reshape(values, (len(values), 1))
            for name, values in {**inputs, **outputs}.items()
        }
