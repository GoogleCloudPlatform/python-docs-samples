import argparse
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
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
    poly = PolynomialFeatures(degree=args.degree)
    train_x_poly = poly.fit_transform(train_x)
    test_x_poly = poly.fit_transform(test_x)

    ridgeModel = Ridge(alpha=args.alpha)
    ridgeModel.fit(train_x_poly, train_y)


    print('Evaluating model...')
    pred_y = ridgeModel.predict(test_x_poly)
    mae = mean_absolute_error(test_y, pred_y)


    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag='mean_absolute_error',
            metric_value=mae,
            global_step=1000
            )

    print(f'Done. Model had MAE={mae}')


if __name__ == '__main__':
    args = get_args()
    fit_model(args)
