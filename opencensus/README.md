<img src="https://avatars2.githubusercontent.com/u/38480854?v=3&s=96" alt="OpenCensus logo" title="OpenCensus" align="right" height="96" width="96"/>

# OpenCensus Stackdriver Metrics Sample

[OpenCensus](https://opencensus.io) is a toolkit for collecting application
performance and behavior data. OpenCensus includes utilities for distributed
tracing, metrics collection, and context propagation within and between
services.

This example demonstrates using the OpenCensus client to send metrics data to
the [Stackdriver Monitoring](https://cloud.google.com/monitoring/docs/)
backend.

## Prerequisites

Install the OpenCensus core and Stackdriver exporter libraries:

```sh
pip install -r opencensus/requirements.txt
```

Make sure that your environment is configured to [authenticate with
GCP](https://cloud.google.com/docs/authentication/getting-started).

## Running the example

```sh
python opencensus/metrics_quickstart.py
```

The example generates a histogram of simulated latencies, which is exported to
Stackdriver after 60 seconds. After it's exported, the histogram will be
visible on the [Stackdriver Metrics
Explorer](https://app.google.stackdriver.com/metrics-explorer) page as
`OpenCensus/task_latency_view`.
