# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@pytest.fixture(scope='session')
def cloud_config():
    """Provides a configuration object as a proxy to environment variables."""
    return Namespace(
        project=os.environ.get('GCLOUD_PROJECT'),
        storage_bucket=os.environ.get('CLOUD_STORAGE_BUCKET'),
        client_secrets=os.environ.get('GOOGLE_CLIENT_SECRETS'))


def get_resource_path(resource, local_path):
    local_resource_path = os.path.join(local_path, 'resources', *resource)

    if os.path.exists(local_resource_path):
        return local_resource_path
    else:
        raise EnvironmentError('Resource {} not found.'.format(
            os.path.join(*resource)))


@pytest.fixture(scope='module')
def resource(request):
    """Provides a function that returns the full path to a local or global
    testing resource"""
    local_path = os.path.dirname(request.module.__file__)
    return lambda *args: get_resource_path(args, local_path)
