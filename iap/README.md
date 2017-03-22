# Identity-Aware Proxy Samples

<!-- auto-doc-link -->
These samples are used on the following documentation pages:

>
* https://cloud.google.com/iap/docs/authentication-howto
* https://cloud.google.com/iap/docs/signed-headers-howto

<!-- end-auto-doc-link -->

## Using make_iap_request

### Google App Engine flexible environment

1. Add the contents of this directory's `requirements.txt` file to the one
   inside your application.
2. Copy `make_iap_request.py` into your application.

### Google App Engine standard environment

1. Follow the instructions
   in
   [Installing a third-party library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_third-party_library) to
   install the `google-auth` and `requests` libraries into your application.
2. Copy `make_iap_request.py` into the same folder as app.yaml .

### Google Compute Engine or Google Container Engine

1. Enable the IAM API on your project.
2. Create a VM with the IAM scope:
   ```
   gcloud compute instances create INSTANCE_NAME
   --scopes=https://www.googleapis.com/auth/iam
   ```
3. Give your VM's default service account the `Service Account Actor` role:
   ```
   gcloud projects add-iam-policy-binding PROJECT_ID
   --role=roles/iam.serviceAccountActor
   --member=serviceAccount:SERVICE_ACCOUNT
   ```
4. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
5. Copy `make_iap_request.py` into your application.

### Using a downloaded service account private key

1. Create a service account and download its private key.
   See https://cloud.google.com/iam/docs/creating-managing-service-account-keys
   for more information on how to do this.
2. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path
   to your service account's `.json` file.
3. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
4. Copy `make_iap_request.py` into your application.

If you prefer to manage service account credentials manually, this method can
also be used in the App Engine flexible environment, Compute Engine, and
Container Engine. Note that this may be less secure, as anyone who obtains the
service account private key can impersonate that account!

## Using validate_jwt

`validate_jwt` is not compatible with App Engine standard environment;
use App Engine's Users API instead. (See `app_engine_app` for an example
of how to do this.)

For all other environments:

1. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
2. Copy `validate_jwt.py` into your application.

## Running Tests

1. Deploy `app_engine_app` to a project.
2. Enable Identity-Aware Proxy on that project's App Engine app.
3. Add the service account you'll be running the test as to the
   Identity-Aware Proxy access list for the project.
4. Update iap_test.py with the hostname for your project.
5. Run the command: ```GOOGLE_CLOUD_PROJECT=project-id pytest iap_test.py```
