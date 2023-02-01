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

"""This trains a TensorFlow Keras model to classify land cover.

The model is a simple Fully Convolutional Network (FCN).
"""

from __future__ import annotations

import tensorflow as tf

# Default values.
EPOCHS = 100
BATCH_SIZE = 512
KERNEL_SIZE = 5

# Constants.
NUM_INPUTS = 13
NUM_CLASSES = 9
TRAIN_TEST_RATIO = 90  # percent for training, the rest for testing/validation
SHUFFLE_BUFFER_SIZE = BATCH_SIZE * 8


def read_example(serialized: bytes) -> tuple[tf.Tensor, tf.Tensor]:
    """Parses and reads a training example from TFRecords.

    Args:
        serialized: Serialized example bytes from TFRecord files.

    Returns: An (inputs, labels) pair of tensors.
    """
    features_dict = {
        "inputs": tf.io.FixedLenFeature([], tf.string),
        "labels": tf.io.FixedLenFeature([], tf.string),
    }
    example = tf.io.parse_single_example(serialized, features_dict)
    inputs = tf.io.parse_tensor(example["inputs"], tf.float32)
    labels = tf.io.parse_tensor(example["labels"], tf.uint8)

    # TensorFlow cannot infer the shape's rank, so we set the shapes explicitly.
    inputs.set_shape([None, None, NUM_INPUTS])
    labels.set_shape([None, None, 1])

    # Classifications are measured against one-hot encoded vectors.
    one_hot_labels = tf.one_hot(labels[:, :, 0], NUM_CLASSES)
    return (inputs, one_hot_labels)


def read_dataset(data_path: str) -> tf.data.Dataset:
    """Reads compressed TFRecord files from a directory into a tf.data.Dataset.

    Args:
        data_path: Local or Cloud Storage directory path where the TFRecord files are.

    Returns: A tf.data.Dataset with the contents of the TFRecord files.
    """
    file_pattern = tf.io.gfile.join(data_path, "*.tfrecord.gz")
    file_names = tf.data.Dataset.list_files(file_pattern).cache()
    dataset = tf.data.TFRecordDataset(file_names, compression_type="GZIP")
    return dataset.map(read_example, num_parallel_calls=tf.data.AUTOTUNE)


def split_dataset(
    dataset: tf.data.Dataset,
    batch_size: int = BATCH_SIZE,
    train_test_ratio: int = TRAIN_TEST_RATIO,
) -> tuple[tf.data.Dataset, tf.data.Dataset]:
    """Splits a dataset into training and validation subsets.

    Args:
        dataset: Full dataset with all the training examples.
        batch_size: Number of examples per training batch.
        train_test_ratio: Percent of the data to use for training.

    Returns: A (training, validation) dataset pair.
    """
    # For more information on how to optimize your tf.data.Dataset, see:
    #   https://www.tensorflow.org/guide/data_performance
    indexed_dataset = dataset.enumerate()  # add an index to each example
    train_dataset = (
        indexed_dataset.filter(lambda i, _: i % 100 <= train_test_ratio)
        .map(lambda _, data: data, num_parallel_calls=tf.data.AUTOTUNE)  # remove index
        .cache()  # cache the individual parsed examples
        .shuffle(SHUFFLE_BUFFER_SIZE)  # randomize the examples for the batches
        .batch(batch_size)  # batch randomized examples
        .prefetch(tf.data.AUTOTUNE)  # prefetch the next batch
    )
    validation_dataset = (
        indexed_dataset.filter(lambda i, _: i % 100 > train_test_ratio)
        .map(lambda _, data: data, num_parallel_calls=tf.data.AUTOTUNE)  # remove index
        .batch(batch_size)  # batch the parsed examples, no need to shuffle
        .cache()  # cache the batches of examples
        .prefetch(tf.data.AUTOTUNE)  # prefetch the next batch
    )
    return (train_dataset, validation_dataset)


def create_model(
    dataset: tf.data.Dataset, kernel_size: int = KERNEL_SIZE
) -> tf.keras.Model:
    """Creates a Fully Convolutional Network Keras model.

    Make sure you pass the *training* dataset, not the validation or full dataset.

    Args:
        dataset: Training dataset used to normalize inputs.
        kernel_size: Size of the square of neighboring pixels for the model to look at.

    Returns: A compiled fresh new model (not trained).
    """
    # Adapt the preprocessing layers.
    normalization = tf.keras.layers.Normalization()
    normalization.adapt(dataset.map(lambda inputs, _: inputs))

    # Define the Fully Convolutional Network.
    model = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(None, None, NUM_INPUTS)),
            normalization,
            tf.keras.layers.Conv2D(32, kernel_size, activation="relu"),
            tf.keras.layers.Conv2DTranspose(16, kernel_size, activation="relu"),
            tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=[
            tf.keras.metrics.OneHotIoU(
                num_classes=NUM_CLASSES,
                target_class_ids=list(range(NUM_CLASSES)),
            )
        ],
    )
    return model


def run(
    data_path: str,
    model_path: str,
    epochs: int = EPOCHS,
    batch_size: int = BATCH_SIZE,
    kernel_size: int = KERNEL_SIZE,
    train_test_ratio: int = TRAIN_TEST_RATIO,
) -> tf.keras.Model:
    """Creates and trains the model.

    Args:
        data_path: Local or Cloud Storage directory path where the TFRecord files are.
        model_path: Local or Cloud Storage directory path to store the trained model.
        epochs: Number of times the model goes through the training dataset during training.
        batch_size: Number of examples per training batch.
        kernel_size: Size of the square of neighboring pixels for the model to look at.
        train_test_ratio: Percent of the data to use for training.

    Returns: The trained model.
    """
    print(f"data_path: {data_path}")
    print(f"model_path: {model_path}")
    print(f"epochs: {epochs}")
    print(f"batch_size: {batch_size}")
    print(f"kernel_size: {kernel_size}")
    print(f"train_test_ratio: {train_test_ratio}")
    print("-" * 40)

    dataset = read_dataset(data_path)
    (train_dataset, test_dataset) = split_dataset(dataset, batch_size, train_test_ratio)

    model = create_model(train_dataset, kernel_size)
    print(model.summary())

    model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=epochs,
    )
    model.save(model_path)
    print(f"Model saved to path: {model_path}")
    return model


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        required=True,
        help="Local or Cloud Storage directory path where the TFRecord files are.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Local or Cloud Storage directory path to store the trained model.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=EPOCHS,
        help="Number of times the model goes through the training dataset during training.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help="Number of examples per training batch.",
    )
    parser.add_argument(
        "--kernel-size",
        type=int,
        default=KERNEL_SIZE,
        help="Size of the square of neighboring pixels for the model to look at.",
    )
    parser.add_argument(
        "--train-test-ratio",
        type=int,
        default=TRAIN_TEST_RATIO,
        help="Percent of the data to use for training.",
    )
    args = parser.parse_args()

    run(
        data_path=args.data_path,
        model_path=args.model_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        kernel_size=args.kernel_size,
        train_test_ratio=args.train_test_ratio,
    )
