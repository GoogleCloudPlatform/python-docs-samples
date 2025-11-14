# Running the Custom Credential Supplier Sample

If you want to use AWS security credentials that cannot be retrieved using methods supported natively by the [google-auth](https://github.com/googleapis/google-auth-library-python) library, a custom `AwsSecurityCredentialsSupplier` implementation may be specified. The supplier must return valid, unexpired AWS security credentials when called by the GCP credential.

This sample demonstrates how to use **Boto3** (the AWS SDK for Python) as a custom supplier to bridge AWS credentials—from sources like EKS IRSA, ECS, or Fargate—to Google Cloud Workload Identity.

## Running Locally

To run the sample on your local system, you need to install the dependencies and configure your AWS and GCP credentials as environment variables.

### 1. Install Dependencies

Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
export AWS_REGION="YOUR_AWS_REGION" # e.g., us-east-1
export GCP_WORKLOAD_AUDIENCE="YOUR_GCP_WORKLOAD_AUDIENCE"
export GCS_BUCKET_NAME="YOUR_GCS_BUCKET_NAME"

# Optional: If you want to use service account impersonation
export GCP_SERVICE_ACCOUNT_IMPERSONATION_URL="YOUR_GCP_SERVICE_ACCOUNT_IMPERSONATION_URL"
```

### 3. Run the Script

```bash
python3 snippets.py
```

## Running in a Containerized Environment (EKS)

This section provides a brief overview of how to run the sample in an Amazon EKS cluster.

### 1. EKS Cluster Setup

First, you need an EKS cluster. You can create one using `eksctl` or the AWS Management Console. For detailed instructions, refer to the [Amazon EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html).

### 2. Configure IAM Roles for Service Accounts (IRSA)

IRSA allows you to associate an IAM role with a Kubernetes service account. This provides a secure way for your pods to access AWS services without hardcoding long-lived credentials.

- Create an IAM OIDC provider for your cluster.
- Create an IAM role and policy that grants the necessary AWS permissions.
- Associate the IAM role with a Kubernetes service account.

For detailed steps, see the [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) documentation.

### 3. Configure GCP to Trust the AWS Role

You need to configure your GCP project to trust the AWS IAM role you created. This is done by creating a Workload Identity Pool and Provider in GCP.

- Create a Workload Identity Pool.
- Create a Workload Identity Provider that trusts the AWS role ARN.
- Grant the GCP service account the necessary permissions.

### 4. Containerize and Package the Application

Create a `Dockerfile` for the Python application and push the image to a container registry (e.g., Amazon ECR) that your EKS cluster can access.

**Dockerfile**
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY snippets.py .

# Run the script
CMD ["python3", "snippets.py"]
```

Build and push the image:
```bash
docker build -t your-container-image:latest .
docker push your-container-image:latest
```

### 5. Deploy to EKS

Create a Kubernetes deployment manifest (`pod.yaml`) to deploy your application to the EKS cluster.

**pod.yaml**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: custom-credential-pod
spec:
  serviceAccountName: your-k8s-service-account # The service account associated with the AWS IAM role
  containers:
  - name: gcp-auth-sample
    image: your-container-image:latest # Your image from ECR
    env:
    # AWS_REGION is often required for Boto3 to initialize correctly in containers
    - name: AWS_REGION
      value: "your-aws-region"
    - name: GCP_WORKLOAD_AUDIENCE
      value: "your-gcp-workload-audience"
    # Optional: If you want to use service account impersonation
    # - name: GCP_SERVICE_ACCOUNT_IMPERSONATION_URL
    #   value: "your-gcp-service-account-impersonation-url"
    - name: GCS_BUCKET_NAME
      value: "your-gcs-bucket-name"
```

Deploy the pod:

```bash
kubectl apply -f pod.yaml
```

### 6. Clean Up

To clean up the resources, delete the EKS cluster and any other AWS and GCP resources you created.

```bash
eksctl delete cluster --name your-cluster-name
```