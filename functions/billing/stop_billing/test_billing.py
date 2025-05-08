from google.cloud import billing_v1

# Create a client
client = billing_v1.CloudBillingClient()

PROJECT_ID = "samples-xwf-01"
PROJECT_NAME = f"projects/{PROJECT_ID}"

# Initialize request argument(s)
request = billing_v1.GetProjectBillingInfoRequest(
    name=PROJECT_NAME,
)

# Make the request
response = client.get_project_billing_info(request=request)

# Handle the response
print(response)
