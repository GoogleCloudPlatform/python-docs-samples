import tensorflow as tf
from typing import Dict, Tuple

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
NUM_CLASSIFICATIONS = 9


def read_dataset(filename: str, patch_size: int, batch_size: int) -> tf.data.Dataset:
    """Reads a compressed TFRecord dataset and preprocesses it into a machine
    learning friendly format."""
    input_shape = (patch_size, patch_size)
    features_dict = {
        band_name: tf.io.FixedLenFeature(input_shape, tf.float32)
        for band_name in INPUT_BANDS + OUTPUT_BANDS
    }
    return (
        tf.data.TFRecordDataset(filename, compression_type="GZIP")
        .map(
            lambda example: tf.io.parse_single_example(example, features_dict),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        .cache()
        .batch(batch_size)
        .prefetch(tf.data.AUTOTUNE)
    )


def preprocess(values: Dict[str, tf.Tensor]) -> Tuple[tf.Tensor, tf.Tensor]:
    """Splits inputs and outputs into a tuple and converts the output
    classifications into one-hot encodings."""
    inputs = tf.stack([values[band] for band in INPUT_BANDS], axis=-1)
    outputs = tf.one_hot(tf.cast(values["landcover"], tf.uint8), NUM_CLASSIFICATIONS)
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
    training_file: str,
    validation_file: str,
    save_model_to: str,
    patch_size: int,
    epochs: int,
    batch_size: int = 256,
) -> None:
    """Creates, trains and saves a new model."""
    training_dataset = read_dataset(training_file, patch_size, batch_size)
    validation_dataset = read_dataset(validation_file, patch_size, batch_size)

    model = new_model(training_dataset)
    model.fit(
        training_dataset.shuffle(10),
        validation_data=validation_dataset,
        epochs=epochs,
    )
    model.save(save_model_to)
