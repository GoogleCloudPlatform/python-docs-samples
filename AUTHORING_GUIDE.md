# Python Sample Authoring Guide

We're happy you want to write a Python sample! Like a lot of Pythonistas, we're
opinationed and fussy. This guide intends to be a reference for the format and
style expected of samples that live in
[python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples).

## Canonical sample

The [Cloud Storage Sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py)
is a great example of what we expect from samples. It's a great sample to copy
and start from.

## The basics

No matter what, all samples must:

1. Have a license header.
1. Pass lint.
1. Be either a web application or a runnable console application.
1. Have a `requirements.txt` containing all of its third-party dependencies.
1. Work in Python 2.7, 3.5, & 3.6. App Engine Standard is exempt as it
   only supports 2.7. Our default version is currently Python 3.5.
1. Have tests.
1. Declare all dependencies in a `requirements.txt`. All requirements must
  be pinned.

## Style & linting

We follow [pep8](https://www.python.org/dev/peps/pep-0008/) and the
*external* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
we verify this with [flake8](https://pypi.python.org/pypi/flake8). In general:

1.  4 spaces.
1.  `CamelCase` only for classes, `snake_case` elsewhere.
1.  `_` for private variables, members, functions, and methods only. Samples
  should generally have very few private items.
1.  `CAP_WITH_UNDERSCORES` for constants.
1.  `mixedCase` is only acceptable when interface with code that doesn't follow
  our style guide.
1.  79-character line limit.
1.  Imports should be in three sections separated by a blank line - standard
    library, third-party, and package-local. Sample will have very few
    package-local imports.

See [Automated tools](#automated-tools) for information on how to run the lint
checker.

Beyond PEP8, there are several idioms and style nits we prefer.

1. Use single quotes (`'`) except for docstrings (which use `"""`).
1. Typically import modules over members, for example
   `from gcloud import datastore`
   instead of `from gcloud.datastore import Client`. Although you should use
   your best judgment, for example
   `from oauth2client.contrib.flask_util import UserOAuth2`
   and `from oauth2client.client import GoogleCredentials` are both totally
   fine.
1. Never alias imports unless there is a name collision.
1. Use `.format()` over `%` for string interpolation.
1. Generally put a blank line above control statements that start new indented
   blocks, for example:

    ```python
    # Good
    do_stuff()

    if other_stuff():
        more_stuff()

    # Not so good
    do_stuff()
    if other_stuff():
        more_stuff()
    ```

   This rule can be relaxed for counter or accumulation variables used in loops.
1. Don't use parenthesis on multiple return values (`return one, two`) or in
   destructuring assignment (`one, two = some_function()`).
2. Prefer not to do hanging indents if possible. If you break at the first
   logical grouping, it shouldn't be necessary. For example:

    ```python
    # Good
    do_some_stuff_please(
        a_parameter, another_parameter, wow_so_many_parameters,
        much_parameter, very_function)

    # Not so good
    do_some_stuff_please(a_parameter, another_parameter, wow_so_many_parameters,
                         much_parameter, very_function)
    ```

   Similarly with strings and other such things:

    ```python
    long_string = (
        'Alice was beginning to get very tired of sitting by her sister on '
        'the bank, and of having nothing to do: once or twice she had peeped '
        'into the book her sister was reading, but it had no pictures or ...'
    )
    ```
1. Use descriptive variables names in comprehensions, for example:

    ```python
    # Good
    blogs = [blog for blog in bob_laws_law_blog]

    # Not so good
    blogs = [x for x in bob_laws_law_blog]
    ```

## The sample format

In general our sample format follows ideas borrowed from
[Literate Programming](https://en.wikipedia.org/wiki/Literate_programming).
Notably, your sample program should self-contained, readable from top to bottom,
and should be fairly self-documenting. Prefer descriptive names. Use comments
and docstrings only as needed to further explain. Always introduce functions and
variables before they are used. Prefer less indirection. Prefer imperative
programming as it is easier to understand.

### Shebang

If, and only if, your sample application is a command-line application then
include a shebang as the first line. Separate the shebang from the rest of
the application with a blank line. The shebang should always be:

```python
#!/usr/bin/env python
```

Don't include shebangs in web applications or test files.

### License header

All samples should start with the following (modulo shebang line):

```
# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

### Module-level docstring

All samples should contain a module-level docstring. For command-line
applications, this docstring will be used as the summary when `-h` is passed.
The docstring should be succinct and should avoid repeating information
available in readmes or documentation.

Here's a simple docstring for a command-line application with straightforward
usage:

```
This application demonstrates how to perform basic operations on blobs
(objects) in a Google Cloud Storage bucket.

For more information, see the README.md under /storage and the documentation
at https://cloud.google.com/storage/docs.
```

Here's a docstring from a command-line application that requires a little
bit more explanation:

```python
"""This application demonstrates how to upload and download encrypted blobs
(objects) in Google Cloud Storage.

Use `generate-encryption-key` to generate an example key:

    python encryption.py generate-encryption-key

Then use the key to upload and download files encrypted with a custom key.

For more information, see the README.md under /storage and the documentation
at https://cloud.google.com/storage/docs/encryption.
"""
```

Finally, here's a docstring from a web application:

```python
"""Google Cloud Endpoints sample application.

Demonstrates how to create a simple echo API as well as how to use the
various authentication methods available.

For more information, see the README.md under /appengine/flexible and the
documentation at https://cloud.google.com/appengine/docs/flexible.
"""
```

### Functions & classes

Very few samples will require authoring classes. Prefer functions whenever
possible. See [this video](https://www.youtube.com/watch?v=o9pEzgHorH0) for
some insight into why classes aren't as necessary as you might think in Python.
Classes also introduce cognitive load. If you do write a class in a sample be
prepared to justify its existence during code review.

Always prefer descriptive function names even if they are long.
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
it prints the blobs instead of returning. In general top of the stack
functions in command-line applications should print, but use your best
judgment.

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

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))
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
as having to resort to this kind of docstring might be extremely accurate but
it comes at the cost of high redundancy, signal-to-noise ratio, and increased
cognitive load.

Finally, if absolutely necessary feel free to document the type for the
parameters, for example:

```
Args:
    credentials (google.oauth2.credentials.Credentials): Credentials authorized
      for the current user.
```

If documenting primitive types, be sure to note if they have a particular set
of constraints, for example `A base64-encoded string` or `Must be between 0 and
10`.

### Request handlers

In general these follow the same rules as top-level functions.
Here's a sample function from a web application:

```python
@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    """Receives push notifications from Cloud Pub/Sub."""
    # Verify the token - if it's not the same token used when creating the
    # notification channel then this request did not come from Pub/Sub.
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])

    MESSAGES.append(payload)

    # Returning any 2xx status indicates successful receipt of the message.
    return 'OK', 200
```

Note the name of the function matches the URL route. The docstring is kept
simple because reading the function body reveals how the parameters are
used.

Use `print` or `logging.info` in request handlers to print useful information
as needed.

### Argparse section

For command-line samples, you'll need an argparse section to handle
parsing command-line arguments and executing the sample functions. This
section lives within the `if __name__ == '__main__'` clause:

```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
```

Note the use of `__doc__` (the module-level docstring) as the description for
the parser. This helps you not repeat yourself and gives users useful
information when invoking the program. We also use `RawDescriptionHelpFormatter`
to prevent argparse from re-formatting the docstring.

Command-line arguments should generally have a 1-to-1 match to function
arguments. For example:

```python
parser.add_argument('source_file_name')
parser.add_argument('destination_blob_name')
```

Again, descriptive names prevent you from having to exhaustively describe
every parameter.

Some samples demonstrate multiple functions. You should use *subparsers* to
handle this, for example:

```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket_name', help='Your cloud storage bucket.')

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help=list_blobs.__doc__)

    upload_parser = subparsers.add_parser('upload', help=upload_blob.__doc__)
    upload_parser.add_argument('source_file_name')
    upload_parser.add_argument('destination_blob_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_blobs(args.bucket_name)
    elif args.command == 'upload':
        upload_blob(
            args.bucket_name,
            args.source_file_name,
            args.destination_blob_name)
```

### Local server

For web application samples using Flask that don't run on App Engine Standard,
the `if __name__ == '__main__'` clause should handle starting the development
server:

```python
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
```
## Writing tests

* Use [pytest](https://docs.pytest.org/en/latest/)-style tests and plain
  asserts. Don't use `unittest`-style tests or `assertX` mthods.
* All tests in this repository are **system tests**. This means they hit real
  services and should use little to no mocking.
* Tests should avoid doing very strict assertions. The exact output format
  from an API call can change, but as long as sample still works assertions
  should pass.
* Tests will run against Python 2.7 and 3. The only exception is App Engine
  standard- these samples are only be tested against Python 2.7.
* Samples that use App Engine Standard should use the App Engine testbed for
  system testing. See existing App Engine tests for how to use this.

## Running tests and automated tools

### Using nox

The testing of `python-docs-samples` is managed by
[nox](https://nox.readthedocs.io). Nox allows us to run a variety of tests,
including the linter, Python 2.7, Python 3, App Engine, and automatic README
generation.

To use nox, install it globally with `pip`:

    $ pip install nox-automation

Nox automatically discovers all samples in the repository and generates three
types of sessions for *each* sample in this repository:

1. A test sessions (`gae`, `py27` and `py35`) for running the system tests
  against a specific Python version.
2. `lint` sessions for running the style linter .
3. `readmegen` sessions for regenerating READMEs.

Because nox generates all of these sessions, it's often useful to filter down
by just the sample you're working on. For example, if you just want to see
which sessions are available for storage samples:

    $ nox -k storage -l
    * gae(sample='./appengine/standard/storage/api-client')
    * gae(sample='./appengine/standard/storage/appengine-client')
    * lint(sample='./appengine/flexible/storage')
    * lint(sample='./appengine/standard/storage/api-client')
    * lint(sample='./appengine/standard/storage/appengine-client')
    * lint(sample='./storage/api')
    * lint(sample='./storage/cloud-client')
    * lint(sample='./storage/transfer_service')
    * py27(sample='./appengine/flexible/storage')
    * py27(sample='./storage/api')
    * py27(sample='./storage/cloud-client')
    * py35(sample='./appengine/flexible/storage')
    * py35(sample='./storage/api')
    * py35(sample='./storage/cloud-client')
    * readmegen(sample='./storage/api')
    * readmegen(sample='./storage/cloud-client')
    * readmegen(sample='./storage/transfer_service')

Now you can use nox to run a specific session, for example, if you want to lint
the storage cloud-client samples:

    $ nox -s "lint(sample='./storage/cloud-client')"

### Test environment setup

Because all the tests here are system tests, you'll need to have a Google
Cloud project with billing enabled. Once you have this configured, you'll
need to set environment variables for the tests to be able to use your project
and its resources. See `testing/test-env.tmpl.sh` for a list of all environment
variables used by all tests. Not every test needs all of these variables.









