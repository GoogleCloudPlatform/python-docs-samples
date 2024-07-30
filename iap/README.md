# Identity-Aware Proxy Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=iap/README.md

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
1. Copy `make_iap_request.py` into your application.

### Google App Engine standard environment

1. Follow the instructions
   in
   [Installing a third-party library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_third-party_library) to
   install the `google-auth` and `requests` libraries into your application.
2. Copy `make_iap_request.py` into the same folder as app.yaml .

### Google Compute Engine or Google Kubernetes Engine

1. [Click here](https://console.cloud.google.com/flows/enableapi?apiid=iam.googleapis.com&showconfirmation=true) to visit Google Cloud Platform Console and enable the IAM API on your project.
1. Create a VM with the IAM scope:
   ```
   gcloud compute instances create INSTANCE_NAME
   --scopes=https://www.googleapis.com/auth/iam
   ```
1. Give your VM's default service account the `Service Account Actor` role:
   ```
   gcloud projects add-iam-policy-binding PROJECT_ID
   --role=roles/iam.serviceAccountActor
   --member=serviceAccount:SERVICE_ACCOUNT
   ```
1. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
1. Copy `make_iap_request.py` into your application.

### Using a downloaded service account private key

1. Create a service account and download its private key.
   See https://cloud.google.com/iam/docs/creating-managing-service-account-keys
   for more information on how to do this.
1. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path
   to your service account's `.json` file.
1. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
1. Copy `make_iap_request.py` into your application.

If you prefer to manage service account credentials manually, this method can
also be used in the App Engine flexible environment, Compute Engine, and
Kubernetes Engine. Note that this may be less secure, as anyone who obtains the
service account private key can impersonate that account!

## Using validate_jwt

1. Install the libraries listed in `requirements.txt`, e.g. by running:
   ```
   virtualenv/bin/pip install -r requirements.txt
   ```
1. Copy `validate_jwt.py` into your application.

## Using generate_self_signed_jwt

### Self-signed JWT with IAM Credentials API

Ensure that you are in the correct working directory: (/python-docs-samples/iap):

1. Install the libraries listed in `/python-docs-samples/iap/requirements.txt`, e.g. by running:

   ```
      virtualenv/bin/pip install -r requirements.txt
   ```

1. Call `sign_jwt` in the python file. This example would create a JWT for the service account email@gmail.com to access the IAP protected application hosted at https://example.com.

   ```
      sign_jwt("email@gmail.com", "https://example.com")
   ``` 

1. Use the result of the call to access your IAP protected resource programmatically: 
   ```
      curl --verbose --header 'Authorization: Bearer SIGNED_JWT' "https://example.com"
   ```


### Self-signed JWT with local key file
1. Install the libraries listed in `/python-docs-samples/iap/requirements.txt`, e.g. by running:

   ```
      virtualenv/bin/pip install -r requirements.txt
   ```
1. Create a service account and download its private key.
   See https://cloud.google.com/iam/docs/creating-managing-service-account-keys
   for more information on how to do this.
1. Call `sign_jwt_with_local_credentials_file`,  using the downloaded local credentials
   for the service account.
   ```
      sign_jwt_with_local_credentials_file("path/to/key/file.json", "https://example.com")
   ```

1. Use the result of the call to access your IAP protected resource programmatically: 
   ```
      curl --verbose --header 'Authorization: Bearer SIGNED_JWT' "https://example.com"
   ```
## Running Tests

1. Deploy `app_engine_app` to a project.
1. Enable Identity-Aware Proxy on that project's App Engine app.
1. Add the service account you'll be running the test as to the
   Identity-Aware Proxy access list for the project.
1. Update iap_test.py with the hostname for your project.
1. Run the command: ```GOOGLE_CLOUD_PROJECT=project-id pytest iap_test.py```
