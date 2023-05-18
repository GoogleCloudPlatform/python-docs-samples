#!/usr/bin/env python

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

import flask

app = flask.Flask(__name__)


@app.route("/ping", methods=["POST"])
def run_root() -> str:
    args = flask.request.get_json() or {}
    return {
        "response": "Your request was successful! 🎉",
        "args": args["message"],
    }


@app.route("/predict", methods=["POST"])
def run_predict() -> dict:
    import predict

    try:
        args = flask.request.get_json() or {}
        bucket = args["bucket"]
        model_dir = f"gs://{bucket}/model_output"
        data = args["data"]
        predictions = predict.run(data, model_dir)

        return {
            "method": "predict",
            "model_dir": model_dir,
            "predictions": predictions,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    import os

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
