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
from opentelemetry import propagate, trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# [END trace_demo_imports]

# [START trace_demo_middleware]
app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
# [END trace_demo_middleware]

# [START trace_demo_create_exporter]
def configure_exporter(exporter):
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(exporter))
    propagate.set_global_textmap(CloudTraceFormatPropagator())


configure_exporter(CloudTraceSpanExporter())
tracer = trace.get_tracer(__name__)
# [END trace_demo_create_exporter]

@app.route("/")
def template_test():
    # Sleep for a random time to imitate a random processing time
    time.sleep(random.uniform(0, 0.5))

    # Keyword that gets passed in will be concatenated to the final output string.
    keyword = app.config['keyword']
    # If there is no endpoint, return the output string.
    url = app.config['endpoint']
    if url == "":
        return keyword, 200

    # Endpoint is the next service to send string to.
    data = {'body': keyword}

    # [START trace_context_header]
    with tracer.start_as_current_span("span_" + keyword):
    response = requests.get(
        url,
        params=data
    )
    # [END trace_context_header]
    return response.text + keyword

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword",  default="", help="name of the service.")
    parser.add_argument("--endpoint", default="", help="endpoint to dispatch appended string, simply respond if not set")

    args = parser.parse_args()
    app.config['keyword'] = args.keyword
    app.config['endpoint'] = args.endpoint
    app.run(debug=True, host="0.0.0.0", port=8080)
