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

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor

# [END trace_demo_imports]

app = flask.Flask(__name__)


def configure_exporter(exporter):
    trace.set_tracer_provider(TracerProvider())

    trace.get_tracer_provider().add_span_processor(SimpleExportSpanProcessor(exporter))


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
    configure_exporter(CloudTraceSpanExporter())
