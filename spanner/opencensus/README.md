# Cloud Spanner OpenCensus Sample

This sample includes a single executable module that demonstrates how to capture
gRPC client metrics for [Google Cloud Spanner](https://cloud.google.com/spanner/)
queries, including round-trip latency: `capture_grpc_metrics.py`.

## Build and Run

1.  Enable APIs for your project.
    [Click here](https://console.cloud.google.com/flows/enableapi?apiid=spanner.googleapis.com&showconfirmation=true)
    to visit Cloud Platform Console and enable the Google Cloud Spanner API.
2.  Create a Cloud Spanner instance and database via the Cloud Plaform Console's
    [Cloud Spanner section](http://console.cloud.google.com/spanner).
3.  Enable application default credentials by running the command `gcloud auth
    application-default login`.
4.  Enable application default credentials by running the command `gcloud auth
    application-default login`.
5.  Create `Singer` and `Album` tables following the
    [Cloud Spanner example schema](https://cloud.google.com/spanner/docs/schema-and-data-model#schema-examples)
6.  Install dependencies: `pip install -R requirements.txt`
7.  Run the sample application: `python spanner/opencensus/capture_grpc_metric <instance-id> <database-id>`
