# Stackdriver Logging v2 API Samples

`snippets.py` is a simple command-line program to demonstrate writing to a log,
listing its entries, and deleting it.

`export.py` demonstrates how to interact with sinks which are used to export
logs to Google Cloud Storage, Cloud Pub/Sub, or BigQuery. The sample uses
Google Cloud Storage, but can be easily adapted for other outputs.

<!-- auto-doc-link -->
<!-- end-auto-doc-link -->

## Prerequisites

All samples require a [Google Cloud Project](https://console.cloud.google.com).

To run `export.py`, you will also need a Google Cloud Storage Bucket. 

    gsutil mb gs://[YOUR_PROJECT_ID]

You must add Cloud Logging as an owner to the bucket. To do so, add
`cloud-logs@google.com` as an owner to the bucket. See the
[exportings logs](https://cloud.google.com/logging/docs/export/configure_export#configuring_log_sinks)
docs for complete details. 

# Running locally

Use the [Cloud SDK](https://cloud.google.com/sdk) to provide authentication:

    gcloud beta auth application-default login

Run the samples:

    python snippets.py -h
    python export.py -h

