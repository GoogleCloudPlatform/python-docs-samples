import numpy as np
import requests

# model_url = "https://weather-nohakdsi7q-uc.a.run.app"
model_url = "http://127.0.0.1:8080"
identity_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImEyOWFiYzE5YmUyN2ZiNDE1MWFhNDMxZTk0ZmEzNjgwYWU0NThkYTUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA5NjY4NDE3ODgyNzExNDkyOTA1IiwiaGQiOiJnb29nbGUuY29tIiwiZW1haWwiOiJkY2F2YXpvc0Bnb29nbGUuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ6T0YwWU9FdmFnZXcweGdoZHJoc0F3IiwiaWF0IjoxNjczMTQ0NTA2LCJleHAiOjE2NzMxNDgxMDZ9.Bm2FZjSgNTOHJqQ4dhtiQKk85YBK6rhiFt8C-pELqsgyl-8FPm86Fb6Ghs6P4nzsyg0NsxYKj9f_FYBUbzF_gIgc2n8DOM0hEUNGomgSUUYU02Edm4XVIHRd-3meB9miMjNDWZNEdZxJO0Q23DckxQkLqlouS28wfWXcnBdr8maola5joElF_7BqbxfoX1qlwL_im_Vqor_GtkMkGiQRV-tSszggQ2HHPoVjWIRVH49w71pZWB0Z5jUaxK-CIbhKkAMsI-1mUbN1byy7sf9FIG7K3LmQr3yC1FLYwUtB-gP9HWAE3W-RzmoHpostkGC9AFmRuOrVwsKbwY2M-NR7tg"

response = requests.get(
    f"{model_url}/predict/2019-09-02T18:00/25.507,-78.322",
    headers={"Authorization": f"Bearer {identity_token}"},
    # params={"patch-size": 64},
)

response.raise_for_status()
results = response.json()

inputs = np.array(results["inputs"], np.float32)
predictions = np.array(results["predictions"], np.uint8)

print(f"inputs: {inputs.dtype.name} {inputs.shape}")
print(f"predictions : {predictions.dtype.name} {predictions.shape}")
