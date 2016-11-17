# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

# To add services insert key value pair of the name of the service and
# the port you want it to run on when running locally
SERVICES = {
    'default': 8000,
    'static': 8001
}


def init_app(app):
    # The GAE_INSTANCE environment variable will be set when deployed to GAE.
    gae_instance = os.environ.get(
        'GAE_INSTANCE', os.environ.get('GAE_MODULE_INSTANCE'))
    environment = 'production' if gae_instance is not None else 'development'
    app.config['SERVICE_MAP'] = map_services(environment)


def map_services(environment):
    """Generates a map of services to correct urls for running locally
    or when deployed."""
    url_map = {}
    for service, local_port in SERVICES.items():
        if environment == 'production':
            url_map[service] = production_url(service)
        if environment == 'development':
            url_map[service] = local_url(local_port)
    return url_map


def production_url(service_name):
    """Generates url for a service when deployed to App Engine."""
    project_id = os.environ.get('GAE_LONG_APP_ID')
    project_url = '{}.appspot.com'.format(project_id)
    if service_name == 'default':
        return 'https://{}'.format(project_url)
    else:
        return 'https://{}-dot-{}'.format(service_name, project_url)


def local_url(port):
    """Generates url for a service when running locally"""
    return 'http://localhost:{}'.format(str(port))
