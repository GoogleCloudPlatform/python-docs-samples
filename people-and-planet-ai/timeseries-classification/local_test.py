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

import os
import tempfile
from unittest import mock

import numpy as np
import pandas as pd
import pytest
import tensorflow as tf

import create_datasets
import predict
import trainer


TEST_VALUE_DICT = {
    "distance_from_port": [[182558.08203125], [181616.03125], [180523.0390625]],
    "speed": [[3.275000035775], [3.2000000477], [3.0750000477]],
    "course": [[81.87499809262499], [36.5999984741], [83.60000038145]],
    "lat": [[-22.482420921325], [-22.4892024994], [-22.500276088725002]],
    "lon": [[-40.124936103825], [-40.1333656311], [-40.146536827074996]],
    "is_fishing": [[1.0]],
}


def test_validated_missing_field() -> None:
    tensor_dict = {}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(KeyError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_incompatible_type() -> None:
    tensor_dict = {"x": tf.constant(["a", "b", "c"])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(TypeError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_incompatible_shape() -> None:
    tensor_dict = {"x": tf.constant([1.0])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(ValueError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_ok() -> None:
    tensor_dict = {"x": tf.constant([1.0, 2.0, 3.0])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    trainer.validated(tensor_dict, values_spec)

    tensor_dict = {"x": tf.constant([[1.0], [2.0], [3.0]])}
    values_spec = {"x": tf.TensorSpec(shape=(None, 1), dtype=tf.float32)}
    trainer.validated(tensor_dict, values_spec)


def test_serialize_deserialize() -> None:
    serialized = trainer.serialize(TEST_VALUE_DICT)
    inputs, outputs = trainer.deserialize(serialized)
    assert set(inputs.keys()) == set(trainer.INPUTS_SPEC.keys())
    assert set(outputs.keys()) == set(trainer.OUTPUTS_SPEC.keys())


@mock.patch.object(trainer, "PADDING", 2)
def test_e2e_local() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        train_data_dir = os.path.join(temp_dir, "datasets", "train")
        eval_data_dir = os.path.join(temp_dir, "datasets", "eval")
        model_dir = os.path.join(temp_dir, "model")
        tensorboard_dir = os.path.join(temp_dir, "tensorboard")
        checkpoint_dir = os.path.join(temp_dir, "checkpoints")

        # Create the dataset TFRecord files.
        create_datasets.run(
            raw_data_dir="test_data",
            raw_labels_dir="test_data",
            train_data_dir=train_data_dir,
            eval_data_dir=eval_data_dir,
            train_eval_split=[80, 20],
        )
        assert os.listdir(train_data_dir), "no training files found"
        assert os.listdir(eval_data_dir), "no evaluation files found"

        # Train the model and save it.
        trainer.run(
            train_data_dir=train_data_dir,
            eval_data_dir=eval_data_dir,
            model_dir=model_dir,
            tensorboard_dir=tensorboard_dir,
            checkpoint_dir=checkpoint_dir,
            train_epochs=2,
            eval_steps=100,
            batch_size=32,
        )
        assert os.listdir(model_dir), "no model files found"
        assert os.listdir(tensorboard_dir), "no tensorboard files found"
        assert os.listdir(checkpoint_dir), "no checkpoint files found"

        # Load the trained model and make a prediction.
        with open("test_data/56980685061237.npz", "rb") as f:
            input_data = pd.DataFrame(np.load(f)["x"])
        predictions = predict.run(model_dir, input_data.to_dict("list"))

        # Check that we get non-empty predictions.
        assert "is_fishing" in predictions
        assert len(predictions["is_fishing"]) > 0
