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

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)


def configure_exporter(exporter):
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(exporter))
    propagate.set_global_textmap(CloudTraceFormatPropagator())


configure_exporter(CloudTraceSpanExporter())
tracer = trace.get_tracer(__name__)


@app.route("/")
def template_test():
    # Sleep for a random time to imitate a random processing time
    time.sleep(random.uniform(0, 0.5))

    with tracer.start_as_current_span("span1"):
        with tracer.start_as_current_span("span2"):
            with tracer.start_as_current_span("span3"):
                print("Hello world from Cloud Trace Exporter!")

    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
