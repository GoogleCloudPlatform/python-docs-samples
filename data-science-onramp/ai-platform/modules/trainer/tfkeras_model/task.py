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

# [START ai_platform_tfkeras_task]
"""Trains a Keras model to predict number of trips
started and ended at Citibike stations. """

# [START ai_platform_tfkeras_task_imports]
import argparse
import os

import tensorflow as tf

from trainer import utils
from trainer.tfkeras_model import model
# [END ai_platform_tfkeras_task_imports]


# [START ai_platform_tfkeras_task_args]
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="path to input data"
    )
    parser.add_argument(
        "--num-epochs",
        type=int,
        help="number of times to go through the data, default=20",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="number of records to read during each training step, default=128",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        help="learning rate for gradient descent, default=.01",
    )
    parser.add_argument(
        "--verbosity",
        choices=["DEBUG", "ERROR", "FATAL", "INFO", "WARN"],
        default="INFO",
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        help="Output directory for the model.",
        default=os.environ["AIP_MODEL_DIR"],
    )
    return parser.parse_args()
# [END ai_platform_tfkeras_task_args]


# [START ai_platform_tfkeras_task_train_and_evaluate]
# [START ai_platform_tfkeras_task_train_and_evaluate_load]
def train_and_evaluate(
    input_path: str,
    model_dir: str,
    num_epochs: int = 5,
    batch_size: int = 128,
    learning_rate: float = 0.01
) -> None:
    """Trains and evaluates the Keras model.

    Uses the Keras model defined in model.py. Saves the trained model in TensorFlow SavedModel
    format to the path defined in part by the --job-dir argument."""

    # Split datasets into training and testing
    train_feature, eval_feature, train_target, eval_target = utils.load_data(input_path)
# [END ai_platform_tfkeras_task_train_and_evaluate_load]

    # [START ai_platform_tfkeras_task_train_and_evaluate_dimensions]
    # Extract dimensions of the data
    num_train_examples, input_dim = train_feature.shape
    num_eval_examples = eval_feature.shape[1]
    output_dim = train_target.shape[1]
    # [END ai_platform_tfkeras_task_train_and_evaluate_dimensions]

    # [START ai_platform_tfkeras_task_train_and_evaluate_model]
    # Create the Keras Model
    keras_model = model.create_keras_model(
        input_dim=input_dim,
        output_dim=output_dim,
        learning_rate=learning_rate,
    )
    # [END ai_platform_tfkeras_task_train_and_evaluate_model]

    # [START ai_platform_tfkeras_task_train_and_evaluate_training_data]
    # Pass a numpy array by passing DataFrame.values
    training_dataset = model.input_fn(
        features=train_feature.values,
        labels=train_target.values,
        shuffle=True,
        num_epochs=num_epochs,
        batch_size=batch_size,
    )
    # [END ai_platform_tfkeras_task_train_and_evaluate_training_data]

    # [START ai_platform_tfkeras_task_train_and_evaluate_validation_data]
    # Pass a numpy array by passing DataFrame.values
    validation_dataset = model.input_fn(
        features=eval_feature.values,
        labels=eval_target.values,
        shuffle=False,
        num_epochs=num_epochs,
        batch_size=num_eval_examples,
    )
    # [END ai_platform_tfkeras_task_train_and_evaluate_validation_data]

    # [START ai_platform_tfkeras_task_train_and_evaluate_fit_export]
    # Train model
    keras_model.fit(
        training_dataset,
        steps_per_epoch=int(num_train_examples / batch_size),
        epochs=num_epochs,
        validation_data=validation_dataset,
        validation_steps=1,
        verbose=1,
    )

    # Export model
    keras_model.save(model_dir)
    print(f"Model exported to: {model_dir}")
    # [END ai_platform_tfkeras_task_train_and_evaluate_fit_export]
# [END ai_platform_tfkeras_task_train_and_evaluate]


if __name__ == "__main__":
    args = get_args()

    kwargs = {}
    if args.num_epochs:
        kwargs["num-epochs"] = args.num_epochs
    if args.batch_size:
        kwargs["batch-size"] = args.batch_size
    if args.learning_rate:
        kwargs["learning-rate"] = args.learning_rate

    tf.compat.v1.logging.set_verbosity(args.verbosity)

    train_and_evaluate(args.input_path, args.model_dir, **kwargs)
# [END ai_platform_tfkeras_task]
