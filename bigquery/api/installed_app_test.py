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

import os
import re

from oauth2client.client import GoogleCredentials

import installed_app

PROJECT = os.environ['GCLOUD_PROJECT']
CLIENT_SECRETS = os.environ['GOOGLE_CLIENT_SECRETS']


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_main(monkeypatch, capsys):
    installed_app.CLIENT_SECRETS = CLIENT_SECRETS

    # Replace the user credentials flow with Application Default Credentials.
    # Unfortunately, there's no easy way to fully test the user flow.
    def mock_run_flow(flow, storage, args):
        return GoogleCredentials.get_application_default()

    monkeypatch.setattr(installed_app.tools, 'run_flow', mock_run_flow)

    args = Namespace(
        project_id=PROJECT,
        logging_level='INFO',
        noauth_local_webserver=True)

    installed_app.main(args)

    out, _ = capsys.readouterr()

    assert re.search(re.compile(
        r'bigquery#datasetList', re.DOTALL), out)
