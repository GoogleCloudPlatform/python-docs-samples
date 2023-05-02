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

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

import data_utils
import trainer

model: Optional[keras.Model] = None


def predict(model: keras.Model, inputs: Dict[str, np.ndarray]) -> pd.DataFrame:
    data = data_utils.with_fixed_time_steps(inputs)

    # Our model always expects a batch prediction, so we create a batch with
    # a single prediction request.
    #   {input: [time_steps]} --> {input: [1, time_steps, 1]}
    inputs_batch = {
        name: np.reshape(data[name].to_numpy(), (1, len(data[name]), 1))
        for name in trainer.INPUTS_SPEC.keys()
    }

    predictions = model.predict(inputs_batch)
    return data[trainer.PADDING:].assign(is_fishing=predictions["is_fishing"][0])


def run(model_dir: str, inputs: Dict[str, List[float]]) -> Dict[str, np.ndarray]:
    # Get the latest model.
    model_path = tf.io.gfile.glob(model_dir)[-1]

    # Cache the model so it only has to be loaded once per runtime.
    global model
    if model is None:
        model = keras.models.load_model(model_dir)

    return predict(model, inputs).to_dict("list")
