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

import numpy as np
import tensorflow as tf


def run(data: dict, model_dir: str) -> dict:
    model = tf.keras.models.load_model(model_dir)
    prediction_values = np.array(list(data.values()))
    transposed = np.transpose(prediction_values, (1, 2, 0))
    predictions = model.predict(np.expand_dims(transposed, axis=0)).tolist()

    return {"predictions": predictions}
