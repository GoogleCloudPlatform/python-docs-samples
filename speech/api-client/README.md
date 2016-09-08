# Google Cloud Speech REST API Samples

These samples show how to use the [Google Cloud Speech API](http://cloud.google.com/speech)
to transcribe audio files, using the REST-based [Google API Client Library for
Python](https://developers.google.com/api-client-library/python/).

For samples that use the more-efficient [GRPC](http://grpc.io)-based client
library (including a streaming sample that transcribes audio streamed from your
microphone), see [../grpc/](../grpc/).

## Prerequisites

### Enable the Speech API

If you have not already done so, [enable the Google Cloud Speech
API][console-speech] for your project.

[console-speech]: https://console.cloud.google.com/apis/api/speech.googleapis.com/overview?project=_

### Authentication

These samples use service accounts for authentication.

* Visit the [Cloud Console][cloud-console], and navigate to:

    `API Manager > Credentials > Create credentials > Service account key > New
    service account`.
* Create a new service account, and download the json credentials file.
* Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your
  downloaded service account credentials:

      export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials-key.json

  If you do not do this, the REST api will return a 403.

See the [Cloud Platform Auth Guide][auth-guide] for more information.

[cloud-console]: https://console.cloud.google.com
[auth-guide]: https://cloud.google.com/docs/authentication#developer_workflow

### Setup

* Clone this repo

    ```sh
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    cd python-docs-samples/speech/api-client
    ```

* Create a [virtualenv][virtualenv]. This isolates the python dependencies
  you're about to install, to minimize conflicts with any existing libraries you
  might already have.

    ```sh
    virtualenv env
    source env/bin/activate
    ```

* Install the dependencies

    ```sh
    pip install -r requirements.txt
    ```

[pip]: https://pip.pypa.io/en/stable/installing/
[virtualenv]: https://virtualenv.pypa.io/en/stable/installation/

## Run the sample

Each of the samples takes the audio file to transcribe as the first argument.
For example:

```sh
python transcribe.py resources/audio.raw
```

You should see a response with the transcription result.

### Deactivate virtualenv

When you're done running the sample, you can exit your virtualenv:

```
deactivate
```
