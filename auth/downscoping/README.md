# Downscoping with Credential Access Boundaries

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=auth/downscoping/README.md

This section contains samples for
[Downscoping with Credential Access Boundaries](https://cloud.google.com/iam/docs/downscoping-short-lived-credentials).

## Running the samples

1. Your environment must be setup with [authentication
information](https://developers.google.com/identity/protocols/application-default-credentials#howtheywork). If you're running on Compute Engine, this is already setup. You can also use `gcloud auth application-default login`.

2. Install dependencies from `requirements.txt`

        $ pip install -r requirements.txt

3. You will also need to create resources on the [Google Developers Console](https://console.developers.google.com). This includes
creating a private Cloud Storage bucket and setting the environment variable `CLOUD_STORAGE_BUCKET` value to the bucket name.
The application default credentials principal should have the ability to create and manage objects in that bucket.

4. Set the environment variable `GOOGLE_CLOUD_PROJECT` to the project ID.
More details are available in the [AUTHORING_GUIDE](../../AUTHORING_GUIDE.md).

5. To run the samples, the `main(bucket_name, filename)` function should be run with the created bucket name
and the path to a test file to use to test access.

6. To run the tests:

        $ nox -s py-3.7 -- snippets_test.py

## Additional resources

For more information on downscoped credentials you can visit:

> https://github.com/googleapis/google-auth-library-python
