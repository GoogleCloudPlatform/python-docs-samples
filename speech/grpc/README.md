# Google Cloud Speech GRPC API Samples

These samples show how to use the [Google Cloud Speech API][speech-api]
to transcribe audio files, as well as live audio from your computer's
microphone.

[speech-api]: http://cloud.google.com/speech

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

  If you do not do this, the streaming sample will just sort of hang silently.

See the [Cloud Platform Auth Guide][auth-guide] for more information.

[cloud-console]: https://console.cloud.google.com
[auth-guide]: https://cloud.google.com/docs/authentication#developer_workflow

### Setup

* Clone this repo

  ```sh
  git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
  cd python-docs-samples/speech/grpc
  ```
  
* If you don't have it already, install [virtualenv][virtualenv].

  ```sh
  pip install virtualenv
  ```

* Create a [virtualenv][virtualenv]. This isolates the python dependencies
  you're about to install, to minimize conflicts with any existing libraries you
  might already have.

  ```sh
  virtualenv env
  source env/bin/activate
  ```

* Install [PortAudio][portaudio]. The `transcribe_streaming.py` sample uses the
  [PyAudio][pyaudio] library to stream audio from your computer's
  microphone. PyAudio depends on PortAudio for cross-platform compatibility, and
  is installed differently depending on the platform. For example:

  * For Mac OS X, you can use [Homebrew][brew]:

    ```sh
    brew install portaudio
    ```

  * For Debian / Ubuntu Linux:

    ```sh
    apt-get install portaudio19-dev python-all-dev
    ```

  * Windows may work without having to install PortAudio explicitly (it will get
    installed with PyAudio, when you run `python -m pip install ...` below).

  * For more details, see the [PyAudio installation][pyaudio-install] page.

* Install the python dependencies:

    ```sh
    pip install -r requirements.txt
    ```

[pyaudio]: https://people.csail.mit.edu/hubert/pyaudio/
[portaudio]: http://www.portaudio.com/
[pyaudio-install]: https://people.csail.mit.edu/hubert/pyaudio/#downloads
[pip]: https://pip.pypa.io/en/stable/installing/
[virtualenv]: https://virtualenv.pypa.io/en/stable/installation/
[brew]: http://brew.sh

### Troubleshooting

#### PortAudio on OS X

If you see the error

    fatal error: 'portaudio.h' file not found

Try adding the following to your `~/.pydistutils.cfg` file,
substituting in your appropriate brew Cellar directory:

    include_dirs=/usr/local/Cellar/portaudio/19.20140130/include/
    library_dirs=/usr/local/$USER/homebrew/Cellar/portaudio/19.20140130/lib/

## Run the sample

* To run the `transcribe_streaming.py` sample:

    ```sh
    python transcribe_streaming.py
    ```

    The sample will run in a continuous loop, printing the data and metadata
    it receives from the Speech API, which includes alternative transcriptions
    of what it hears, and a confidence score. Say "exit" to exit the loop.

* To run the `transcribe_async.py` sample:

    ```sh
    $ python transcribe_async.py gs://python-docs-samples-tests/speech/audio.flac
    ```

    You should see a response with the transcription result.

* To run the `transcribe.py` sample:

    ```sh
    $ python transcribe.py gs://python-docs-samples-tests/speech/audio.flac
    ```

    You should see a response with the transcription result.

* Note that `gs://python-docs-samples-tests/speech/audio.flac` is the path to a
  sample audio file, and you can transcribe your own audio files using this
  method by uploading them to [Google Cloud Storage][gcs]. (The [gsutil][gsutil]
  tool is often used for this purpose.)

[gcs]: https://cloud.google.com/storage
[gsutil]: https://cloud.google.com/storage/docs/gsutil

### Deactivate virtualenv

When you're done running the sample, you can exit your virtualenv:

```
deactivate
```
