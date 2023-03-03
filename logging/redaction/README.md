# Logging redaction tutorial code samples

This is a sample of the [DataFlow] pipeline that detects and masks US Social Security Numbers from the log payloads at ingestion time.
The folder contains the following files:

* [Dockerfile] to use for a customized a DataFlow job container in order to save initialization time
* [Boilerplate code][boilerplate] that implements a pipeline for streaming log entries from [PubSub] to a destination Log bucket
* [Final version][final] of the pipeline that includes all modifications to the [boilerplate] code that are required to implement log redaction
* [Requirements] file to be install the DataFlow job's environment with missing component(s)

If you have a Google Cloud account and an access to a GCP project you can launch an interactive tutorial in Cloud Console and see how the sample works.
To run the tutorial press the button below.

[![Open in Cloud Shell][shell_img]][shell_link]

NOTE: To run this tutorial you will need to have permissions to enable Google APIs, provision PubSub, DataFlow and Cloud Storage resources as well as permissions to call DLP API

[dataflow]: https://cloud.google.com/dataflow
[pubsub]: https://cloud.google.com/pubsub
[dockerfile]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/logging/redaction/Dockerfile
[boilerplate]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/logging/redaction/log_redaction.py
[final]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/logging/redaction/log_redaction_final.py
[requirements]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/logging/redaction/requirements.txt
[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/?walkthrough_id=cloud-ops-log-redacting-on-ingestion
