from google.cloud import run_v2

client = run_v2.ServicesClient()

full_service_name = "projects/samples-xwf-02/locations/us-central1/services/receive-python"

# Initialize request argument(s)
request = run_v2.GetServiceRequest(
    name=full_service_name,
)

# Make the request
response = client.get_service(request=request)

# Handle the response
print(response.uri)
print(client.get_service(request=request).uri)
