# Copyright 2020 Google LLC
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
"""
A sample app demonstrating CloudTraceSpanExporter
"""
import argparse
import random
import time

# [START trace_demo_imports]
import flask
import requests
from opentelemetry import trace, propagators
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter
# [END trace_demo_imports]

app = flask.Flask(__name__)



propagator = propagators.get_global_httptextformat()


@app.route('/')
def template_test():
    # Sleep for a random time to imitate a random processing time
    time.sleep(random.uniform(0, 0.5))
    # Keyword that gets passed in will be concatenated to the final output string.
    output_string = app.config['keyword']
    # If there is no endpoint, return the output string.
    url = app.config['endpoint']
    if url == '':
        return output_string, 200
    # Endpoint is the next service to send string to.
    data = {'body': output_string}

    request_to_downstream = requests.Request(
        url,
        params=data
    )
    # [START trace_context_header]

    context = propagator.extract(get_header_from_flask_request, flask.request)
    propagator.inject(set_header_into_requests_request, request_to_downstream, context=context)
    session = requests.Session()
    response = session.send(request_to_downstream.prepare())
    # [END trace_context_header]
    return response.text + app.config['keyword']


def set_header_into_requests_request(request: requests.Request, key: str, value: str):
    request.headers[key] = value


def get_header_from_flask_request(request, key):
    return request.headers.get_all(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', default='', help='name of the service.')
    parser.add_argument('--endpoint', default='',
                        help='endpoint to dispatch appended string, simply respond if not set')
    args = parser.parse_args()
    app.config['keyword'] = args.keyword
    app.config['endpoint'] = args.endpoint

    trace.set_tracer_provider(TracerProvider())
    # cloud_trace_exporter = CloudTraceSpanExporter()
    trace.get_tracer_provider().add_span_processor(
        SimpleExportSpanProcessor(ConsoleSpanExporter())
    )
    tracer = trace.get_tracer(__name__)

    app.run(debug=True, host='0.0.0.0', port=8080)
