# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START ai_platform_sklearn_task]
# [START ai_platform_sklearn_task_imports]
import argparse
import os
import re

import joblib
from sklearn.metrics import mean_absolute_error
from google.cloud import storage

from trainer.sklearn_model import model
from trainer.utils import load_data
# [END ai_platform_sklearn_task_imports]

# [START ai_platform_sklearn_task_args]
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="path to input data"
    )
    parser.add_argument(
        "--job-dir",
        type=str,
        required=True,
        help="local of GCS location for model export",
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
    return parser.parse_args()
# [END ai_platform_sklearn_task_args]

# [START ai_platform_sklearn_task_fit]
def fit_model(input_path, job_dir, degree=1, alpha=0):
    """Train, evaluate and save model given model configuration"""
    print(f"Fitting model with degree={args.degree} and alpha={args.alpha}")

    # Split datasets into training and testing
    train_x, eval_x, train_y, eval_y = load_data(input_path)

    # Create sklearn pipeline for a polynomial model defined in model.py"""
    polynomial_model = model.polynomial_model(degree, alpha)

    # Fit the sklearn model
    print("Fitting model...")
    polynomial_model.fit(train_x, train_y)

    # Evaluate the model
    print("Evaluating model...")
    pred_y = polynomial_model.predict(eval_x)
    mae = mean_absolute_error(eval_y, pred_y)

    print(f"Done. Model had MAE={mae}")
# [END ai_platform_sklearn_task_fit]

# [START ai_platform_sklearn_task_export]
    # Save model to GCS
    print("Saving model")
    matches = re.match("gs://(.*?)/(.*)", job_dir)
    bucket = matches.group(1)
    blob = matches.group(2)

    model_dump = "model.joblib"
    joblib.dump(polynomial_model, model_dump)

    blob_name = os.path.join(blob, model_dump)
    client = storage.Client()
    client.bucket(bucket).blob(blob_name).upload_from_filename(model_dump)
    print("Model saved")
# [END ai_platform_sklearn_task_export]

if __name__ == "__main__":
    args = get_args()
    
    input_path = args.input_path
    job_dir = args.job_dir
    
    kwargs = {}
    if args.degree:
        kwargs["degree"] = args.degree
    if args.alpha:
        kwargs["alpha"] = args.alpha

    fit_model(input_path, job_dir, **kwargs)
# [END ai_platform_sklearn_task]
