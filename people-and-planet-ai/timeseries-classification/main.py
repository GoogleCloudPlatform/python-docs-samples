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

# Default values for dataset creation.
DEFAULT_TRAIN_EVAL_SPLIT = [80, 20]

# Default values for training in Vertex AI.
DEFAULT_TRAIN_STEPS = 10000
DEFAULT_EVAL_STEPS = 100
DEFAULT_BATCH_SIZE = 64
DEFAULT_MACHINE_TYPE = "n1-standard-4"
DEFAULT_GPU_TYPE = "NVIDIA_TESLA_T4"
DEFAULT_GPU_COUNT = 2

# Google Cloud resources.
project = os.environ["PROJECT"]
region = os.environ["REGION"]
storage_path = os.environ["STORAGE_PATH"]
container_image = os.environ["CONTAINER_IMAGE"]

raw_data_dir = f"{storage_path}/data"
raw_labels_dir = f"{storage_path}/labels"
train_data_dir = f"{storage_path}/datasets/train"
eval_data_dir = f"{storage_path}/datasets/eval"
training_dir = f"{storage_path}/training"
temp_dir = f"{storage_path}/temp"


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
        params = {
            "raw_data_dir": raw_data_dir,
            "raw_labels_dir": raw_labels_dir,
            "train_data_dir": train_data_dir,
            "eval_data_dir": eval_data_dir,
            "train_eval_split": args.get("train_eval_split", DEFAULT_TRAIN_EVAL_SPLIT),
            # Apache Beam runner pipeline options.
            "runner": "DataflowRunner",
            "job_name": f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "project": project,
            "region": region,
            "sdk_container_image": container_image,
            "temp_location": temp_dir,
            "experiments": ["use_runner_v2"],
        }
        job_id = create_datasets.run(**params)

        return {
            "job_id": job_id,
            "job_url": f"https://console.cloud.google.com/dataflow/jobs/{region}/{job_id}?project={project}",
            "params": params,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.route("/train-model", methods=["POST"])
def run_train_model():
    try:
        args = flask.request.get_json() or {}
        params = {
            "project": project,
            "region": region,
            "container_image": container_image,
            "train_data_dir": train_data_dir,
            "eval_data_dir": eval_data_dir,
            "training_dir": training_dir,
            "train_steps": args.get("train_steps", DEFAULT_TRAIN_STEPS),
            "eval_steps": args.get("eval_steps", DEFAULT_EVAL_STEPS),
            "batch_size": args.get("batch_size", DEFAULT_BATCH_SIZE),
            "machine_type": args.get("machine_type", DEFAULT_MACHINE_TYPE),
            "gpu_type": args.get("gpu_type", DEFAULT_GPU_TYPE),
            "gpu_count": args.get("gpu_count", DEFAULT_GPU_COUNT),
        }
        job_id = train_model.run(**params)

        return {
            "job_id": job_id,
            "job_url": f"https://console.cloud.google.com/vertex-ai/locations/{region}/training/{job_id}/cpu?project={project}",
            "params": params,
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
