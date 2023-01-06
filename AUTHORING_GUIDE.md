# Python Sample Authoring Guide

The [Google Cloud Samples Style Guide][style-guide] is considered the primary
guidelines for all Google Cloud samples. This section details some additional,
Python-specific rules that will be merged into the Samples Style Guide in the 
near future. 

[style-guide]: https://googlecloudplatform.github.io/samples-style-guide/

We're happy you want to write a Python sample! Like a lot of Pythonistas,
we're opinionated and fussy. This guide is a reference for the format and
style expected of samples contributed to the
[python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
repo. The guidelines below are intended to ensure that all Python samples
meet the following goals:

* **Copy-paste-runnable.** A developer should be able to copy and paste the
code into their own environment and run it with as few modifications as
possible.
* **Teach through code.** Each sample should demonstrate best practices for
interacting with Google Cloud libraries, APIs, or services.
* **Idiomatic.** Each sample should follow widely accepted Python best
practices as covered below.


## FAQs

### Are there any canonical samples?

We recommend referencing the following samples and sample tests:

 * [Storage client samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/storage/cloud-client)

### Where should I put my samples?

See [Folder Location](#folder-location). Samples live in this repository, **python-docs-samples**,
or in a library repository.

### Where are the client libraries?

Python libraries repositories live in https://github.com/googleapis/ in repositories named **python-API**.
Each repository contains _one_ library. For example, https://github.com/googleapis/python-bigquery
contains the `google-cloud-bigquery` library.

### Who reviews my PR?

This is a work in progress - in **python-docs-samples**, your PR will
automatically be assigned to one of the reviewers in [@GoogleCloudPlatform/python-samples-reviewers](https://github.com/orgs/GoogleCloudPlatform/teams/python-samples-reviewers).
You can assign a new person using the `blunderbuss:assign` label if your assignee is OOO or busy.
You can (and probably should) also assign a teammate in addition to the auto-assigned
owner to review your code for product-specific needs.

In **library repositories** GitHub should automatically assign a reviewer
from python-samples-reviewers. If no reviewer is automatically assigned, contact [@googleapis/python-samples-reviewers](https://github.com/orgs/googleapis/teams/python-samples-reviewers).

Please reach out to your assigned reviewer if it's been more than 2 days and you haven't gotten a response!

### How do I set up my environment?

You should install the latest patch version of each minor version listed in [Python Versions](#python-versions).

We recommend using the Python version management tool [Pyenv](https://github.com/pyenv/pyenv) if you are using MacOS or Linux.

**Googlers:** See [the internal Python policies doc](https://g3doc.corp.google.com/company/teams/cloud-devrel/dpe/samples/python.md?cl=head).

**Using MacOS?:** See [Setting up a Mac development environment with pyenv and pyenv-virtualenv](MAC_SETUP.md).

Afterwards, see [Test Environment Setup](#test-environment-setup).


## Sample Guidelines

This section covers guidelines for Python samples. Note that
[Testing Guidelines](#testing-guidelines) are covered separately below.

### Folder Location

Samples that primarily show the use of one client library should be placed in the
client library repository `googleapis/python-{api}`. Other samples should be placed in this repository
`python-docs-samples`.

**Library repositories:** Each sample should be in a folder under the top-level samples folder `samples`
in the client library repository. See the [Text-to-Speech samples](https://github.com/googleapis/python-texttospeech/tree/main/samples)
for an example.

**python-docs-samples:** Each sample should be in a folder under the top-level folder of
[python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
that corresponds to the Google Cloud service or API used by the sample.
For example, a sample demonstrating how to work with Composer should be
in a subfolder under the
[python-docs-samples/composer](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/composer)
folder.

Conceptually related samples under a service or API should be grouped into
a subfolder. For example, App Engine Standard samples are under the
[appengine/standard](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/standard)
folder, and App Engine Flex samples are under the
[appengine/flexible](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/flexible)
folder.

If your sample is a set of discrete code snippets that each demonstrate a
single operation, these should be grouped into a `snippets` folder. For
example, see the snippets in the
[bigtable/snippets/writes](https://github.com/googleapis/python-bigtable/tree/main/samples/snippets/writes)
folder.

If your sample is a quickstart — intended to demonstrate how to quickly get
started with using a service or API — it should be in a _quickstart_ folder.

### Python Versions

Samples should support Python 3.6, 3.7, 3.8, and 3.9.

If the API or service your sample works with has specific Python version
requirements different from those mentioned above, the sample should support
those requirements.

### License Header

Source code files should always begin with an Apache 2.0 license header. See
the instructions in the repo license file on [how to apply the Apache license
to your work](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/LICENSE#L178-L201).
For example, see the license header for the [Datastore client quickstart
sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/datastore/cloud-client/quickstart.py#L1-L15).

### Shebang

If, and only if, your sample application is a command-line application, then
include a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) as the
first line. Separate the shebang line from the rest of the application with
a blank line. The shebang line for a Python application should always be:

```python
#!/usr/bin/env python
```

Don't include shebang lines in web applications or test files.

### Coding Style

All Python samples should follow the best practices defined in the
[PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/) and the
[Google Python Style Guide](http://google.github.io/styleguide/pyguide.html).
The automated linting process for Python samples uses
[flake8](http://flake8.pycqa.org/en/latest/) to verify conformance to common
Python coding standards, so the use of flake8 is recommended.

If you prefer to use [pylint](https://www.pylint.org/), note that Python
samples for this repo are not required to conform to pylint’s default settings
outside the scope of PEP 8, such as the “too many arguments” or “too many
local variables” warnings.

The use of [Black](https://pypi.org/project/black/) to standardize code
formatting and simplify diffs is recommended, but optional.

The default noxfile has `blacken` session for convenience. Here are
some examples.

If you have pyenv configured:
```sh
nox -s blacken
```

If you only have docker:
```
cd proj_directory
../scripts/run_tests_local.sh . blacken
```

In addition to the syntax guidelines covered in PEP 8, samples should strive
to follow the Pythonic philosophy outlined in the
[PEP 20 - Zen of Python](https://www.python.org/dev/peps/pep-0020/) as well
as the readability tenets presented in Donald Knuth's
_[Literate Programming](https://en.wikipedia.org/wiki/Literate_programming)_.
Notably, your sample program should be self-contained, readable from top to
bottom, and fairly self-documenting. Prefer descriptive names, and use
comments and docstrings only as needed to further clarify the code’s intent.
Always introduce functions and variables before they are used. Prefer less
indirection. Prefer imperative programming as it is easier to understand.


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

GAPIC libraries are generated from [protos](https://github.com/googleapis/googleapis)
that define the API surface via a [generator](https://github.com/googleapis/gapic-generator-python).
GAPIC libraries have library type `GAPIC_AUTO` in `.repo-metadata.json`
located in the root of the repository. Some `GAPIC_COMBO` libraries will
also expose [`proto-plus`](https://github.com/googleapis/proto-plus-python/) types.

Because they are generated, GAPIC libraries share a common interface.
All API proto messages are exposed as `proto-plus` message classes.

`proto-plus` provides a [few ways to create objects](https://proto-plus-python.readthedocs.io/en/latest/messages.html#usage).

Strongly prefer instantiating library types through the constructor
or by instantiating an empty object and initializing individual attributes.
The dictionary construction method is discouraged as it is harder to use
type checking and IDEs are not able to offer intellisense.

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

Very few samples will require authoring classes. Prefer functions whenever
possible. See [this video](https://www.youtube.com/watch?v=o9pEzgHorH0) for
some insight into why classes aren't as necessary as you might think in Python.
Classes also introduce cognitive load. If you do write a class in a sample, be
prepared to justify its existence during code review.

#### Descriptive function names

Always prefer descriptive function names, even if they are long.
For example `upload_file`, `upload_encrypted_file`, and `list_resource_records`.
Similarly, prefer long and descriptive parameter names. For example
`source_file_name`, `dns_zone_name`, and `base64_encryption_key`.

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
it prints the blobs instead of returning. In general, top of the stack
functions in command-line applications should print, but use your best
judgment.

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
complex context, then it might make sense to expand the docstring to include
an `Args` section such as:

```
Args:
    bucket_name: The name of the cloud storage bucket.
    source_blob_name: The name of the blob in the bucket to download.
    destination_file_name: The blob will be downloaded to this path.
    base64_encryption_key: A base64-encoded RSA256 encryption key. Must be the
        same key used to encrypt the file.
```

Generally, however, it's rarely necessary to exhaustively document the
parameters this way. Lean towards unsurprising arguments with descriptive
names, as having to resort to this kind of docstring might be extremely
accurate but it comes at the cost of high redundancy, signal-to-noise ratio,
and increased cognitive load.

#### Documenting types

Argument types should be documented using Python type annotations as
introduced in [PEP 484](https://www.python.org/dev/peps/pep-0484/). For example:

```py
def hello_world(name: str) -> None:
    print(f"Hello {name}!")
```

```py
def adder(a: int, b: int) -> int:
    return a+b
```

Type hinting is enforced using [`flake8-annotations`](https://pypi.org/project/flake8-annotations/), which is enabled by setting the `enforce_type_hints` variable to `True` in the appropriate `noxfile_config.py`. Type hinting is expected in all new samples, and will gradually be added to all compatible existing samples.

If there is an `Args` section within the function's docstring, consider
documenting the argument types there as well. For example:

```
Args:
    credentials (google.oauth2.credentials.Credentials): Credentials
      authorized for the current user.
```

When documenting primitive types, be sure to note if they have a particular set
of constraints. For example, `A base64-encoded string` or `Must be between 0
and 10`.

### `datetime.datetime` Objects

Always create timezone aware datetime objects. For libraries that use protobuf,
omitting the timezone may lead to unexpected behavior when the datetime
is converted to a protobuf timestamp.

```py
import datetime

now = datetime.datetime.now(tz=datetime.timezone.utc)
```

For more information see the [Python datetime documentation](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcfromtimestamp).

### README File

Each sample should have a `README.md` file that provides instructions for how
to install, configure, and run the sample. Setup steps that cover creating
Google Cloud projects and resources should link to appropriate pages in the
[Google Cloud Documentation](https://cloud.google.com/docs/), to avoid
duplication and simplify maintenance.

### Dependencies

Every sample should include a
[requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
file that lists all of its dependencies, to enable others to re-create the
environment that was used to create and test the sample. All dependencies
should be pinned to a specific version, as in this example:

```
Flask==1.1.1
PyMySQL==0.9.3
SQLAlchemy==1.3.12
```

If a sample has testing requirements that differ from its runtime requirements
(such as dependencies on [pytest](http://pytest.org/en/latest/) or other
testing libraries), the testing requirements may be listed in a separate
`requirements-test.txt` file instead of the main `requirements.txt` file.

#### Developing samples for un-released changes

Pip has [VCS support](https://pip.pypa.io/en/stable/cli/pip_install/#vcs-support). Use the branch name or commit hash instead of the package name.


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

Sample code may be integrated into Google Cloud Documentation through the use
of region tags, which are comments added to the source code to identify code
blocks that correspond to specific topics covered in the documentation. For
example, see
[this sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/mysql/sqlalchemy/main.py)
— the region tags are the comments that begin with `[START` or `[END`.

The use of region tags is beyond the scope of this document, but if you’re
using region tags they should start after the source code header
(license/copyright information), but before imports and global configuration such as
initializing constants.

### Exception Handling

Sample code should use standard Python exception handling techniques as
covered in the [Google Python Style
Guide](http://google.github.io/styleguide/pyguide.html#24-exceptions).

## Testing Guidelines

Samples should include tests to verify that the sample runs correctly and
generates the intended output. Follow these guidelines while writing your
tests:

* Use [pytest](https://docs.pytest.org/en/latest/)-style tests and plain
asserts. Don't use `unittest`-style tests or `assertX` methods.
* Whenever possible, tests should allow for future changes or additions to
APIs that are unrelated to the code being tested.
For example, if a test is intended to verify a JSON payload
returned from an endpoint, it should only check for the existence of the
expected keys and values, and the test should continue to work correctly
if the order of keys changes or new keys are added to the response in a future
version of the API. In some cases, it may make sense for tests to simply
verify that an API call was successful rather than checking the response
payload.
* Samples that use App Engine Standard should use the [App Engine
testbed](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.testbed)
for system testing, as shown in [this
example](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/appengine/standard/localtesting/datastore_test.py).
* All tests should be independent of one another and order-independent.
* We use parallel processing for tests, so tests should be capable of running in parallel with one another.
* Use pytest's fixture for resource setup and teardown, instead of
  having them in the test itself.
* Avoid infinite loops.
* Retry RPCs
* You can enable running tests in parallel by adding `pytest-parallel` or `pytest-xdist`
  to your `requirements-test.txt` file.

### Arrange, Act, Assert

Tests for samples should follow the “Arrange, Act, Assert” structure:

* _Arrange_ — create and configure the components required for the test.
Avoid nesting; prioritize readability and simplicity over efficiency. For
Python tests, typical "arrange" steps include imports, copying environment
variables to local variables, and so on.
* _Act_ — execute the code to be tested, such as sending a request to an API and
receiving a response.
* _Assert_ — verify that the test results match what is expected, using an
`assert` statement.

### External Resources

Whenever possible, tests should run against the live production version of
cloud APIs and resources. This will assure that any breaking changes in those
resources are identified by the tests.

External resources that must exist prior to the test (for example, a
Cloud SQL instance) should be identified and passed in through an environment
variable. If specific data needs to exist within such infrastructure resources,
however, the test should create this data as part of its _Arrange_ steps and
then clean up when the test is completed.

Creating mocks for external resources is strongly discouraged. Tests should
verify the validity of the sample against the APIs, and not against a mock
that embodies assumptions about the behavior of the APIs.

### Temporary Resources

When tests need temporary resources (such as a temp file or folder), they
should create reasonable names for these resources with a UUID attached to
assure uniqueness. Use the Python ```uuid``` package from the standard
library to generate UUIDs for resource names. For example:

```python
glossary_id = f'test-glossary-{uuid.uuid4()}'
```

or:

```python
# If full uuid4 is too long, use its hex representation.
encrypted_disk_name = f'test-disk-{uuid.uuid4().hex}'
```

```python
# If the hex representation is also too long, slice it.
encrypted_disk_name = f'test-disk-{uuid.uuid4().hex[:5]}'
```

All temporary resources should be explicitly deleted when testing is
complete. Use pytest's fixture for cleaning up these resouces instead
of doing it in test itself.

We recommend using `finally` to ensure that resource deletion occurs even if there is an error on creation. For example, this fixture creates a Dataproc cluster and tears it down regardless of errors during creation.

```python
@pytest.fixture(scope="function")
def setup_and_teardown_cluster():
    try:
        # Create cluster using cluster client
        cluster_client = dataproc.ClusterControllerClient(
            client_options={
                "api_endpoint": f"{CLUSTER_REGION}-dataproc.googleapis.com:443"
            }
        )

        operation = cluster_client.create_cluster(
            project_id=PROJECT_ID, region=CLUSTER_REGION, cluster=CLUSTER_CONFIG
        )

        # Wait for cluster to provision
        operation.result()

        yield
    finally:
        try:
            # Delete cluster
            operation = cluster_client.delete_cluster(
                project_id=PROJECT_ID, region=CLUSTER_REGION, cluster_name=DATAPROC_CLUSTER
            )
            operation.result()
        except NotFound:
            print("Cluster already deleted")
```

### Console Output

If the sample prints output to the console, the test should capture stdout to
a file and verify that the captured output contains the key information that
is expected. Strive to verify the content of the output rather than the syntax.
For example, the test might verify that a string is included in the output,
without taking a dependency on where that string occurs in the output.

### Avoid infinite loops

Never put potential infinite loops in the test code path. A typical
example is about gRPC's LongRunningOperations. Make sure you pass the
timeout parameter to the `result()` call.

Good:

```python
# will raise google.api_core.GoogleAPICallError after 60 seconds
operation.result(60)
```

Bad:

```python
operation.result()  # this could wait forever.
```

We recommend the timeout parameter to be around the number that gives
you more than 90% success rate. Don't put too long a timeout.

Now this test is inevitably flaky, so consider marking the test as
`flaky` as follows:

```python

@pytest.mark.flaky(max_runs=3, min_passes=1)
def my_flaky_test():
    # test that involves LRO poling with the timeout
```

This combination will give you very high success rate with fixed test
execution time (0.999 success rate and 180 seconds operation wait time
in the worst case in this example).

### Retry RPCs

All the RPCs are inevitably flaky. It can fail for many reasons. The
`google-cloud` Python client retries requests automatically for most
cases.

The old api-client doesn't retry automatically, so consider using
[`backoff`](https://pypi.org/project/backoff/) for retrying. Here is a
simple example:

```python

import backoff
from googleapiclient.errors import HttpError

@pytest.fixture(scope='module')
def test_resource():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create_resource():
        try:
            return client.projects().imaginaryResource().create(
                name=resource_id, body=body).execute()
        except HttpError as e:
            if '409' in str(e):
                # Ignore this case and get the existing one.
                return client.projects().imaginaryResource().get(
                    name=resource_id).execute()
            else:
                raise

    resource = create_resource()

    yield resource

    # cleanup
    ...
```

### Use filters with list methods

When writing a test for a `list` method, consider filtering the possible results.
Listing all resources in the test project may take a considerable amount of time.
The exact way to do this depends on the API.

Some `list` methods take a `filter`/`filter_` parameter:

```python
from datetime import datetime

from google.cloud import logging_v2

client = logging_v2.LoggingServiceV2Client()
resource_names = [f"projects/{project}"]
   # We add timestamp for making the query faster.
    now = datetime.datetime.now(datetime.timezone.utc)
    filter_date = now - datetime.timedelta(minutes=1)
    filters = (
        f"timestamp>=\"{filter_date.isoformat('T')}\" "
        "resource.type=cloud_run_revision "
        "AND severity=NOTICE "
)

entries = client.list_log_entries(resource_names, filter_=filters)

```

Others allow you to limit the result set with additional arguments
to the request:

```python
from google.cloud import asset_v1p5beta1

# TODO project_id = 'Your Google Cloud Project ID'
# TODO asset_types = 'Your asset type list, e.g.,
# ["storage.googleapis.com/Bucket","bigquery.googleapis.com/Table"]'
# TODO page_size = 'Num of assets in one page, which must be between 1 and
# 1000 (both inclusively)'

project_resource = "projects/{}".format(project_id)
content_type = asset_v1p5beta1.ContentType.RESOURCE
client = asset_v1p5beta1.AssetServiceClient()

# Call ListAssets v1p5beta1 to list assets.
response = client.list_assets(
    request={
        "parent": project_resource,
        "read_time": None,
        "asset_types": asset_types,
        "content_type": content_type,
        "page_size": page_size,
    }
)
```

### Test Environment Setup

Because all tests are system tests that use live resources, running tests
requires a Google Cloud project with billing enabled, as covered under
[Creating and Managing Projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

Once you have your project created and configured, you'll need to set
environment variables to identify the project and resources to be used
by tests. See
[testing/test-env.tmpl.sh](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/testing/test-env.tmpl.sh)
for a list of all environment variables that must be set manually. Not every
test needs all of these variables. All required environment variables
are listed in `testing/test-env.tmpl.sh`. If you need to add a new secret,
follow instructions in [Secrets](#secrets).

We suggest that you copy this file as follows:

```sh
$ cp testing/test-env.tmpl.sh testing/test-env.sh
$ editor testing/test-env.sh  # change the value of `GOOGLE_CLOUD_PROJECT`.
```

You can easily `source` this file for exporting the environment variables.

#### Development environment setup

This repository supports two ways to run tests locally.

1. nox

    This is the recommended way. Setup takes little more efforts than
    the second one, but the test execution will be faster.

2. Docker

    This is another way of running the tests. Setup is easier because
    you only need to instal Docker. The test execution will be bit
    slower than the first one. This option is also useful if you need
    to simulate the CI system.


### Running tests with nox

Automated testing for samples is managed by
[nox](https://nox.readthedocs.io). Nox allows us to run a variety of tests,
including the flake8 linter, Python 2.7, Python 3.x, and App Engine tests,
as well as automated README generation.

Sample tests are run through [pytest](https://pytest.org). Do not use
[unittest](https://docs.python.org/3/library/unittest.html).

__Note:__

**Library repositories:** If you are working on an existing project (meaning that a `samples` directory already exists), a `noxfile.py` will already exist within that `samples` directory.

For new samples, create a new `noxfile.py` and paste the contents of
[noxfile-template.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/noxfile-template.py). Note - there may be a `noxfile.py` in the repo already in the root directory, but this is used for testing the libraries, not the samples, so you will still need to make a samples noxfile.

**python-docs-samples:** As a temporary workaround, each project currently uses first
`noxfile-template.py` found in a parent folder above the current sample. In
order to simulate this locally, you need to copy + rename the parent
`noxfile-template.py` as `noxfile.py` in the folder of the project (containing the `requirements.txt` for the file).

```console
cd python-docs-samples
cp noxfile-template.py PATH/TO/YOUR/PROJECT/noxfile.py
cd PATH/TO/YOUR/PROJECT/
```

ℹ️ **Note:** Nox only detects tests in the `tests` directory where the `noxfile_config.py` file is or [for any files named `*_test.py` or `test_*.py`](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/6c4c8de274496300e3285168a012f8b6203b5122/noxfile-template.py#L182-L187) in the same directory as the config file.

To use nox, install it globally with `pip`:

```console
$ pip install nox
```

To run style checks on your samples:
```console
nox -s lint
```

To run tests with a python version, use the correct `py-3.*` sessions:
```console
nox -s py-3.6
```

To run a specific file:
```console
nox -s py-3.7 -- snippets_test.py
```

To run a specific test from a specific following:
```console
nox -s py-3.7 -- snippets_test.py:test_list_blobs
```

#### `noxfile_config.py`

The [`noxfile_config.py`](noxfile_config.py) allows for customization
of some options:

* Ignore specific Python versions.
* Enforce type hints.
* Specify a different Google Cloud Project.
* Add additional environment variables. Also see [Environment Variables](#environment-variables).
* Override the version of `pip` used by nox

Options are documented inside the [noxfile_config.py](noxfile_config.py).


### Running tests with Docker

__Note__: This is currently only available for samples in `python-docs-samples`.

If you have [Docker](https://www.docker.com) installed and runnable by
the local user, you can use `scripts/run_tests_local.sh` helper script
to run the tests. For example, let's say you want to modify the code
in `cdn` directory, then you can do:

```sh
$ cd cdn
$ ../scripts/run_tests_local.sh .
# This will run the default sessions; lint, py-3.6, and py-3.7
$ ../scripts/run_tests_local.sh . lint
# Running only lint
```

If your test needs a service account, you have to create a service
account and download the JSON key to `testing/service-account.json`.

On MacOS systems, you also need to install `coreutils` to use
`scripts/run_tests_local.sh`. Here is how to install it with `brew`:

```sh
$ brew install coreutils
```

### Environment Variables and Secrets

This section explains how to set environment variables that are needed
by tests.


#### Environment Variables

If a `noxfile_config.py` does not exist, copy [`noxfile_config.py`](noxfile_config.py)
into the directory.

Add the new environment variables to the `envs` dictionary.

```py
TEST_CONFIG_OVERRIDE = {
    # You can opt out specific Python versions from the test.
    # To save resources, please consider testing 2 versions at most.
    # Test min and max supported versions which are python 3.7 and 3.11
    # Ignoring python 2.7 which is no longer supported.
    "ignored_versions": ["2.7", "3.8", "3.9", "3.10"],
    # Old samples are opted out of enforcing Python type hints
    # All new samples should feature them
    "enforce_type_hints": True,
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    "gcloud_project_env": "GOOGLE_CLOUD_PROJECT",
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {"DJANGO_SETTINGS_MODULE": "mysite.settings"},
}
```


#### Secrets

For setting up a local test environment, see [Test Environment Setup](#test-environment-setup).

Secrets (e.g., project names, API keys, passwords) are kept in
Cloud Secret Manager. See [python-docs-samples-test-env](https://console.cloud.google.com/security/secret-manager/secret/python-docs-samples-test-env/versions?project=cloud-devrel-kokoro-resources).
If you are unable to access the link, reach out to your assigned pull
request reviewer or someone in [@GoogleCloudPlatform/python-samples-reviewers](https://github.com/orgs/GoogleCloudPlatform/teams/python-samples-reviewers)
for assistance.

1. Add the new environment variable to [`testing/test-env.tmpl.sh`](testing/test-env.tmpl.sh)
   in your pull request.
2. Run [`scripts/decrypt-secrets.sh`](scripts/decrypt-secrets.sh)
   to fetch the secrets. A new file `testing/test-env.sh` will appear.
3. Add the new environment variable to `testing/test-env.sh`.
4. Run [`scripts/encrypt-secrets.sh`](scripts/encrypt-secrets.sh)
   to upload the secrets to secret manager.



### Google Cloud Storage Resources

Certain samples require integration with Google Cloud Storage (GCS), most
commonly for APIs that read files from GCS. To run the tests for these
samples, configure your GCS bucket name via the `CLOUD_STORAGE_BUCKET`
environment variable.

The resources required by tests can usually be found in the `./resources`
folder inside the `samples/snippets` directory in client libraries, as in
[this example](https://github.com/googleapis/python-automl/tree/main/samples/snippets/resources).
You can upload those resources to your own GCS bucket to run the tests with
[gsutil](https://cloud.google.com/storage/docs/gsutil). For example:

```console
gsutil cp ./samples/snippets/resources/* gs://{$CLOUD_STORAGE_BUCKET}/
```

## Debugging

### Can I use a debugger for samples?

Yes, you can use `pdb` or any Python debugger. For pdb, use `import pdb; pdb.set_trace()` (<3.7) or `breakpoint` (3.7+).
See https://docs.python.org/3/library/pdb.html.

### How do I do that in IntelliJ, VSCode, etc.?

These IDEs just inject the breakpoint above into the code, so it should work.
