from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

def define_polynomial_model(degree, alpha):
    return Pipeline([
                     ('polynomial features', PolynomialFeatures(degree=degree)),
                     ('ridge regression', Ridge(alpha=alpha))
                    ])
