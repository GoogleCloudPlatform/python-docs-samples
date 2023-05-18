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


"""This training script trains binary classifier on Sentinel-2 satellite images.
The model is a fully convolutional neural network that predicts whether a power
plant is turned on or off.

A Sentinel-2 image consists of 13 bands. Each band contains the data for a
specific range of the electromagnetic spectrum.

A JPEG image consists of three channels: Red, Green, and Blue. For Sentinel-2
images, these correspond to Band 4 (red), Band 3 (green), and Band 2 (blue).
These bands contain the raw pixel data directly from the satellite sensors.
For more information on the Sentinel-2 dataset:
https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
"""

from __future__ import annotations

import argparse

import tensorflow as tf

BANDS = [
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
LABEL = "is_powered_on"
BATCH_SIZE = 64


def get_args() -> dict:
    """Parses args."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True, type=str, help="GCS Bucket")
    args = parser.parse_args()
    return args


def parse_tfrecord(example_proto: bytes, features_dict: dict) -> dict:
    """Parses a single tf.train.Example."""

    return tf.io.parse_single_example(example_proto, features_dict)


def create_features_dict() -> dict:
    """Creates dict of features."""

    features_dict = {
        name: tf.io.FixedLenFeature(shape=[33, 33], dtype=tf.float32) for name in BANDS
    }

    features_dict[LABEL] = tf.io.FixedLenFeature(shape=[1, 1], dtype=tf.float32)

    return features_dict


def get_feature_and_label_vectors(
    inputs: dict, features_dict: dict
) -> tuple[tf.Tensor, int]:
    """Formats data."""

    label_value = tf.cast(inputs.pop(LABEL), tf.int32)
    features_vec = [inputs[name] for name in BANDS]
    # (bands, x, y) -> (x, y, bands)
    features_vec = tf.transpose(features_vec, [1, 2, 0])
    return features_vec, label_value


def create_datasets(bucket: str) -> tuple[tf.data.Dataset, tf.data.Dataset]:
    """Creates training and validation datasets."""

    train_data_dir = f"gs://{bucket}/geospatial_training.tfrecord.gz"
    eval_data_dir = f"gs://{bucket}/geospatial_validation.tfrecord.gz"
    features_dict = create_features_dict()

    training_dataset = (
        tf.data.TFRecordDataset(train_data_dir, compression_type="GZIP")
        .map(lambda example_proto: parse_tfrecord(example_proto, features_dict))
        .map(lambda inputs: get_feature_and_label_vectors(inputs, features_dict))
        .batch(64)
    )

    validation_dataset = (
        tf.data.TFRecordDataset(eval_data_dir, compression_type="GZIP")
        .map(lambda example_proto: parse_tfrecord(example_proto, features_dict))
        .map(lambda inputs: get_feature_and_label_vectors(inputs, features_dict))
        .batch(64)
    )

    return training_dataset, validation_dataset


def create_model(training_dataset: tf.data.Dataset) -> tf.keras.Model:
    """Creates model."""

    feature_ds = training_dataset.map(lambda x, y: x)
    normalizer = tf.keras.layers.experimental.preprocessing.Normalization()
    normalizer.adapt(feature_ds)

    inputs = tf.keras.Input(shape=(None, None, 13))
    x = normalizer(inputs)
    x = tf.keras.layers.Conv2D(filters=32, kernel_size=33, activation="relu")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.0001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    args = get_args()
    training_dataset, validation_dataset = create_datasets(args.bucket)
    model = create_model(training_dataset)
    model.fit(training_dataset, validation_data=validation_dataset, epochs=20)
    model.save(f"gs://{args.bucket}/model_output")


if __name__ == "__main__":
    main()
