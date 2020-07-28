import argparse
import os
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
import joblib

from . import model

import hypertune

from .. import util


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--job-dir',
            type=str,
            required=True,
            help='local of GCS location for model export')
    parser.add_argument(
            '--degree',
            type=int,
            default=1,
            help='degree of the polynomial regression, default=1 (linear model)')
    parser.add_argument(
            '--alpha',
            type=float,
            default=0,
            help='Regularization strength, default=0 (Standard Regression)')

    args, _ = parser.parse_known_args()
    return args

def fit_model(args):
    print(f'Fitting model with degree={args.degree} and alpha={args.alpha}')

    print('Loading data from GCS...')
    train_x, train_y, test_x, test_y = util.load_data()

    print('Fitting model...')
    poly_model = model.define_polynomial_model(args.degree, args.alpha)
    poly_model.fit(train_x, train_y)

    print('Evaluating model...')
    pred_y = poly_model.predict(test_x)
    mae = mean_absolute_error(test_y, pred_y)


    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag='mean_absolute_error',
            metric_value=mae,
            global_step=1000)

    print(f'Done. Model had MAE={mae}')

    model_filename = 'model.joblib'
    print('Saving model')
    if 'gs://' in args.job_dir:
        joblib.dump(poly_model, model_filename)
        util.copy_file_to_GCS(model_filename, args.job_dir)
    else:
        joblib.dump(poly_model, os.path.join(args.job_dir, model_filename))
    print('Model saved')



if __name__ == '__main__':
    args = get_args()
    fit_model(args)
