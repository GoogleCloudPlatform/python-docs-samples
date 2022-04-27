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

from typing import Dict, Tuple

import tensorflow as tf

SENTINEL2_BANDS = [
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

# Define the input and output names for the model.
INPUT_BANDS = SENTINEL2_BANDS
OUTPUT_BANDS = ["landcover"]

NUM_CLASSIFICATIONS = 9


def read_dataset(
    file_pattern: str, patch_size: int, batch_size: int
) -> tf.data.Dataset:
    """Reads a compressed TFRecord dataset and preprocesses it into a machine
    learning friendly format."""
    input_shape = (patch_size, patch_size)
    features_dict = {
        band_name: tf.io.FixedLenFeature(input_shape, tf.float32)
        for band_name in INPUT_BANDS + OUTPUT_BANDS
    }
    # For more information on how to optimize your tf.data.Dataset, refer to:
    #   https://www.tensorflow.org/guide/data_performance
    return (
        tf.data.Dataset.list_files(file_pattern)
        .interleave(
            lambda filename: tf.data.TFRecordDataset(filename, compression_type="GZIP"),
            cycle_length=tf.data.AUTOTUNE,
            num_parallel_calls=tf.data.AUTOTUNE,
            deterministic=False,
        )
        .batch(batch_size)
        .map(
            lambda batch: tf.io.parse_example(batch, features_dict),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        .cache()
        .prefetch(tf.data.AUTOTUNE)
    )


def preprocess(patch: Dict[str, tf.Tensor]) -> Tuple[tf.Tensor, tf.Tensor]:
    """Splits inputs and outputs into a tuple and converts the output
    classifications into one-hot encodings."""
    inputs = tf.stack([patch[band] for band in INPUT_BANDS], axis=-1)
    outputs = tf.one_hot(tf.cast(patch["landcover"], tf.uint8), NUM_CLASSIFICATIONS)
    return (inputs, outputs)


def new_model(training_dataset: tf.data.Dataset) -> tf.keras.Model:
    """Creates a new Fully Convolutional Network (FCN) model."""
    normalization = tf.keras.layers.Normalization()
    normalization.adapt(training_dataset.map(lambda x, _: x))

    model = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(None, None, len(INPUT_BANDS))),
            normalization,
            tf.keras.layers.Conv2D(filters=32, kernel_size=5, activation="relu"),
            tf.keras.layers.Conv2DTranspose(
                filters=16, kernel_size=5, activation="relu"
            ),
            tf.keras.layers.Dense(NUM_CLASSIFICATIONS, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def run(
    training_data: str,
    validation_data: str,
    model_path: str,
    patch_size: int,
    epochs: int,
    batch_size: int = 256,
) -> None:
    """Creates, trains and saves a new model."""
    training_dataset = read_dataset(training_data, patch_size, batch_size)
    validation_dataset = read_dataset(validation_data, patch_size, batch_size)

    model = new_model(training_dataset)
    model.fit(
        training_dataset.shuffle(10),
        validation_data=validation_dataset,
        epochs=epochs,
    )
    model.save(model_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--training-data", default="datasets/training*.tfrecord.gz")
    parser.add_argument("--validation-data", default="datasets/validation*.tfrecord.gz")
    parser.add_argument("--model-path", default="model")
    parser.add_argument("--patch-size", default=16, type=int)
    parser.add_argument("--epochs", default=50, type=int)
    parser.add_argument("--batch-size", default=256, type=int)
    args = parser.parse_args()

    run(**vars(args))
