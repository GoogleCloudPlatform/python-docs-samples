# Copyright 2023 Google LLC
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

from datetime import datetime
import os

from flask import Flask, request

from weather.data import get_inputs_patch
from weather.model import WeatherModel

app = Flask(__name__)

MODEL = WeatherModel.from_pretrained("model")


@app.route("/")
def ping() -> dict:
    """Check that we can communicate with the service and get arguments."""
    return {
        "response": "✅ I got your request!",
        "args": request.args,
    }


# predict/2019-09-02T18:00/25.507,-78.322
@app.route("/predict/<iso_date>/<float(signed=True):lat>,<float(signed=True):lon>")
def predict(iso_date: str, lat: float, lon: float) -> dict:
    # Optional HTTP request parameters.
    #   https://en.wikipedia.org/wiki/Query_string
    patch_size = request.args.get("patch-size", 128, type=int)

    date = datetime.fromisoformat(iso_date)
    point = (lon, lat)
    inputs = get_inputs_patch(date, point, patch_size).tolist()
    predictions = MODEL.predict(inputs)
    return {"inputs": inputs, "predictions": predictions.tolist()}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
