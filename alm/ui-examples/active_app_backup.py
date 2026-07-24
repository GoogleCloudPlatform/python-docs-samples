
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# A comprehensive list of GCP regions
GCP_REGIONS = [
    "africa-south1",
    "asia-east1", "asia-east2", "asia-northeast1", "asia-northeast2", "asia-northeast3",
    "asia-south1", "asia-south2", "asia-southeast1", "asia-southeast2",
    "australia-southeast1", "australia-southeast2",
    "europe-central2", "europe-north1", "europe-southwest1",
    "europe-west1", "europe-west2", "europe-west3", "europe-west4",
    "europe-west6", "europe-west8", "europe-west9", "europe-west10", "europe-west12",
    "me-central1", "me-central2", "me-west1",
    "northamerica-northeast1", "northamerica-northeast2",
    "southamerica-east1", "southamerica-west1",
    "us-central1", "us-east1", "us-east4", "us-east5",
    "us-south1", "us-west1", "us-west2", "us-west3", "us-west4"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_region = None
    api_response_data = None
    operation_state = None
    
    if request.method == 'POST':
        # Get the selected region and which button was clicked
        selected_region = request.form.get('region')
        action = request.form.get('action') 
        
        # --- DEPLOY BUTTON CLICKED ---
        if action == 'deploy':
            print(f"\n--- SUCCESS: User clicked DEPLOY for: {selected_region} ---\n")
            url = "https://apigee.saas8384.saas-example.com/v1/saas/operations"
            headers = {"Content-Type": "application/json"}
            payload = {"region": selected_region}
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status() 
                api_response_data = response.json() 
                print(f"Deploy Successful. Response: {api_response_data}")
            except requests.exceptions.RequestException as e:
                print(f"API Call Failed: {e}")
                api_response_data = {"error": str(e)}

        # --- GET STATUS BUTTON CLICKED ---
        elif action == 'status':
            print(f"\n--- SUCCESS: User clicked STATUS for: {selected_region} ---\n")
            operation_id = "depr-25094d41-7768-4ef3-bd8d-e5bf67ca09d6"
            url = f"https://apigee.saas8384.saas-example.com/v1/saas/operations/{operation_id}?region={selected_region}"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                # Parse JSON and get the state
                get_data = response.json()
                operation_state = get_data.get('state', 'STATE_UNKNOWN')
                print(f"Status check successful. State: {operation_state}")
                
            except requests.exceptions.RequestException as e:
                print(f"Status API Call Failed: {e}")
                operation_state = "ERROR_FETCHING_STATE"

    return render_template(
        'index.html', 
        regions=GCP_REGIONS, 
        selected_region=selected_region, 
        api_response=api_response_data,
        operation_state=operation_state
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)








# from flask import Flask, render_template, request

# app = Flask(__name__)

# # A comprehensive list of GCP regions
# GCP_REGIONS = [
#     "africa-south1",
#     "asia-east1", "asia-east2", "asia-northeast1", "asia-northeast2", "asia-northeast3",
#     "asia-south1", "asia-south2", "asia-southeast1", "asia-southeast2",
#     "australia-southeast1", "australia-southeast2",
#     "europe-central2", "europe-north1", "europe-southwest1",
#     "europe-west1", "europe-west2", "europe-west3", "europe-west4",
#     "europe-west6", "europe-west8", "europe-west9", "europe-west10", "europe-west12",
#     "me-central1", "me-central2", "me-west1",
#     "northamerica-northeast1", "northamerica-northeast2",
#     "southamerica-east1", "southamerica-west1",
#     "us-central1", "us-east1", "us-east4", "us-east5",
#     "us-south1", "us-west1", "us-west2", "us-west3", "us-west4"
# ]

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     selected_region = None
    
#     if request.method == 'POST':
#         # Get the selected region from the HTML form
#         selected_region = request.form.get('region')
        
#         # Print the selected value to the console/terminal
#         print(f"\n--- SUCCESS: User selected GCP Region: {selected_region} ---\n")

#     return render_template('index.html', regions=GCP_REGIONS, selected_region=selected_region)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host='0.0.0.0', port=port, debug=False)