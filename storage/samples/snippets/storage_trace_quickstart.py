#!/usr/bin/env python

# Copyright 2024 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import sys

"""
Sample that exports OpenTelemetry Traces collected from the Storage client to Cloud Trace.
"""


def run_quickstart(bucket_name, blob_name, data):
    # [START storage_enable_otel_tracing]

    from opentelemetry import trace
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    from opentelemetry.resourcedetector.gcp_resource_detector import (
        GoogleCloudResourceDetector,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.trace.sampling import ALWAYS_ON
    # Optional: Enable traces emitted from the requests HTTP library.
    from opentelemetry.instrumentation.requests import RequestsInstrumentor

    from google.cloud import storage

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"
    # The contents to upload to the file
    # data = "The quick brown fox jumps over the lazy dog."

    # In this sample, we use Google Cloud Trace to export the OpenTelemetry
    # traces: https://cloud.google.com/trace/docs/setup/python-ot
    # Choose and configure the exporter for your environment.

    tracer_provider = TracerProvider(
        # Sampling is set to ALWAYS_ON.
        # It is recommended to sample based on a ratio to control trace ingestion volume,
        # for instance, sampler=TraceIdRatioBased(0.2)
        sampler=ALWAYS_ON,
        resource=GoogleCloudResourceDetector().detect(),
    )

    # Export to Google Cloud Trace.
    tracer_provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    # Optional: Enable traces emitted from the requests HTTP library.
    RequestsInstrumentor().instrument(tracer_provider=tracer_provider)

    # Get the tracer and create a new root span.
    tracer = tracer_provider.get_tracer("My App")
    with tracer.start_as_current_span("trace-quickstart"):
        # Instantiate a storage client and perform a write and read workload.
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data)
        print(f"{blob_name} uploaded to {bucket_name}.")

        blob.download_as_bytes()
        print("Downloaded storage object {} from bucket {}.".format(blob_name, bucket_name))

    # [END storage_enable_otel_tracing]


if __name__ == "__main__":
    run_quickstart(bucket_name=sys.argv[1], blob_name=sys.argv[2], data=sys.argv[3])
