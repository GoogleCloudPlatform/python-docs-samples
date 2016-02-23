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
