# Running the Custom AWS Credential Supplier Sample

This sample demonstrates how to use a custom AWS security credential supplier to authenticate with Google Cloud using AWS as an external identity provider. It uses Boto3 (the AWS SDK for Python) to fetch credentials from sources like Amazon Elastic Kubernetes Service (EKS) with IAM Roles for Service Accounts(IRSA), Elastic Container Service (ECS), or Fargate.

## Prerequisites

*   An AWS account.
*   A Google Cloud project with the IAM API enabled.
*   A GCS bucket.
*   Python 3.10 or later installed.

If you want to use AWS security credentials that cannot be retrieved using methods supported natively by the [google-auth](https://github.com/googleapis/google-auth-library-python) library, a custom `AwsSecurityCredentialsSupplier` implementation may be specified. The supplier must return valid, unexpired AWS security credentials when called by the Google Cloud Auth library.


## Running Locally

For local development, you can provide credentials and configuration in a JSON file.

### Install Dependencies

Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

### Configure Credentials for Local Development

1.  Copy the example secrets file to a new file named `custom-credentials-aws-secrets.json`:
    ```bash
    cp custom-credentials-aws-secrets.json.example custom-credentials-aws-secrets.json
    ```
2.  Open `custom-credentials-aws-secrets.json` and fill in the required values for your AWS and Google Cloud configuration. Do not check your `custom-credentials-aws-secrets.json` file into version control.

**Note:** This file is only used for local development and is not needed when running in a containerized environment like EKS with IRSA.


### Run the Script

```bash
python3 snippets.py
```

When run locally, the script will detect the `custom-credentials-aws-secrets.json` file and use it to configure the necessary environment variables for the Boto3 client.

## Running in a Containerized Environment (EKS)

This section provides a brief overview of how to run the sample in an Amazon EKS cluster.

### EKS Cluster Setup

First, you need an EKS cluster. You can create one using `eksctl` or the AWS Management Console. For detailed instructions, refer to the [Amazon EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html).

### Configure IAM Roles for Service Accounts (IRSA)

IRSA enables you to associate an IAM role with a Kubernetes service account. This provides a secure way for your pods to access AWS services without hardcoding long-lived credentials.

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

> **Note**: The `--attach-policy-arn` flag is used here to demonstrate attaching permissions. Update this with the specific AWS policy ARN your application requires.

For a deep dive into how this works without using `eksctl`, refer to the [IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) documentation.

### Configure Google Cloud to Trust the AWS Role

To allow your AWS role to authenticate as a Google Cloud service account, you need to configure Workload Identity Federation. This process involves these key steps:

1.  **Create a Workload Identity Pool and an AWS Provider:** The pool holds the configuration, and the provider is set up to trust your AWS account.

2.  **Create or select a Google Cloud Service Account:** This service account will be impersonated by your AWS role.

3.  **Bind the AWS Role to the Google Cloud Service Account:** Create an IAM policy binding that gives your AWS role the `Workload Identity User` (`roles/iam.workloadIdentityUser`) role on the Google Cloud service account.

For more detailed information, see the documentation on [Configuring Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds).

**Alternative: Direct Access**

> For supported resources, you can grant roles directly to the AWS identity, bypassing service account impersonation. To do this, grant a role (like `roles/storage.objectViewer`) to the workload identity principal (`principalSet://...`) directly on the resource's IAM policy.

For more detailed information, see the documentation on [Configuring Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds).

### Containerize and Package the Application

Create a `Dockerfile` for the Python application and push the image to a container registry (for example Amazon ECR) that your EKS cluster can access.

**Note:** The provided [`Dockerfile`](Dockerfile) is an example and may need to be modified for your specific needs.

Build and push the image:
```bash
docker build -t your-container-image:latest .
docker push your-container-image:latest
```

### Deploy to EKS

Create a Kubernetes deployment manifest to deploy your application to the EKS cluster. See the [`pod.yaml`](pod.yaml) file for an example.

**Note:** The provided [`pod.yaml`](pod.yaml) is an example and may need to be modified for your specific needs.

Deploy the pod:

```bash
kubectl apply -f pod.yaml
```

### Clean Up

To clean up the resources, delete the EKS cluster and any other AWS and Google Cloud resources you created.

```bash
eksctl delete cluster --name your-cluster-name
```

## Testing

This sample is not continuously tested. It is provided for instructional purposes and may require modifications to work in your environment.
