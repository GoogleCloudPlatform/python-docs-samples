from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

def define_polynomial_model(degree, alpha):
    return Pipeline([
                     ('polynomial features',
                         PolynomialFeatures(degree=degree)),
                     ('ridge regression', Ridge(alpha=alpha))
                    ])
