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


"""Trigger a DAG in Cloud Composer 2 environment using the Airflow 2 stable REST API."""

# [START composer_2_trigger_dag]

import google.auth
from google.auth.transport.requests import AuthorizedSession

AUTH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'

def make_composer2_web_server_request(url, method='GET', **kwargs):
  """
  Make a request to Cloud Composer 2 environment's web server.
  Args:
    url: The URL to fetch.
    method: The request method to use ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT',
      'PATCH', 'DELETE')
    **kwargs: Any of the parameters defined for the request function:
              https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
  """

  credentials, _ = google.auth.default(scopes=[AUTH_SCOPE])
  authed_session = AuthorizedSession(credentials)
  
  # Set the default timeout, if missing
  if 'timeout' not in kwargs:
    kwargs['timeout'] = 90
  
  return authed_session.request(
    method, 
    url,
    **kwargs)


def trigger_dag(web_server_url, dag_id, data, context=None):

  endpoint = f'api/v1/dags/{dag_id}/dagRuns'
  request_url = f'{web_server_url}/{endpoint}'
  json_data = { 'conf': data }

  response = make_composer2_web_server_request(request_url, 
    method='POST',
    json=json_data
    )

  if response.status_code == 403:
    raise Exception('You do not have a permission to access this resource.')
  elif response.status_code != 200:
    raise Exception(
      'Bad request: {!r} / {!r} / {!r}'.format(
        response.status_code, response.headers, response.text))
  else:
    return response.text


if __name__ == "__main__":

  # Replace dag_id with the ID of the DAG that you want to run.
  dag_id="composer_sample_dag"
  # Replace dag_config with configuration parameters for the DAG run.
  dag_config={"test": "value"}
  # Replace web_server_url with the Airflow web server address. To obtain this
  # URL, run the following command for your environment:
  # gcloud composer environments describe example-environment \
  #  --location=us-central1 \
  #  --format="value(config.airflowUri)"
  web_server_url="https://example-airflow-ui-url-dot-us-central1.composer.googleusercontent.com"

  response_text = trigger_dag(
    web_server_url=web_server_url, dag_id=dag_id, data=dag_config)

  print(response_text)

# [END composer_2_trigger_dag]
