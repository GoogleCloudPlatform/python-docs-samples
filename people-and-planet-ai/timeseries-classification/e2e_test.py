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
import pytest
import tensorflow as tf
from tensorflow import keras

import create_dataset
import trainer


TEST_VALUE_DICT = {
    "distance_from_port": [[182558.08203125], [181616.03125], [180523.0390625]],
    "speed": [[3.275000035775], [3.2000000477], [3.0750000477]],
    "course": [[81.87499809262499], [36.5999984741], [83.60000038145]],
    "lat": [[-22.482420921325], [-22.4892024994], [-22.500276088725002]],
    "lon": [[-40.124936103825], [-40.1333656311], [-40.146536827074996]],
    "is_fishing": [[1.0]],
}


def test_validated_missing_field():
    tensor_dict = {}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(KeyError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_incompatible_type():
    tensor_dict = {"x": tf.constant(["a", "b", "c"])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(TypeError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_incompatible_shape():
    tensor_dict = {"x": tf.constant([1.0])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    with pytest.raises(ValueError):
        trainer.validated(tensor_dict, values_spec)


def test_validated_ok():
    tensor_dict = {"x": tf.constant([1.0, 2.0, 3.0])}
    values_spec = {"x": tf.TensorSpec(shape=(3,), dtype=tf.float32)}
    trainer.validated(tensor_dict, values_spec)

    tensor_dict = {"x": tf.constant([[1.0], [2.0], [3.0]])}
    values_spec = {"x": tf.TensorSpec(shape=(None, 1), dtype=tf.float32)}
    trainer.validated(tensor_dict, values_spec)


def test_serialize_deserialize():
    serialized = trainer.serialize(TEST_VALUE_DICT)
    inputs, outputs = trainer.deserialize(serialized)
    assert set(inputs.keys()) == set(trainer.INPUTS_SPEC.keys())
    assert set(outputs.keys()) == set(trainer.OUTPUTS_SPEC.keys())


@mock.patch.object(trainer, "PADDING", 1)
def test_e2e_local():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the dataset TFRecord files.
        train_files, eval_files = create_dataset.run(
            input_data="test_data/*.npz",
            input_labels="test_data/*.csv",
            output_datasets_path=temp_dir,
        )

        # Train the model and save it.
        model_dir = os.path.join(temp_dir, "model")
        trainer.train_model(
            train_files=train_files,
            eval_files=eval_files,
            model_dir=model_dir,
            tensorboard_dir=os.path.join(temp_dir, "tensorboard"),
            train_steps=1,
            eval_steps=1,
        )

        # Load the trained model and make a prediction.
        trained_model = keras.models.load_model(model_dir)
        np_dict = {
            field: np.reshape(value, (1, len(value), 1))
            for field, value in TEST_VALUE_DICT.items()
            if field in trainer.INPUTS_SPEC
        }
        predictions = trained_model.predict(np_dict)

        # Check that we get predictions of the correct type and shape.
        assert set(predictions.keys()) == {"is_fishing"}
        assert predictions["is_fishing"].dtype == np.float32
        assert predictions["is_fishing"].shape == (1, 1, 1)
