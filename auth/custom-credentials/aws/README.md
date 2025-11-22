# Running the Custom Credential Supplier Sample

If you want to use AWS security credentials that cannot be retrieved using methods supported natively by the [google-auth](https://github.com/googleapis/google-auth-library-python) library, a custom `AwsSecurityCredentialsSupplier` implementation may be specified. The supplier must return valid, unexpired AWS security credentials when called by the Google Cloud Auth library.

This sample demonstrates how to use **Boto3** (the AWS SDK for Python) as a custom supplier to bridge AWS credentials—from sources like EKS IRSA, ECS, or Fargate—to Google Cloud Workload Identity.

## Running Locally

For local development, you can provide credentials and configuration in a JSON file. For containerized environments like EKS, the script can fall back to environment variables.

### 1. Install Dependencies

Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials for Local Development

1.  Copy the example secrets file to a new file named `custom-credentials-aws-secrets.json`:
    ```bash
    cp custom-credentials-aws-secrets.json.example custom-credentials-aws-secrets.json
    ```
2.  Open `custom-credentials-aws-secrets.json` and fill in the required values for your AWS and GCP configuration. The `custom-credentials-aws-secrets.json` file is ignored by Git, so your credentials will not be checked into version control.

### 3. Run the Script

```bash
python3 snippets.py
```

When run locally, the script will detect the `custom-credentials-aws-secrets.json` file and use it to configure the necessary environment variables for the Boto3 client.

## Running in a Containerized Environment (EKS)

This section provides a brief overview of how to run the sample in an Amazon EKS cluster.

### 1. EKS Cluster Setup

First, you need an EKS cluster. You can create one using `eksctl` or the AWS Management Console. For detailed instructions, refer to the [Amazon EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html).

### 2. Configure IAM Roles for Service Accounts (IRSA)

IRSA allows you to associate an IAM role with a Kubernetes service account. This provides a secure way for your pods to access AWS services without hardcoding long-lived credentials.

You can essentially complete the OIDC setup, IAM role creation, and Service Account association in one step using `eksctl`.

Run the following command to create the IAM role and bind it to a Kubernetes Service Account:

```bash
eksctl create iamserviceaccount \
  --name your-k8s-service-account \
  --namespace default \
  --cluster your-cluster-name \
  --region your-aws-region \
  --role-name your-role-name \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
  --approve
```

> **Note**: The `--attach-policy-arn` flag is used here to demonstrate attaching permissions. Update this with the specific AWS policy ARN your application requires (e.g., if your Boto3 client needs to read from S3 or DynamoDB).

For a deep dive into how this works manually, refer to the [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) documentation.

### 3. Configure GCP to Trust the AWS Role

To allow your AWS role to authenticate as a Google Cloud service account, you need to configure Workload Identity Federation. This process involves these key steps:

1.  **Create a Workload Identity Pool and an AWS Provider:** The pool holds the configuration, and the provider is set up to trust your AWS account.

2.  **Create or select a GCP Service Account:** This service account will be impersonated by your AWS role. Grant this service account the necessary GCP permissions for your application (e.g., access to GCS or BigQuery).

3.  **Bind the AWS Role to the GCP Service Account:** Create an IAM policy binding that gives your AWS role the `Workload Identity User` (`roles/iam.workloadIdentityUser`) role on the GCP service account. This allows the AWS role to impersonate the service account.

**Alternative: Direct Access**

> For supported resources, you can grant roles directly to the AWS identity, bypassing service account impersonation. To do this, grant a role (like `roles/storage.objectViewer`) to the workload identity principal (`principalSet://...`) directly on the resource's IAM policy.

For more detailed information, see the documentation on [Configuring Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds).

### 4. Containerize and Package the Application

Create a `Dockerfile` for the Python application and push the image to a container registry (e.g., Amazon ECR) that your EKS cluster can access. Refer to the [`Dockerfile`](Dockerfile) for the container image definition.

Build and push the image:
```bash
docker build -t your-container-image:latest .
docker push your-container-image:latest
```

### 5. Deploy to EKS

Create a Kubernetes deployment manifest to deploy your application to the EKS cluster. See the [`pod.yaml`](pod.yaml) file for an example.

Deploy the pod:

```bash
kubectl apply -f pod.yaml
```

### 6. Clean Up

To clean up the resources, delete the EKS cluster and any other AWS and GCP resources you created.

```bash
eksctl delete cluster --name your-cluster-name
```