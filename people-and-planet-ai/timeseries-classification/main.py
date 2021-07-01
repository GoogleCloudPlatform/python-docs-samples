#!/usr/bin/env python

from datetime import datetime
import flask
import json

import create_datasets
import train_model
import predict

app = flask.Flask(__name__)


@app.route("/")
def run_root():
    return "Your request was successful! 🎉"


@app.route("/create-datasets")
def run_create_datasets():
    request = flask.request.get_json()

    default_job_id = f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    job_id = create_datasets.run(
        raw_data_dir=request["raw_data_dir"],
        raw_labels_dir=request["raw_labels_dir"],
        train_data_dir=request["train_data_dir"],
        eval_data_dir=request["eval_data_dir"],
        train_eval_split=request.get("train_eval_split", [80, 20]),
        runner="DataflowRunner",
        job_id=request.get("job_id", default_job_id),
        project=request["project"],
        region=request["region"],
        temp_location=request.get("temp_location"),
        sdk_container_image=request["image"],
        experiments=["use_runner_v2"],
    )

    response = {
        "job_type": "Dataflow pipeline",
        "job_id": job_id,
        "job_url": f"https://console.cloud.google.com/dataflow/jobs/{request['region']}/{job_id}?project={request['project']}",
    }
    return json.dumps(response, indent=2)


@app.route("/train-model")
def run_train_model():
    request = flask.request.get_json()

    job_id = train_model.run(
        project=request["project"],
        region=request["region"],
        train_data_dir=request["train_data_dir"],
        eval_data_dir=request["eval_data_dir"],
        output_dir=request["output_dir"],
        image=request["image"],
        train_steps=request.get("train_steps", 10000),
        eval_steps=request.get("eval_steps", 1000),
    )

    response = {
        "job_type": "Vertex AI custom training",
        "job_id": job_id,
        "job_url": f"https://console.cloud.google.com/vertex-ai/locations/{request['region']}/training/{job_id}?project={request['project']}",
    }
    return json.dumps(response, indent=2)


@app.route("/predict")
def run_predict():
    request = flask.request.get_json()

    predictions = predict.run(
        model_dir=request["model_dir"],
        inputs=request["inputs"],
    )

    # Convert the numpy arrays to Python lists to make them JSON-encodable.
    response = {name: values.tolist() for name, values in predictions.items()}
    return json.dumps(response, indent=2)


if __name__ == "__main__":
    import os

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
