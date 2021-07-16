# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_sklearn_task]
# [START aiplatform_sklearn_task_imports]
import argparse
import os
import re

from google.cloud import storage
import joblib
from sklearn.metrics import mean_absolute_error

from trainer import utils
from trainer.sklearn_model import model
# [END aiplatform_sklearn_task_imports]


# [START aiplatform_sklearn_task_args]
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="path to input data"
    )
    parser.add_argument(
        "--degree",
        type=int,
        help="degree of the polynomial regression, default=1 (linear model)",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        help="Regularization strength, default=0 (Standard Regression)",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        help="Output directory for the model.",
        default=os.getenv("AIP_MODEL_DIR"),
    )
    return parser.parse_args()
# [END aiplatform_sklearn_task_args]


# [START aiplatform_sklearn_task_fit]
def fit_model(
    input_path: str,
    model_dir: str,
    degree: int = 1,
    alpha: int = 0
) -> None:
    """Train, evaluate and save model given model configuration"""
    print(f"Fitting model with degree={args.degree} and alpha={args.alpha}")

    # Split datasets into training and testing
    train_feature, eval_feature, train_target, eval_target = utils.load_data(
        input_path)

    # Create sklearn pipeline for a polynomial model defined in model.py"""
    polynomial_model = model.polynomial_model(degree, alpha)

    # Fit the sklearn model
    print("Fitting model...")
    polynomial_model.fit(train_feature, train_target)

    # Evaluate the model
    print("Evaluating model...")
    pred_target = polynomial_model.predict(eval_feature)
    mae = mean_absolute_error(eval_target, pred_target)

    print(f"Done. Model had MAE={mae}")
# [END aiplatform_sklearn_task_fit]

# [START aiplatform_sklearn_task_export]
    # Save model to GCS
    print("Saving model")
    matches = re.match("gs://(.*?)/(.*)", model_dir)
    bucket = matches.group(1)
    blob = matches.group(2)

    model_dump = "model.joblib"
    joblib.dump(polynomial_model, model_dump)

    blob_name = os.path.join(blob, model_dump)
    client = storage.Client()
    client.bucket(bucket).blob(blob_name).upload_from_filename(model_dump)
    print("Model saved")
# [END aiplatform_sklearn_task_export]


if __name__ == "__main__":
    args = get_args()

    kwargs = {}
    if args.degree:
        kwargs["degree"] = args.degree
    if args.alpha:
        kwargs["alpha"] = args.alpha

    fit_model(args.input_path, args.model_dir, **kwargs)
# [END aiplatform_sklearn_task]
