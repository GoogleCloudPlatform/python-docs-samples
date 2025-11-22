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

To run the sample on your local system, you need to install the dependencies and configure your credentials.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Credentials

1.  Copy the example secrets file to a new file named `custom-credentials-okta-secrets.json`:
    ```bash
    cp custom-credentials-okta-secrets.json.example custom-credentials-okta-secrets.json
    ```
2.  Open `custom-credentials-okta-secrets.json` and fill in the following values:

    *   `okta_domain`: Your Okta developer domain (e.g., `https://dev-123456.okta.com`).
    *   `okta_client_id`: The client ID for your application.
    *   `okta_client_secret`: The client secret for your application.
    *   `gcp_workload_audience`: The audience for the GCP Workload Identity Pool. This typically follows the format: `//iam.googleapis.com/projects/YOUR_PROJECT_NUMBER/locations/global/workloadIdentityPools/YOUR_POOL_ID/providers/YOUR_PROVIDER_ID`.
    *   `gcs_bucket_name`: The name of the GCS bucket to access.
    *   `gcp_service_account_impersonation_url`: (Optional) The URL for service account impersonation. If set, the script will exchange the federated token for a Google Service Account token. Example: `https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/my-service-account@my-project.iam.gserviceaccount.com:generateAccessToken`.

### Run the Application

```bash
python3 snippets.py
```

The script will then authenticate with Okta to get an OIDC token, exchange that token for a GCP federated token (and optionally a Service Account token), and use it to list metadata for the specified GCS bucket.