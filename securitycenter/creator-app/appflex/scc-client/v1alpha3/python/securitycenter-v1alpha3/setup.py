# Copyright 2018 Google LLC
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
"""A setup module for the GAPIC Cloud Security Command Center API library.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import io
import sys

install_requires = [
    'google-api-core >= 0.1.0, < 0.2.0dev',
    'googleapis-common-protos[grpc] >= 1.5.2, < 2.0dev',
]

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='google-cloud-securitycenter',
    version='0.1.0',
    author='Google LLC',
    author_email='googleapis-packages@google.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description='GAPIC library for the Cloud Security Command Center API',
    include_package_data=True,
    long_description=long_description,
    install_requires=install_requires,
    license='Apache 2.0',
    packages=find_packages(exclude=('tests*', )),
    namespace_packages=['google', 'google.cloud'],
    url='https://github.com/googleapis/googleapis',
    zip_safe=False,
)
