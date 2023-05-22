# User-managed encryption key publisher

Code intended to be run by users of the Live Stream API. This code utilizes DRM
provider CPIX APIs to fetch encryption keys and store them in Google Secret
Manager for use with the Live Stream API's encryption feature.

To create a zip archive of all the files needed to run key publisher, run the
script `./package.sh`.

## 1. Setup

### Install and configure gcloud

Follow [standard install instructions](http://cloud/sdk/docs/install). Use
`gcloud config` to set your project and preferred region/zone.

## 2. Configure Cloud Functions and API Gateway

### Enable APIs

Enable the following Google APIs to host your key publisher and write key
information to Secret Manager.

```shell
gcloud services enable apigateway.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable servicecontrol.googleapis.com
gcloud services enable servicemanagement.googleapis.com
```

### Create service accounts

Two service accounts are needed for your key publisher. The first allows your
API Gateway to invoke your cloud function (with the IAM role of
`roles/cloudfunctions.invoker`), and the second allows Cloud Functions to read
and write to Secret Manager (with the IAM role of `roles/secretmanager.admin`).

Create the service account for invoking Cloud Functions:

```shell
gcloud iam service-accounts create livestream-cf-invoker \
  --display-name="Cloud Function invoker for the API Gateway" \
  --description="Service Account to be used by the API Gateway to invoke Cloud Functions"
```

Then configure the IAM policy binding using your `project-id`:

```shell
gcloud projects add-iam-policy-binding [MY-PROJEC-ID] \
  --member serviceAccount:"livestream-cf-invoker@[MY-PROJECT-ID].iam.gserviceaccount.com" \
  --role "roles/cloudfunctions.invoker" \
  --no-user-output-enabled \
  --quiet
```

Next, create another service account for interacting with Secret Manager:

```shell
gcloud iam service-accounts create livestream-cloud-functions \
  --display-name="Service account for Cloud Functions" \
  --description="Service Account used for the Live Stream API key publisher functions"
```

Then configure the IAM policy binding:

```shell
gcloud projects add-iam-policy-binding [MY-PROJECT-ID] \
  --member serviceAccount:"livestream-cloud-functions@[MY-PROJECT-ID].iam.gserviceaccount.com" \
  --role "roles/secretmanager.admin" \
  --no-user-output-enabled \
  --quiet
```

### Deploy the cloud function

Create a file `.env.yaml`. Take a look at the example template file:
[`env.template.yml`](./templates/env.template.yml). Copy the template file and
replace any needed values. This file will store environment variables to be used
by your function. This file should have the following contents (also included in
the example file):

```yaml
# Your project ID.
PROJECT: [MY-PROJECT-ID]
# The endpoint of the CPIX API the key publisher will be calling.
CPIX_ENDPOINT: https://cpix-api.url
# The ID of the secret containing the provider's public certificate.
CPIX_PUBLIC_CERT_PROVIDER_SECRET: cpix-public-cert-provider
# The ID of the secret containing your private key.
CPIX_PRIVATE_KEY_USER_SECRET: cpix-private-key-user
# The ID of the secret containing your public certificate.
CPIX_PUBLIC_CERT_USER_SECRET: cpix-public-cert-user
# (Optional) The ID of the secret containing your enduser private key.
CPIX_PRIVATE_KEY_ENDUSER_SECRET: cpix-private-key-enduser
# (Optional) The ID of the secret containing your enduser public certificate.
CPIX_PUBLIC_CERT_ENDUSER_SECRET: cpix-public-cert-enduser
```

Then deploy your function:

```shell
gcloud functions deploy livestream-key-publisher \
  --entry-point=keys \
  --runtime=python310 \
  --trigger-http \
  --memory=256MB \
  --security-level=secure-always \
  --timeout=60s \
  --env-vars-file=.env.yaml \
  --service-account="livestream-cloud-functions@[MY-PROJECT-ID].iam.gserviceaccount.com"
```

After your function is deployed, the response you get will contain the
`httpsTrigger.url` field. It will show up in the following format:

```shell
httpsTrigger:
    url: https://<REGION>-<MY-PROJECT_ID>.cloudfunctions.net/livestream-key-publisher
```

Save this value for later when you configure your API Gateway.

### Create the API and API Gateway

Create the API:

```shell
gcloud api-gateway apis create livestream-key-publisher-api --display-name="Live Stream Key Publisher API"
```

Create a file `api-config.yml`. Take a look at the example template file:
[`api-config.template.yml`](./templates/api-config.template.yml). Copy the
template file and replace any needed values. In particular `CLOUD_FUNCTION_URL`
must be replaced with the URL you received when you deployed your function.

Once the file has been created, create your API config:

```shell
gcloud api-gateway api-configs create livestream-key-publisher-api-config-1 \
  --display-name="Live Stream Key Publisher API Config v1" \
  --api=livestream-key-publisher-api \
  --openapi-spec="api-config.yml" \
  --backend-auth-service-account="livestream-cf-invoker@[MY-PROJECT-ID].iam.gserviceaccount.com"
```

Next, create the API Gateway. The following example deploys to GCP Region
`us-central1`. You can choose a different location from supported GCP Regions
[listed here](https://cloud.google.com/api-gateway/docs/deploying-api#deploy_an_api_config_to_a_gateway):

```shell
gcloud api-gateway gateways create livestream-key-publisher-api-gateway \
  --display-name="Live Stream Key Publisher API Gateway" \
  --api=livestream-key-publisher-api \
  --api-config=livestream-key-publisher-api-config-1 \
  --location=us-central1
```

Once created, your API must be enabled. Run a command to describe your API:

```shell
gcloud api-gateway apis describe livestream-key-publisher-api
```

You will get the `managedService` field in the response. This is the service you
need to enable. For example,

```shell
gcloud services enable livestream-key-publisher-api-144h6p0e7bzc1.apigateway.[MY-PROJECT-ID].cloud.goog
```

Now you need to locate the endpoint URL of your API. Run a command to describe
your gateway:

```shell
gcloud api-gateway gateways describe livestream-key-publisher-api-gateway --location=us-central1
```

You will get the `defaultHostname` field in the response. For example,

```
defaultHostname: livestream-key-publisher-api-gateway-48mwfke9.uc.gateway.dev
```

You will send API requests to the URL received from your response.

Create an API key to use for making queries to your API, and restrict the API
key such that only your newly created `livestream-key-publisher-api` can be
called with the API key. Specify the API restriction with the `managedService`
field from earlier:

```shell
gcloud alpha services api-keys create --api-target=service=[managedService]
```

For example

```shell
gcloud alpha services api-keys create --api-target=service=livestream-key-publisher-api-144h6p0e7bzc1.apigateway.[MY-PROJECT-ID].cloud.goog
```

> **Warning**: You will get the `keyString` field in the response. This is your
> API key. Save this key, as you will not be able to retrieve it again.

### Test your API

Using the above information, use `curl` to make a `GET` query to your API:

```shell
curl --location --request POST \
  'https://livestream-key-publisher-api-gateway-48mwfke9.uc.gateway.dev/keys?api_key=YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"mediaId": "my-asset", "provider": "FakeProvider", "keyIds": ["abcd1234", "efgi5678"]}'
```

Arguments in the request body are:

*   `mediaId`: arbitrary identifier for the media being encrypted.
*   `provider`: the DRM provider to use. Omit this argument to see a list of
    supported providers.
*   `keyIds`: a list of key IDs to prepare for the given media ID.

This example query uses `FakeProvider`. This is a provider used as a reference
example, which does not make any actual CPIX queries, but generates random hex
strings in place of a real key. These keys will not work for a real encryption
setup. `keyIds` should be unique identifiers for the keys provided by your
third-party DRM provider. Please replace `provider` and `keyIds` accordingly.
For `mediaId`, you can change it to any identifier to label the encrypted media.

If the query is successful, you will see a response like:

```
projects/PROJECT_NUMBER/secrets/MEDIA_ID/versions/1
```

This is the name of the secret version that was created to hold your encryption
keys.

To verify this, you can use `gcloud` to access the content of that secret:

```shell
gcloud secrets versions access projects/PROJECT_NUMBER/secrets/MEDIA_ID/versions/1
```

## 3. Update code

Use `gcloud functions deploy` to update your Cloud Function code. Ensure
`.env.yaml` still exists (example file:
[env.template.yml](./templates/env.template.yml)).

```shell
gcloud functions deploy livestream-key-publisher \
  --entry-point=keys \
  --runtime=python310 \
  --trigger-http \
  --memory=256MB \
  --security-level=secure-always \
  --timeout=60s \
  --env-vars-file=.env.yaml \
  --service-account="livestream-cloud-functions@[MY-PROJECT-ID].iam.gserviceaccount.com"
```

If request paths or parameters have changed, you may also need to update
`api-config.yml` to match. To do this, update `api-config.yml` as needed, then
create a new API config:

```shell
gcloud api-gateway api-configs create livestream-key-publisher-api-config-2 \
  --display-name="Live Stream Key Publisher API Config v2" \
  --api=livestream-key-publisher-api \
  --openapi-spec="api-config.yml" \
  --backend-auth-service-account="livestream-cf-invoker@[MY-PROJECT-ID].iam.gserviceaccount.com"
```

Once the config has been created, update the API Gateway to use your new config:

```shell
gcloud api-gateway gateways update livestream-key-publisher-api-gateway \
  --api=livestream-key-publisher-api \
  --api-config=livestream-key-publisher-api-config-2 \
  --location=us-central1
```

## 4. Supported Python Versions

The code samples for key publisher are compatible with all current
[active](https://devguide.python.org/developer-workflow/development-cycle/index.html#in-development-main-branch)
and
[maintenance](https://devguide.python.org/developer-workflow/development-cycle/index.html#maintenance-branches)
versions of Python.

## 5. Testing

You can run unit tests for this code in a local environment. These tests do not
utilize external services (e.g. Google Cloud Functions, Google Secret Manager).

Install python virtual environment:

```shell
sudo apt-get install python3-venv
```

Create a local virtual environment for running tests:

```shell
python3 -m venv venv-key-publisher-test
```

And activate the virtual environment:

```shell
. venv-key-publisher-test/bin/activate
```

Install dependencies needed for testing:

```shell
pip install -r requirements.txt
```

Execute the tests:

```shell
pytest -k _test.py -v
```
