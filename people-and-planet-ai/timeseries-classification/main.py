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
import re
import subprocess

import flask
import numpy as np

app = flask.Flask(__name__)

# Default values for dataset creation.
DEFAULT_TRAIN_EVAL_SPLIT = [80, 20]

# Default values for training in Vertex AI.
DEFAULT_TRAIN_EPOCHS = 100
DEFAULT_BATCH_SIZE = 128
DEFAULT_MACHINE_TYPE = "n1-standard-4"
DEFAULT_GPU_TYPE = "NVIDIA_TESLA_T4"
DEFAULT_GPU_COUNT = 2

# Google Cloud resources.
PROJECT = os.environ["PROJECT"]
REGION = os.environ["REGION"]
STORAGE_PATH = os.environ["STORAGE_PATH"]
CONTAINER_IMAGE = os.environ["CONTAINER_IMAGE"]

RAW_DATA_DIR = f"{STORAGE_PATH}/data"
RAW_LABELS_DIR = f"{STORAGE_PATH}/labels"
TRAIN_DATA_DIR = f"{STORAGE_PATH}/datasets/train"
EVAL_DATA_DIR = f"{STORAGE_PATH}/datasets/eval"
TRAINING_DIR = f"{STORAGE_PATH}/training"
TEMP_DIR = f"{STORAGE_PATH}/temp"


@app.route("/ping", methods=["POST"])
def run_root() -> dict:
    args = flask.request.get_json() or {}
    return {
        "response": "Your request was successful! 🎉",
        "args": args,
    }


@app.route("/create-datasets", methods=["POST"])
def run_create_datasets() -> dict:
    try:
        args = flask.request.get_json() or {}
        job_name = f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        cmd = [
            "python",
            "create_datasets.py",
            f"--raw-data-dir={args.get('raw_data_dir', RAW_DATA_DIR)}",
            f"--raw-labels-dir={args.get('raw_labels_dir', RAW_LABELS_DIR)}",
            f"--train-data-dir={args.get('train_data_dir', TRAIN_DATA_DIR)}",
            f"--eval-data-dir={args.get('eval_data_dir', EVAL_DATA_DIR)}",
            f"--train-eval-split={args.get('train_eval_split', DEFAULT_TRAIN_EVAL_SPLIT)}",
            "--runner=DataflowRunner",
            f"--job_name={job_name}",
            f"--project={args.get('project', PROJECT)}",
            f"--region={args.get('region', REGION)}",
            f"--temp_location={args.get('temp_location', TEMP_DIR)}",
        ]
        result = subprocess.run(cmd, check=True, capture_output=True)
        output = result.stdout.decode("utf-8")

        m = re.search(r"^job_id: (.*)$", output)
        if m:
            job_id = m.group(1)
            job_url = (
                f"https://console.cloud.google.com/dataflow/jobs/{REGION}/{job_id}?project={PROJECT}",
            )
        else:
            job_id = ""
            job_url = ""

        return {
            "method": "create-datasets",
            "job_name": job_name,
            "job_id": job_id,
            "job_url": job_url,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.route("/train-model", methods=["POST"])
def run_train_model() -> dict:
    import train_model

    try:
        args = flask.request.get_json() or {}
        params = {
            "project": args.get("project", PROJECT),
            "region": args.get("region", REGION),
            "train_data_dir": args.get("train_data_dir", TRAIN_DATA_DIR),
            "eval_data_dir": args.get("eval_data_dir", EVAL_DATA_DIR),
            "training_dir": args.get("training_dir", TRAINING_DIR),
            "train_epochs": args.get("train_epochs", DEFAULT_TRAIN_EPOCHS),
            "batch_size": args.get("batch_size", DEFAULT_BATCH_SIZE),
            "machine_type": args.get("machine_type", DEFAULT_MACHINE_TYPE),
            "gpu_type": args.get("gpu_type", DEFAULT_GPU_TYPE),
            "gpu_count": args.get("gpu_count", DEFAULT_GPU_COUNT),
            "sync": args.get("sync", False),
        }
        train_model.run(**params)

        return {
            "method": "train-model",
            "params": params,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.route("/predict", methods=["POST"])
def run_predict() -> dict:
    import predict

    try:
        args = flask.request.get_json() or {}
        params = {
            "model_dir": args.get("model_dir", f"{TRAINING_DIR}/model"),
            "inputs": args["inputs"],
        }
        predictions = predict.run(**params)

        # Convert the numpy arrays to Python lists to make them JSON-encodable.
        return {
            "method": "predict",
            "model_dir": params["model_dir"],
            "input_shapes": {
                name: np.shape(values) for name, values in params["inputs"].items()
            },
            "predictions": predictions,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
