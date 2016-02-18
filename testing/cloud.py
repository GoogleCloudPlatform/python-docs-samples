# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common testing tools for cloud samples.
"""

import inspect
import os
import unittest

from .utils import silence_requests


GLOBAL_RESOURCE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'resources')


# Note: these values must also be whitelisted in tox.ini.
ENVIRONMENT_VARIABLES = frozenset((
    'GCLOUD_PROJECT',
    'CLOUD_STORAGE_BUCKET',
))


class Config(object):
    def __getattr__(self, name):
        if name not in ENVIRONMENT_VARIABLES:
            raise AttributeError(
                'Environment variable {} is not in the whitelist.'
                .format(name))

        if name not in os.environ:
            raise EnvironmentError(
                'Environment variable {} not set.'.format(name))

        return os.environ[name]


def get_resource_path(resource, local_path):
    global_resource_path = os.path.join(GLOBAL_RESOURCE_PATH, *resource)
    local_resource_path = os.path.join(local_path, 'resources', *resource)

    if os.path.exists(local_resource_path):
        return local_resource_path

    if os.path.exists(global_resource_path):
        return global_resource_path

    raise EnvironmentError('Resource {} not found.'.format(
        os.path.join(*resource)))


class CloudTest(unittest.TestCase):
    """Common base class for cloud tests."""
    def __init__(self, *args, **kwargs):
        super(CloudTest, self).__init__(*args, **kwargs)
        self.config = Config()

    @classmethod
    def setUpClass(self):
        silence_requests()

    def resource_path(self, *resource):
        local_path = os.path.dirname(inspect.getfile(self.__class__))
        return get_resource_path(resource, local_path)
