# Using Cloud SQL from Google App Engine

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/cloudsql/README.md

This is an example program showing how to use the native MySQL connections from Google App Engine to [Google Cloud SQL](https://cloud.google.com/sql).

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## Setup

1. You will need to create a [Cloud SQL instance](https://cloud.google.com/sql/docs/create-instance).

2. Edit the update the `env_variables` section in `app.yaml` with your Cloud SQL configuration.
