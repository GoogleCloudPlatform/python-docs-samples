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

"""This trains a TensorFlow model to classify land cover.

The model is a simple Fully Convolutional Network (FCN) using the
TensorFlow Keras high-level API.
"""

import os
from typing import Dict, Tuple

import tensorflow as tf

# Define the input and output names for the model.
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

# Number of land cover classifications.
NUM_CLASSIFICATIONS = 9


def preprocess(values: Dict[str, tf.Tensor]) -> Tuple[Dict[str, tf.Tensor], tf.Tensor]:
    """Splits inputs and outputs into a tuple and converts them into a
    machine learning friendly format.

    Args:
        values: Dictionary of 2D tensors, each corrseponding to one band.

    Returns: A tuple of (inputs, outputs).
    """

    # Create a dictionary of band values.
    inputs = {name: values[name] for name in INPUT_BANDS}

    # Convert the labels into one-hot encoded vectors.
    outputs = tf.one_hot(tf.cast(values["landcover"], tf.uint8), NUM_CLASSIFICATIONS)
    return (inputs, outputs)


def read_dataset(
    file_pattern: str, patch_size: int, batch_size: int
) -> tf.data.Dataset:
    """Reads a compressed TFRecord dataset and preprocesses it into a machine
    learning friendly format.

    Args:
        file_pattern: Local or Cloud Storage file pattern of the TFRecord files.
        patch_size: Patch size of each example.
        batch_size: Number of examples to batch together.

    Returns: A tf.data.Dataset ready to feed to the model.
    """

    # Create the features dictionary, we need this to parse the TFRecords.
    input_shape = (patch_size, patch_size)
    features_dict = {
        band_name: tf.io.FixedLenFeature(input_shape, tf.float32)
        for band_name in INPUT_BANDS + OUTPUT_BANDS
    }

    return (
        # We list and interleave each TFRecord file to process each file in parallel.
        tf.data.Dataset.list_files(file_pattern)
        .interleave(
            lambda filename: tf.data.TFRecordDataset(filename, compression_type="GZIP"),
            cycle_length=tf.data.AUTOTUNE,
            num_parallel_calls=tf.data.AUTOTUNE,
            deterministic=False,
        )
        # We batch before parsing and preprocessing so it can be vectorized.
        .batch(batch_size)
        .map(
            lambda batch: tf.io.parse_example(batch, features_dict),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        # Finally we cache the current batch and prefetch the next one.
        .cache()
        .prefetch(tf.data.AUTOTUNE)
        # For more information on how to optimize your tf.data.Dataset, see:
        #   https://www.tensorflow.org/guide/data_performance
    )


def new_model(training_dataset: tf.data.Dataset) -> tf.keras.Model:
    """Creates a new Fully Convolutional Network (FCN) model.

    Args:
        training_dataset: The dataset to use for the normalization layer.

    Returns: A Fully Convolutional Network model.
    """

    # Adapt the Normalization layer with the training dataset.
    normalization = tf.keras.layers.Normalization()
    normalization.adapt(
        training_dataset.map(
            lambda inputs, _: tf.stack([inputs[name] for name in INPUT_BANDS], axis=-1)
        )
    )

    # Define the Fully Convolutional Network.
    layers = [
        tf.keras.Input(shape=(None, None, len(INPUT_BANDS))),
        normalization,
        tf.keras.layers.Conv2D(filters=32, kernel_size=5, activation="relu"),
        tf.keras.layers.Conv2DTranspose(filters=16, kernel_size=5, activation="relu"),
        tf.keras.layers.Dense(NUM_CLASSIFICATIONS, activation="softmax"),
    ]
    fcn_model = tf.keras.Sequential(layers, name="FullyConvolutionalNetwork")

    # Define the input dictionary layers.
    input_layers = {
        name: tf.keras.Input(shape=(None, None, 1), name=name) for name in INPUT_BANDS
    }

    # Model wrapper that takes an input dictionary and feeds it to the FCN.
    inputs = tf.keras.layers.concatenate(input_layers.values())
    model = tf.keras.Model(input_layers, fcn_model(inputs))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=[
            tf.keras.metrics.OneHotIoU(
                num_classes=NUM_CLASSIFICATIONS,
                target_class_ids=list(range(NUM_CLASSIFICATIONS)),
            )
        ],
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
    """Creates, trains and saves a new model.

    Args:
        training_data: File pattern for the training data files.
        validation_data: File pattern for the validation data files.
        model_path: Path to save the model to.
        patch_size: Patch size of the training and validation datasets.
        epochs: Number of times to go through the training dataset.
        batch_size: Number of examples for the model to look at the same time.
    """

    # Read the training and validation datasets.
    training_dataset = read_dataset(training_data, patch_size, batch_size)
    validation_dataset = read_dataset(validation_data, patch_size, batch_size)

    # Create, train and save the model.
    model = new_model(training_dataset)
    model.fit(
        training_dataset,
        validation_data=validation_dataset,
        epochs=epochs,
    )
    model.save(model_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--training-data",
        default="datasets/training*.tfrecord.gz",
        help="Local or Cloud Storage file pattern for the training data files.",
    )
    parser.add_argument(
        "--validation-data",
        default="datasets/validation*.tfrecord.gz",
        help="Local or Cloud Storage file pattern for the validation data files.",
    )
    parser.add_argument(
        "--model-path",
        default=os.environ.get("AIP_MODEL_DIR", "model"),
        help="Local or Cloud Storage path to save the model to.",
    )
    parser.add_argument(
        "--patch-size",
        default=16,
        type=int,
        help="Patch size of the training and validation datasets.",
    )
    parser.add_argument(
        "--epochs",
        default=50,
        type=int,
        help="Number of times to go through the training dataset.",
    )
    parser.add_argument(
        "--batch-size",
        default=256,
        type=int,
        help="Number of examples for the model to look at the same time.",
    )
    args = parser.parse_args()

    run(**vars(args))
