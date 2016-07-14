
# Google Cloud Speech API Samples

These examples demo accessing the [Google Cloud Speech API](http://cloud.google.com/speech)
in streaming mode (via its gRPC API) and in non-streaming mode (via its REST
API).

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

If you do not do this, the REST api will return a 403. The streaming sample will
just sort of hang silently.

See the
[Cloud Platform Auth Guide](https://cloud.google.com/docs/authentication#developer_workflow)
for more information.

### Download code

To download code or clone the repo go [here][home-page] and then navigate appropriately. 

### Install pip

Install [pip][pip] if not already installed

### Install virtualenv

Install [virtualenv][virtualenv] if not already installed

### Create isolated Python environment

```
virtualenv speechsamples
source speechsamples/bin/activate
```

### Install the dependencies

The sample uses the [PyAudio][pyaudio] library to stream audio from your computer's microphone.  PyAudio depends on [PortAudio][portaudio], which may need to be compiled when you install PyAudio. If you run into compilation issues that mention PortAudio, you may have to [install some dependencies][pyaudio-install].

* If you're running the `speech_rest.py` sample:

    ```sh
    $ pip install -r requirements-speech_rest.txt
    ```

* If you're running the `speech_streaming.py` sample:

    ```sh
    $ pip install -r requirements-speech_grpc.txt
    ```

[pyaudio]: https://people.csail.mit.edu/hubert/pyaudio/
[portaudio]: http://www.portaudio.com/
[pyaudio-install]: https://people.csail.mit.edu/hubert/pyaudio/#downloads
[pip]: https://pip.pypa.io/en/stable/installing/
[virtualenv]: https://virtualenv.pypa.io/en/stable/installation/
[home-page]: https://github.com/GoogleCloudPlatform/python-docs-samples

## Run the example

* To run the `speech_rest.py` sample:

    ```sh
    $ python speech_rest.py resources/audio.raw
    ```

    You should see a response with the transcription result.

* To run the `speech_async_rest.py` sample:

    ```sh
    $ python speech_async_rest.py resources/audio.raw
    ```

    You should see a response with the transcription result.

* To run the `speech_streaming.py` sample:

    ```sh
    $ python speech_streaming.py
    ```

    The sample will run in a continuous loop, printing the data and metadata
    it receives from the Speech API, which includes alternative transcriptions
    of what it hears, and a confidence score. Say "exit" to exit the loop.

    Note that the `speech_streaming.py` sample does not yet support python 3, as
    the upstream `grpcio` library's support is [not yet
    complete](https://github.com/grpc/grpc/issues/282).
    
### Deactivate virtualenv

```
deactivate
```
