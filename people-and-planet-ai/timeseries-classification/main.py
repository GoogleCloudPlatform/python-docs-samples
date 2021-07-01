#!/usr/bin/env python

from datetime import datetime
from flask import Flask
import json

import create_datasets
import train_model
import predict

app = Flask(__name__)


@app.route("/create-datasets")
def run_create_datasets():
    project = "dcavazos-lyra"
    location = "us-central1"
    data_dir = f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/data"
    labels_dir = f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/labels"
    train_data_dir = (
        f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/datasets/train"
    )
    eval_data_dir = (
        f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/datasets/eval"
    )
    image = "gcr.io/dcavazos-lyra/samples/global-fishing-watch:latest"
    temp_dir = None
    train_eval_split = [80, 20]

    job_id = f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    create_datasets.run(
        data_dir=data_dir,
        labels_dir=labels_dir,
        train_data_dir=train_data_dir,
        eval_data_dir=eval_data_dir,
        train_eval_split=train_eval_split,
        runner="DataflowRunner",
        job_id=job_id,
        project=project,
        region=location,
        temp_location=temp_dir,
        sdk_container_image=image,
        experiments=["use_runner_v2"],
    )
    return job_id


@app.route("/train-model")
def run_train_model():
    project = "dcavazos-lyra"
    location = "us-central1"
    train_data_dir = (
        f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/datasets/train"
    )
    eval_data_dir = (
        f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/datasets/eval"
    )
    output_dir = f"gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/training"
    image = "gcr.io/dcavazos-lyra/samples/global-fishing-watch:latest"
    train_steps = 10000
    eval_steps = 1000
    job_id = (
        f"global-fishing-watch-train-model-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    train_model.run(
        project=project,
        location=location,
        train_data_dir=train_data_dir,
        eval_data_dir=eval_data_dir,
        output_dir=output_dir,
        image=image,
        train_steps=train_steps,
        eval_steps=eval_steps,
    )
    return job_id


@app.route("/predict")
def run_predict():
    model_dir = "gs://dcavazos-lyra-us-central1/samples/global-fishing-watch/model"
    inputs = {
        k: list(range(49))
        for k in ["course", "distance_from_port", "lat", "lon", "speed", "timestamp"]
    }

    predictions = predict.run(model_dir, inputs)
    return json.dumps(
        {name: values.tolist() for name, values in predictions.items()},
        indent=2,
    )


if __name__ == "__main__":
    import os

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
