# Google Cloud Monitoring Samples

This section contains samples for [Google Cloud Monitoring](https://cloud.google.com/monitoring).

## Running the samples

1. Your environment must be setup with [authentication
information](https://developers.google.com/identity/protocols/application-default-credentials#howtheywork). *Note* that Cloud Monitoring does not currently work
with `gcloud auth`. You will need to use a *service account* when running
locally and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

        $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json

2. Install dependencies from `requirements.txt`:

        $ pip install -r requirements.txt

3. Depending on the sample, you may also need to create resources on the [Google Developers Console](https://console.developers.google.com). Refer to the sample description and associated documentation page.

## Additional resources

For more information on Cloud Monitoring you can visit:

> https://cloud.google.com/monitoring

For more information on the Stackdriver Monitoring API Python library surface you
can visit:

> https://developers.google.com/resources/api-libraries/documentation/storage/v2beta2/python/latest/

For information on the Python Client Library visit:

> https://developers.google.com/api-client-library/python
