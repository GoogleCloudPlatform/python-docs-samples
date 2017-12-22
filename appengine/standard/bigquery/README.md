# Google App Engine accessing BigQuery using OAuth2

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/bigquery/README.md

This sample demonstrates [authenticating to BigQuery in App Engine using OAuth2](https://cloud.google.com/bigquery/authentication).

<!-- auto-doc-link -->
These samples are used on the following documentation pages:

>
* https://cloud.google.com/bigquery/authentication
* https://cloud.google.com/monitoring/api/authentication

<!-- end-auto-doc-link -->

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## Setup

1. You'll need a client id for your project. Follow [these instructions](https://cloud.google.com/bigquery/authentication#clientsecrets). Once you've downloaded the client's json secret copy it into the sample directory and rename it to `client_secrets.json`.

2. Update `main.py` and replace `<your-project-id>` with your project's ID.
