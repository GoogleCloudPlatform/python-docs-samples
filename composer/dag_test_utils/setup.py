import os

from setuptools import find_packages
from setuptools import setup



# # TODO: verify if this is needed
# PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

# # TODO: verify if this is needed
# # TODO: verify if renovate would update this
# REQUIREMENTS = [
#     'apache-airflow[gcp]==1.10.12',
# ]

setup(
    name="dag_test_utils", # Replace with your own username
    version="0.0.1",
    url="git@github.com:GoogleCloudPlatform/python-docs-samples.git#egg=dag_test_utils&subdirectory=composer/dag_test_utils",
    author="Google Cloud Platform",
    author_email="googleapis-publisher@google.com",
    description="Utilities used to unit test example DAGs",
    packages=find_packages(),
    py_modules=['unit_testing']
)