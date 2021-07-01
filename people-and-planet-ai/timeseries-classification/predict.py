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

import numpy as np
from tensorflow import keras

from typing import Dict, List

import trainer


def run(model_dir: str, inputs: Dict[str, List[float]]) -> Dict[str, np.ndarray]:
    # Our model always expects a batch prediction,
    # so we create a batch with a single prediction request.
    #   {input: [time_steps, 1]} --> {input: [1, time_steps, 1]}
    batch_size = 1
    inputs_batch = {
        name: np.reshape(values, (batch_size, len(values), 1))
        for name, values in inputs.items()
    }

    # Get our model's predictions.
    model = keras.models.load_model(model_dir)

    # Include the timestamp for each prediction so we can merge them back to the request data.
    predictions_batch = {
        "timestamp": [inputs_batch["timestamp"][0][trainer.PADDING : -trainer.PADDING]],
        **model.predict(inputs_batch),
    }

    # We got a batch of a single prediction, with a single number per time step.
    # So we extract the single prediction and flatten into a 1-dimensional vector.
    #   {output: [1, time_steps, 1]} --> {output: [time_steps]}
    return {name: values[0].flatten() for name, values in predictions_batch.items()}
