# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_tfkeras_model]
"""Defines a Keras model and input function for training."""

# [START aiplatform_tfkeras_model_tf_import]
import numpy as np
import tensorflow as tf
# [END aiplatform_tfkeras_model_tf_import]


# [START aiplatform_tfkeras_model_input_fn]
def input_fn(
    features: np.array,
    labels: np.array,
    num_epochs: int,
    batch_size: int,
    shuffle: bool
) -> tf.data.Dataset:
    """Generates an input function to be used for model training"""

    inputs = (features, labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(features))

    # Call repeat after shuffling to prevent epochs from blending together
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset
# [END aiplatform_tfkeras_model_input_fn]


# [START aiplatform_tfkeras_model_create_keras_model]
# [START aiplatform_tfkeras_model_create_keras_model_init]
def create_keras_model(
    input_dim: int,
    output_dim: int,
    learning_rate: float
) -> tf.keras.Sequential:
    """Creates Keras Model for regression"""

    # Define regularizers
    kernel_regularizer = tf.keras.regularizers.l1_l2(l1=1e-5, l2=1e-4)
    bias_regularizer = tf.keras.regularizers.l2(1e-4)
# [END aiplatform_tfkeras_model_create_keras_model_init]
# [START aiplatform_tfkeras_model_create_keras_model_define]
    # Define model layers
    Dense = tf.keras.layers.Dense
    # Define Keras model
    model = tf.keras.Sequential(
        [
            Dense(
                11,
                activation=tf.nn.relu,
                input_shape=(input_dim,),
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
            ),
            Dense(80, activation=tf.nn.relu),
            Dense(150, activation=tf.nn.relu),
            Dense(
                300,
                activation=tf.nn.relu,
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
            ),
            Dense(500, activation=tf.nn.relu),
            Dense(
                800,
                activation=tf.nn.relu,
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
            ),
            Dense(1000, activation=tf.nn.relu),
            Dense(
                1500,
                activation=tf.nn.relu,
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
            ),
            Dense(output_dim),
        ]
    )

    # Compile Keras model
    model.compile(loss="mae", optimizer="adam", metrics=["mae"])

    return model
# [END aiplatform_tfkeras_model_create_keras_model_define]
# [END aiplatform_tfkeras_model_create_keras_model]
# [END aiplatform_tfkeras_model]
