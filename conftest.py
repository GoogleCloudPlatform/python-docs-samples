import os

import pytest
from testing.cloud import Config, get_resource_path


@pytest.fixture(scope='session')
def cloud_config():
    """Provides a configuration option as a proxy to environment variables."""
    return Config()


@pytest.fixture(scope='module')
def resource(request):
    """Provides a function that returns the full path to a local or global
    testing resource"""
    local_path = os.path.dirname(request.module.__file__)
    return lambda *args: get_resource_path(args, local_path)
