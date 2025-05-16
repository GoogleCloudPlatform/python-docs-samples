from google.auth.transport import requests
from google.oauth2 import id_token


def token(audience: str) -> str:
    # Cloud Run uses your service's hostname as the `audience` value
    # audience = 'https://my-cloud-run-service.run.app/'
    auth_req = requests.Request()
    token = id_token.fetch_id_token(auth_req, audience)

    return token


print(token("https://receive-python-698899164414.us-central1.run.app"))

# Returned
# Hello, insecure-cloudtop-shared-user@cloudtop-prod-us-west.iam.gserviceaccount.com.
# Perhaps we need to interpersonate someone else?
"""
{
  "aud": "https://receive-go-07567b6d-6543-4d2f-8266-332b1ccfd8bc-764067474825.us-central1.run.app",
  "azp": "115299743472206915304",
  "email": "insecure-cloudtop-shared-user@cloudtop-prod-us-west.iam.gserviceaccount.com",
  "email_verified": "true",
  "exp": "1745091447",
  "google": "{\"compute_engine\":{\"instance_creation_timestamp\":1744858838,\"instance_id\":\"4635286025016483629\",\"instance_name\":\"paradalicea\",\"project_id\":\"cloudtop-prod-us-west\",\"project_number\":597486904816,\"zone\":\"us-west4-a\"}}",
  "iat": "1745087847",
  "iss": "https://accounts.google.com",
  "sub": "115299743472206915304",
  "alg": "RS256",
  "kid": "c37da75c9fbe18c2ce9125b9aa1f300dcb31e8d9",
  "typ": "JWT"
}
"""
