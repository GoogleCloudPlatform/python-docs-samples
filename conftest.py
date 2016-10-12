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
import requests


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@pytest.fixture(scope='session')
def cloud_config():
    """Provides a configuration object as a proxy to environment variables."""
    return Namespace(
        project=os.environ.get('GCLOUD_PROJECT'),
        storage_bucket=os.environ.get('CLOUD_STORAGE_BUCKET'),
        client_secrets=os.environ.get('GOOGLE_CLIENT_SECRETS'),
        bigtable_instance=os.environ.get('BIGTABLE_CLUSTER'),
        api_key=os.environ.get('API_KEY'))


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


def fetch_gcs_resource(resource, tmpdir, _chunk_size=1024):
    resp = requests.get(resource, stream=True)
    dest_file = str(tmpdir.join(os.path.basename(resource)))
    with open(dest_file, 'wb') as f:
        for chunk in resp.iter_content(_chunk_size):
            f.write(chunk)

    return dest_file


@pytest.fixture(scope='module')
def remote_resource(cloud_config):
    """Provides a function that downloads the given resource from Cloud
    Storage, returning the path to the downloaded resource."""
    remote_uri = 'http://storage.googleapis.com/{}/'.format(
        cloud_config.storage_bucket)

    return lambda path, tmpdir: fetch_gcs_resource(
        remote_uri + path.strip('/'), tmpdir)
