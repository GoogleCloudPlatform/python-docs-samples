# Copyright 2020 Google LLC
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

import argparse
import os
import random
import time

from flask import Flask, redirect, url_for

# [START trace_setup_python_configure]
from opentelemetry import propagate, trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def initialize_tracer(project_id):
    trace.set_tracer_provider(TracerProvider())
    cloud_trace_exporter = CloudTraceSpanExporter(project_id)
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(cloud_trace_exporter)
    )
    propagate.set_global_textmap(CloudTraceFormatPropagator())
    opentelemetry_tracer = trace.get_tracer(__name__)

    return opentelemetry_tracer


# [END trace_setup_python_configure]

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return redirect(url_for("index"))


# [START trace_setup_python_quickstart]
@app.route("/index.html", methods=["GET"])
def index():
    tracer = app.config["TRACER"]
    with tracer.start_as_current_span(name="index"):
        # Add up to 1 sec delay, weighted toward zero
        time.sleep(random.random() ** 2)
        result = "Tracing requests"

    return result


# [END trace_setup_python_quickstart]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--project_id",
        help="Project ID you want to access.",
        default=os.environ["GOOGLE_CLOUD_PROJECT"],
        required=True,
    )
    args = parser.parse_args()

    app.config["TRACER"] = initialize_tracer(args.project_id)

    app.run()
