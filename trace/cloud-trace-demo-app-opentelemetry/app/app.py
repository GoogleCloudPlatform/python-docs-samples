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

import os
import random
import time

import flask
# [START trace_demo_imports]
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# [END trace_demo_imports]
import requests


# [START trace_demo_create_exporter]
def configure_exporter(exporter):
    set_global_textmap(CloudTraceFormatPropagator())
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(tracer_provider)


configure_exporter(CloudTraceSpanExporter())
tracer = trace.get_tracer(__name__)
# [END trace_demo_create_exporter]


# [START trace_demo_middleware]
app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
# [END trace_demo_middleware]


@app.route("/")
def template_test():
    # Sleep for a random time to imitate a random processing time
    time.sleep(random.uniform(0, 0.5))

    # If there is an endpoint, send keyword to next service.
    # Return received input with the keyword
    keyword = os.getenv("KEYWORD")
    endpoint = os.getenv("ENDPOINT")
# [START trace_context_header]
    if endpoint is not None and endpoint != "":
        data = {'body': keyword}
        response = requests.get(
            endpoint,
            params=data,
        )
        return keyword + "\n" + response.text
    else:
        return keyword, 200
# [END trace_context_header]


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(debug=True, host="0.0.0.0", port=port)
