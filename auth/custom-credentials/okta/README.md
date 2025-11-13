Here is the adapted `README.md` for the Python version of the Okta Custom Credential Supplier sample.

# Running the Custom Okta Credential Supplier Sample (Python)

If you want to use OIDC or SAML 2.0 tokens that cannot be retrieved using methods supported natively by the [google-auth](https://github.com/googleapis/google-auth-library-python) library, a custom `SubjectTokenSupplier` implementation may be specified when creating an identity pool client. The supplier must return a valid, unexpired subject token when called by the GCP credential.

This document provides instructions on how to run the custom Okta credential supplier sample using Python.

## 1. Okta Configuration

Before running the sample, you need to configure an Okta application for Machine-to-Machine (M2M) communication.

### Create an M2M Application in Okta

1.  Log in to your Okta developer console.
2.  Navigate to **Applications** > **Applications** and click **Create App Integration**.
3.  Select **API Services** as the sign-on method and click **Next**.
4.  Give your application a name and click **Save**.

### Obtain Okta Credentials

Once the application is created, you will find the following information in the **General** tab:

*   **Okta Domain**: Your Okta developer domain (e.g., `https://dev-123456.okta.com`).
*   **Client ID**: The client ID for your application.
*   **Client Secret**: The client secret for your application.

You will need these values to configure the sample.

## 2. GCP Configuration

You need to configure a Workload Identity Pool in GCP to trust the Okta application.

### Set up Workload Identity Federation

1.  In the Google Cloud Console, navigate to **IAM & Admin** > **Workload Identity Federation**.
2.  Click **Create Pool** to create a new Workload Identity Pool.
3.  Add a new **OIDC provider** to the pool.
4.  Configure the provider with your Okta domain as the issuer URL.
5.  Map the Okta `sub` (subject) assertion to a GCP principal.

For detailed instructions, refer to the [Workload Identity Federation documentation](https://cloud.google.com/iam/docs/workload-identity-federation).

### GCS Bucket

Ensure you have a GCS bucket that the authenticated user will have access to. You will need the name of this bucket to run the sample.

## 3. Running the Script

To run the sample on your local system, you need to install the dependencies and configure the environment variables.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Environment Variables

The script relies on the `GCP_WORKLOAD_AUDIENCE` variable, which typically follows this format:
`//iam.googleapis.com/projects/YOUR_PROJECT_NUMBER/locations/global/workloadIdentityPools/YOUR_POOL_ID/providers/YOUR_PROVIDER_ID`

```bash
# Okta Configuration
export OKTA_DOMAIN="https://your-okta-domain.okta.com"
export OKTA_CLIENT_ID="your-okta-client-id"
export OKTA_CLIENT_SECRET="your-okta-client-secret"

# GCP Configuration
export GCP_WORKLOAD_AUDIENCE="//iam.googleapis.com/projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider"
export GCS_BUCKET_NAME="your-gcs-bucket-name"

# Optional: Service Account Impersonation
# If set, the script will exchange the federated token for a Google Service Account token.
export GCP_SERVICE_ACCOUNT_IMPERSONATION_URL="https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/my-service-account@my-project.iam.gserviceaccount.com:generateAccessToken"
```

### Run the Application

```bash
python3 snippets.py
```

The script will then authenticate with Okta to get an OIDC token, exchange that token for a GCP federated token (and optionally a Service Account token), and use it to list metadata for the specified GCS bucket.