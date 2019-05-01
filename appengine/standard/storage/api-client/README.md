# Cloud Storage & Google App Engine

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/storage/api-client/README.md

This sample demonstrates how to use the [Google Cloud Storage API](https://cloud.google.com/storage/docs/json_api/) from Google App Engine.

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## Setup

Before running the sample:

1. You need a Cloud Storage Bucket. You create one with [`gsutil`](https://cloud.google.com/storage/docs/gsutil):

        gsutil mb gs://your-bucket-name

2. Update `main.py` and replace `<your-bucket-name>` with your Cloud Storage bucket.
