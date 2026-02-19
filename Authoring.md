# Python Sample Authoring Guide

The [Google Cloud Samples Style Guide][style-guide] is considered the primary
guidelines for all Google Cloud samples. This section details some additional,
Python-specific rules that will be merged into the Samples Style Guide in the
near future.

[style-guide]: https://googlecloudplatform.github.io/samples-style-guide/

We're happy you want to write a Python sample! Like a lot of Pythonistas, we're
opinionated and fussy. This guide is a reference for the format and style
expected of samples contributed to the
[python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
repo. The guidelines below are intended to ensure that all Python samples meet
the following goals:

* **Copy-paste-runnable.** A developer should be able to copy and paste the code
into their own environment and run it with as few modifications as possible.
* **Teach through code.** Each sample should demonstrate best practices for
interacting with Google Cloud libraries, APIs, or services.
* **Idiomatic.** Each sample should follow widely accepted Python best practices
as covered below.

## FAQs

### Are there any canonical samples?

We recommend referencing the following samples and sample tests:

* [Storage client
   samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/storage/cloud-client)

### Where should I put my samples?

See [Folder Location](#folder-location). Samples live in this repository,
**python-docs-samples**, or in a library repository.

### Where are the client libraries?

Python libraries repositories live in <https://github.com/googleapis/> in
repositories named **python-API**. Each repository contains _one_ library. For
example, <https://github.com/googleapis/python-bigquery> contains the
`google-cloud-bigquery` library.

### Who reviews my PR?

This is a work in progress - in **python-docs-samples**, your PR will
automatically be assigned to one of the reviewers in
[@GoogleCloudPlatform/python-samples-reviewers](https://github.com/orgs/GoogleCloudPlatform/teams/python-samples-reviewers).
You can assign a new person using the `blunderbuss:assign` label if your
assignee is OOO or busy. You can (and probably should) also assign a teammate in
addition to the auto-assigned owner to review your code for product-specific
needs.

In **library repositories** GitHub should automatically assign a reviewer from
python-samples-reviewers. If no reviewer is automatically assigned, contact
[@googleapis/python-samples-reviewers](https://github.com/orgs/googleapis/teams/python-samples-reviewers).

Please reach out to your assigned reviewer if it's been more than 2 days and you
haven't gotten a response!

### How do I set up my environment?

You should install the latest patch version of each minor version listed in
[Python Versions](#python-versions).

We recommend using the Python version management tool
[Pyenv](https://github.com/pyenv/pyenv) if you are using MacOS or Linux.

**Googlers:** See [the internal Python policies
doc](go/cloudsamples/language-guides/python).

**Using MacOS?:** See [Setting up a Mac development environment with pyenv and
pyenv-virtualenv](MAC_SETUP.md).

Afterwards, see [Test Environment Setup](#test-environment-setup).

## Sample Guidelines

This section covers guidelines for Python samples. Note that [Testing
Guidelines](#testing-guidelines) are covered separately below.

### Folder Location

**Library repositories:** Each sample should be in a folder under the top-level
samples folder `samples` in the client library repository. See the
[Text-to-Speech
samples](https://github.com/googleapis/python-texttospeech/tree/main/samples)
for an example.

**python-docs-samples:** Each sample should be in a folder under the top-level
folder of
[python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
that corresponds to the Google Cloud service or API used by the sample. For
example, a sample demonstrating how to work with Composer should be in a
subfolder under the
[python-docs-samples/composer](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/composer)
folder.

Conceptually related samples under a service or API should be grouped into a
subfolder. For example, App Engine Standard samples are under the
[appengine/standard](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/standard)
folder, and App Engine Flex samples are under the
[appengine/flexible](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/flexible)
folder.

If your sample is a quickstart — intended to demonstrate how to quickly get
started with using a service or API — it should be in a _quickstart_ folder.

### Python Versions

Samples should support Python 3.9, 3.10, 3.11, 3.12 and 3.13.

If the API or service your sample works with has specific Python version
requirements different from those mentioned above, the sample should support
those requirements.

### License Header

Source code files should always begin with an Apache 2.0 license header. See the
instructions in the repo license file on [how to apply the Apache license to
your
work](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/LICENSE#L178-L201).
For example, see the license header for the [Datastore client quickstart
sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/datastore/cloud-client/quickstart.py#L1-L15).

### Shebang

If, and only if, your sample application is a command-line application, then
include a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) as the first
line. Separate the shebang line from the rest of the application with a blank
line. The shebang line for a Python application should always be:

```python
#!/usr/bin/env python
```

Don't include shebang lines in web applications or test files.

### Coding Style

All Python samples should follow the best practices defined in the [PEP 8 style
guide](https://www.python.org/dev/peps/pep-0008/) and the [Google Python Style
Guide](http://google.github.io/styleguide/pyguide.html). The automated linting
process for Python samples uses [flake8](http://flake8.pycqa.org/en/latest/) to
verify conformance to common Python coding standards, so the use of flake8 is
recommended.

If you prefer to use [pylint](https://www.pylint.org/), note that Python samples
for this repo are not required to conform to pylint’s default settings outside
the scope of PEP 8, such as the “too many arguments” or “too many local
variables” warnings.

The use of [Black](https://pypi.org/project/black/) to standardize code
formatting and simplify diffs is recommended.

The default noxfile has `blacken` session for convenience. Here are some
examples.

If you have pyenv configured:

```sh
nox -s blacken
```

If you only have docker:

```sh
cd proj_directory
../scripts/run_tests_local.sh . blacken
```

Owlbot is an automated tool that will run the `blacken` session automatically on
new pull requests.

In addition to the syntax guidelines covered in PEP 8, samples should strive to
follow the Pythonic philosophy outlined in the [PEP 20 - Zen of
Python](https://www.python.org/dev/peps/pep-0020/) as well as the readability
tenets presented in Donald Knuth's _[Literate
Programming](https://en.wikipedia.org/wiki/Literate_programming)_. Notably, your
sample program should be self-contained, readable from top to bottom, and fairly
self-documenting. Prefer descriptive names, and use comments and docstrings only
as needed to further clarify the code’s intent. Always introduce functions and
variables before they are used. Prefer less indirection. Prefer imperative
programming as it is easier to understand.

### Importing Google Cloud Libraries

Follow this style for importing Google Cloud libraries:

```py
from google.cloud import texttospeech_v1
```

All commonly used clients and types are exposed under `texttospeech_v1`.

```py
from google.cloud import texttospeech_v1

client = texttospeech_v1.TextToSpeechClient()

audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
)
```

### Creating Request Objects for GAPICs

GAPIC libraries are generated from
[protos](https://github.com/googleapis/googleapis) that define the API surface
via a [generator](https://github.com/googleapis/gapic-generator-python). GAPIC
libraries have library type `GAPIC_AUTO` in `.repo-metadata.json` located in the
root of the repository. Some `GAPIC_COMBO` libraries will also expose
[`proto-plus`](https://github.com/googleapis/proto-plus-python/) types.

Because they are generated, GAPIC libraries share a common interface. All API
proto messages are exposed as `proto-plus` message classes.

`proto-plus` provides a [few ways to create
objects](https://proto-plus-python.readthedocs.io/en/latest/messages.html#usage).

Strongly prefer instantiating library types through the constructor or by
instantiating an empty object and initializing individual attributes. The
dictionary construction method is discouraged as it is harder to use type
checking and IDEs are not able to offer intellisense.

```py
# To try this sample yourself, install `google-cloud-tasks==2.5.1`
from google.cloud import tasks_v2


# 1. Generated types via constructor
task_from_constructor = tasks_v2.Task(
    http_request=tasks_v2.HttpRequest(
        http_method=tasks_v2.HttpMethod.POST,
        url="https://pubsub.googleapis.com/v1/projects/my-project/topics/testtopic:publish",
        body=b"eyJtZXNzYWdlcyI6IFt7ImRhdGEiOiAiVkdocGN5QnBjeUJoSUhSbGMzUUsifV19Cg==",
        oauth_token=tasks_v2.OAuthToken(
            service_account_email='my-svc-acct@my-project.iam.gserviceaccount.com'
        )
    )
)

# 2. Instantiate object and then set attributes
http_request = tasks_v2.HttpRequest()
http_request.http_method = tasks_v2.HttpMethod.POST
http_request.url = "https://pubsub.googleapis.com/v1/projects/my-project/topics/testtopic:publish"
http_request.body = b"eyJtZXNzYWdlcyI6IFt7ImRhdGEiOiAiVkdocGN5QnBjeUJoSUhSbGMzUUsifV19Cg==",
http_request.oauth_token.service_account_email = "my-svc-acct@my-project.iam.gserviceaccount.com"

task = tasks_v2.Task()
task.http_request = http_request

# 2. Dictionary (NOT RECOMMENDED)
task_from_dict = {
    "http_request": {
        "http_method": "POST",
        "url": "https://pubsub.googleapis.com/v1/projects/my-project/topics/testtopic:publish",
        "body": b"eyJtZXNzYWdlcyI6IFt7ImRhdGEiOiAiVkdocGN5QnBjeUJoSUhSbGMzUUsifV19Cg==",
        "oauth_token": {"service_account_email":"my-svc-acct@my-project.iam.gserviceaccount.com"},
    }
}
```

### Functions and Classes

Prefer functions over classes whenever possible. 

See [this video](https://www.youtube.com/watch?v=o9pEzgHorH0) for some
hints into practical refactoring examples where simpler functions lead to more
readable and maintainable code. 


#### Descriptive function names

Always prefer descriptive function names, even if they are long. For example
`upload_file`, `upload_encrypted_file`, and `list_resource_records`. Similarly,
prefer long and descriptive parameter names. For example `source_file_name`,
`dns_zone_name`, and `base64_encryption_key`.

Here's an example of a top-level function in a command-line application:

```python
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)
```

Notice the simple docstring and descriptive argument name (`bucket_name`
implying a string instead of just `bucket` which could imply a class instance).

This particular function is intended to be the "top of the stack" - the function
executed when the command-line sample is run by the user. As such, notice that
it prints the blobs instead of returning. In general, top of the stack functions
in command-line applications should print, but use your best judgment.

#### Documenting arguments

Here's an example of a more complicated top-level function in a command-line
application:

```python
def download_encrypted_blob(
        bucket_name, source_blob_name, destination_file_name,
        base64_encryption_key):
    """Downloads a previously-encrypted blob from Google Cloud Storage.

    The encryption key provided must be the same key provided when uploading
    the blob.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # Encryption key must be an AES256 key represented as a bytestring with
    # 32 bytes. Since it's passed in as a base64 encoded string, it needs
    # to be decoded.
    encryption_key = base64.b64decode(base64_encryption_key)

    blob.download_to_filename(
        destination_file_name, encryption_key=encryption_key)

    print(f'Blob {source_blob_name} downloaded to {destination_file_name}.'
```

Note the verbose parameter names and the extended description that helps the
user form context. If there were more parameters or if the parameters had
complex context, then it might make sense to expand the docstring to include an
`Args` section such as:

```
Args:
    bucket_name: The name of the cloud storage bucket.
    source_blob_name: The name of the blob in the bucket to download.
    destination_file_name: The blob will be downloaded to this path.
    base64_encryption_key: A base64-encoded RSA256 encryption key. Must be the
        same key used to encrypt the file.
```

Generally, however, it's rarely necessary to exhaustively document the
parameters this way. Lean towards unsurprising arguments with descriptive names,
as having to resort to this kind of docstring might be extremely accurate but it
comes at the cost of high redundancy, signal-to-noise ratio, and increased
cognitive load.

#### Documenting types

Argument types should be documented using Python type annotations as introduced
in [PEP 484](https://www.python.org/dev/peps/pep-0484/). For example:

```py
def hello_world(name: str) -> None:
    print(f"Hello {name}!")
```

```py
def adder(a: int, b: int) -> int:
    return a+b
```

Type hinting is enforced using
[`flake8-annotations`](https://pypi.org/project/flake8-annotations/), which is
enabled by setting the `enforce_type_hints` variable to `True` in the
appropriate `noxfile_config.py`. Type hinting is expected in all new samples,
and will gradually be added to all compatible existing samples.

If there is an `Args` section within the function's docstring, consider
documenting the argument types there as well. For example:

```
Args:
    credentials (google.oauth2.credentials.Credentials): Credentials
      authorized for the current user.
```

When documenting primitive types, be sure to note if they have a particular set
of constraints. For example, `A base64-encoded string` or `Must be between 0 and
10`.

### `datetime.datetime` Objects

Always create timezone aware datetime objects. For libraries that use protobuf,
omitting the timezone may lead to unexpected behavior when the datetime is
converted to a protobuf timestamp.

```py
import datetime

now = datetime.datetime.now(tz=datetime.timezone.utc)
```

For more information see the [Python datetime
documentation](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcfromtimestamp).

### README File

Each sample should have a `README.md` file that provides instructions for how to
install, configure, and run the sample. Setup steps that cover creating Google
Cloud projects and resources should link to appropriate pages in the [Google
Cloud Documentation](https://cloud.google.com/docs/), to avoid duplication and
simplify maintenance.

### Dependencies

Every sample should include a
[requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
file that lists all of its dependencies, to enable others to re-create the
environment that was used to create and test the sample. All dependencies should
be pinned to a specific version, as in this example:

```
Flask==1.1.1
PyMySQL==0.9.3
SQLAlchemy==1.3.12
```

If a sample has testing requirements that differ from its runtime requirements
(such as dependencies on [pytest](http://pytest.org/en/latest/) or other testing
libraries), the testing requirements may be listed in a separate
`requirements-test.txt` file instead of the main `requirements.txt` file.

#### Developing samples for un-released changes

Pip has [VCS
support](https://pip.pypa.io/en/stable/cli/pip_install/#vcs-support). Use the
branch name or commit hash instead of the package name.

**pip install**:

```
pip install git+https://github.com/googleapis/python-firestore.git@ee518b741eb5d7167393c23baa1e29ace861b253
```

**requirements.txt**:

```
Flask==1.1.1
PyMySQL==0.9.3
git+https://github.com/googleapis/python-firestore.git@ee518b741eb5d7167393c23baa1e29ace861b253
```

### Region Tags

Region tags are comments added to the source code that begin with 
`[START region_tag]` and end with `[END region_tag]`. They enclose 
the core sample logic that can be easily copied into a REPL and run.

This allows us to integrate this copy-paste callable code into 
documentation directly. Region tags should be placed after the 
license header but before imports that are crucial to the 
sample running. 

Example:
```python
# This import is not included within the region tag as
# it is used to make the sample command-line runnable
import sys

# [START example_storage_control_create_folder]
# This import is included within the region tag
# as it is critical to understanding the sample
from google.cloud import storage_control_v2


def create_folder(bucket_name: str, folder_name: str) -> None:
    print(f"Created folder: {response.name}")


# [END example_storage_control_create_folder]
```

### Exception Handling

Sample code should use standard Python exception handling techniques as covered
in the [Google Python Style
Guide](http://google.github.io/styleguide/pyguide.html#24-exceptions).

## Testing Guidelines

Samples should include tests to verify that the sample runs correctly and
generates the intended output. Follow these guidelines while writing your tests:

* Use [pytest](https://docs.pytest.org/en/latest/)-style tests and plain
asserts. Don't use `unittest`-style tests or `assertX` methods.
* Whenever possible, tests should allow for future changes or additions to APIs
that are unrelated to the code being tested. For example, if a test is intended
to verify a JSON payload returned from an endpoint, it should only check for the
existence of the expected keys and values, and the test should continue to work
correctly if the order of keys changes or new keys are added to the response in
a future version of the API. In some cases, it may make sense for tests to
simply verify that an API call was successful rather than checking the response
payload.
* Samples that use App Engine Standard should use the [App Engine
testbed](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.testbed)
for system testing, as shown in [this
example](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/appengine/standard/localtesting/datastore_test.py).
* All tests should be independent of one another and order-independent.
* We use parallel processing for tests, so tests should be capable of running in
  parallel with one another.
* Use pytest's fixture for resource setup and teardown, instead of having them
  in the test itself.
* Avoid infinite loops.
* Retry RPCs
* You can enable running tests in parallel by adding `pytest-parallel` or
  `pytest-xdist` to your `requirements-test.txt` file.

### Arrange, Act, Assert

Tests for samples should follow the “Arrange, Act, Assert” structure:

* _Arrange_ — create and configure the components required for the test. Avoid
nesting; prioritize readability and simplicity over efficiency. For Python
tests, typical "arrange" steps inclu
