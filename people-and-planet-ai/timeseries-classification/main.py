#!/usr/bin/env python

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

from datetime import datetime
import os

import flask

import create_datasets
import train_model
import predict

app = flask.Flask(__name__)

project = os.environ["PROJECT"]
bucket = os.environ["BUCKET"]
region = os.environ["REGION"]
container_image = os.environ["CONTAINER_IMAGE"]
storage_path = os.environ.get("STORAGE_PATH", "samples/global-fishing-watch")

raw_data_dir = f"gs://{bucket}/{storage_path}/data"
raw_labels_dir = f"gs://{bucket}/{storage_path}/labels"
train_data_dir = f"gs://{bucket}/{storage_path}/datasets/train"
eval_data_dir = f"gs://{bucket}/{storage_path}/datasets/eval"
training_dir = f"gs://{bucket}/{storage_path}/training"
temp_dir = f"gs://{bucket}/{storage_path}/temp"


@app.route("/ping", methods=["POST"])
def run_root():
    args = flask.request.get_json() or {}

    return {
        "response": "Your request was successful! 🎉",
        "args": args,
    }


@app.route("/create-datasets", methods=["POST"])
def run_create_datasets():
    try:
        args = flask.request.get_json() or {}

        job_id = create_datasets.run(
            raw_data_dir=raw_data_dir,
            raw_labels_dir=raw_labels_dir,
            train_data_dir=train_data_dir,
            eval_data_dir=eval_data_dir,
            train_eval_split=args.get("train_eval_split", [80, 20]),
            # Apache Beam runner pipeline options.
            runner="DataflowRunner",
            job_name=f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            project=project,
            region=region,
            sdk_container_image=container_image,
            temp_location=temp_dir,
            experiments=["use_runner_v2"],
        )

        return {
            "job_id": job_id,
            "job_url": f"https://console.cloud.google.com/dataflow/jobs/{region}/{job_id}?project={project}",
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.route("/train-model", methods=["POST"])
def run_train_model():
    try:
        args = flask.request.get_json() or {}

        job_id = train_model.run(
            project=project,
            region=region,
            container_image=container_image,
            train_data_dir=train_data_dir,
            eval_data_dir=eval_data_dir,
            training_dir=training_dir,
            train_steps=args.get("train_steps", 10000),
            eval_steps=args.get("eval_steps", 1000),
        )

        return {
            "job_id": job_id,
            "job_url": f"https://console.cloud.google.com/vertex-ai/locations/{region}/training/{job_id}/cpu?project={project}",
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.route("/predict", methods=["POST"])
def run_predict():
    try:
        args = flask.request.get_json() or {}

        predictions = predict.run(
            model_dir=args.get("model_dir", f"{training_dir}/model"),
            inputs=args["inputs"],
        )

        # Convert the numpy arrays to Python lists to make them JSON-encodable.
        return {name: values.tolist() for name, values in predictions.items()}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    import os

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
