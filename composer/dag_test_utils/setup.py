# Copyright 2021 Google LLC
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

from setuptools import find_packages
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="cloud_composer_dag_test_utils",
    version="1.0.0",
    url="https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/composer/dag_test_utils",
    author="Google LLC",
    description="Utility used to unit test example Apache Airflow DAGs for Google Cloud Composer. This is not an officially supported Google product.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    py_modules=['internal_unit_testing'],
    install_requires=['apache-airflow[google] >= 2.0.0, < 3.0.0']
)
