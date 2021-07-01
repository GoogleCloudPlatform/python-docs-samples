#!/usr/bin/env python

from datetime import datetime
import flask

import create_datasets
import train_model
import predict

app = flask.Flask(__name__)


@app.route("/ping", methods=["POST"])
def run_root():
    args = flask.request.get_json()
    print(f"args: {args}")

    return {
        "response": "Your request was successful! 🎉",
        "args": args,
    }


@app.route("/create-datasets", methods=["POST"])
def run_create_datasets():
    args = flask.request.get_json()
    print(f"args: {args}")

    default_job_id = f"global-fishing-watch-create-datasets-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    job_id = create_datasets.run(
        raw_data_dir=args["raw_data_dir"],
        raw_labels_dir=args["raw_labels_dir"],
        train_data_dir=args["train_data_dir"],
        eval_data_dir=args["eval_data_dir"],
        train_eval_split=args.get("train_eval_split", [80, 20]),
        runner="DataflowRunner",
        job_id=args.get("job_id", default_job_id),
        project=args["project"],
        region=args["region"],
        temp_location=args.get("temp_location"),
        sdk_container_image=args["image"],
        experiments=["use_runner_v2"],
    )

    return {
        "job_type": "Dataflow pipeline",
        "job_id": job_id,
        "job_url": f"https://console.cloud.google.com/dataflow/jobs/{args['region']}/{job_id}?project={args['project']}",
    }


@app.route("/train-model", methods=["POST"])
def run_train_model():
    args = flask.request.get_json()
    print(f"args: {args}")

    job_id = train_model.run(
        project=args["project"],
        region=args["region"],
        train_data_dir=args["train_data_dir"],
        eval_data_dir=args["eval_data_dir"],
        output_dir=args["output_dir"],
        image=args["image"],
        train_steps=args.get("train_steps", 10000),
        eval_steps=args.get("eval_steps", 1000),
    )

    return {
        "job_type": "Vertex AI custom training",
        "job_id": job_id,
        "job_url": f"https://console.cloud.google.com/vertex-ai/locations/{args['region']}/training/{job_id}?project={args['project']}",
    }


@app.route("/predict", methods=["POST"])
def run_predict():
    args = flask.request.get_json()
    print(f"args: {args}")

    predictions = predict.run(
        model_dir=args["model_dir"],
        inputs=args["inputs"],
    )

    # Convert the numpy arrays to Python lists to make them JSON-encodable.
    return {name: values.tolist() for name, values in predictions.items()}


if __name__ == "__main__":
    import os

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
