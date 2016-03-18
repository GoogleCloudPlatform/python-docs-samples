
# Google Cloud Speech API Sample (REST API)

This example demos accessing the [Google Cloud Speech API](http://cloud.google.com/speech)
via its REST API.

## Prerequisites

### Enable the Speech API

If you have not already done so,
[enable the Google Cloud Speech API for your project](https://console.cloud.google.com/apis/api/speech.googleapis.com/overview).
You must be whitelisted to do this.


### Set Up to Authenticate With Your Project's Credentials

The example uses a service account for OAuth2 authentication.
So next, set up to authenticate with the Speech API using your project's
service account credentials.

Visit the [Cloud Console](https://console.cloud.google.com), and navigate to:
`API Manager > Credentials > Create credentials >
Service account key > New service account`.
Create a new service account, and download the json credentials file.

Then, set
the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your
downloaded service account credentials before running this example:

    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials-key.json

If you do not do this, you will see an error that looks something like this when
you run the example script:
`...<HttpError 403 when requesting https://speech.googleapis.com/v1/speech:recognize?alt=json returned "Request had insufficient authentication scopes.">`.
See the
[Cloud Platform Auth Guide](https://cloud.google.com/docs/authentication#developer_workflow)
for more information.

## Run the example

```sh
$ python speechrest.py resources/audio.raw
```

You should see a response with the transcription result.
