import base64
import json
import re
import google.auth
import google.auth.transport.requests
import requests
import uuid


def retry_bigquery_query(event, context):
   """Retries a failed BigQuery continuous query.


   Args:
       event (dict):  The dictionary with data specific to this type of
           event. The `data` field contains the PubsubMessage message. The
           `attributes` field will contain custom attributes if there are any.
       context (google.cloud.functions.Context): The Cloud Functions event
           metadata. The `event_id` field contains the Pub/Sub message ID.
           The `timestamp` field contains the publish time.
   """
   if 'data' in event:
       try:
           # Decode and parse the Pub/Sub message data (LogEntry)
           log_entry = json.loads(base64.b64decode(event['data']).decode('utf-8'))


           # Check if 'protoPayload' exists
           if 'protoPayload' in log_entry:
               # Extract the SQL query
               sql_query = log_entry['protoPayload']['metadata']['jobChange']['job']['jobConfig']['queryConfig']['query']
              
           # Record Job ID that failed and will attempt to be restarted
           failed_job_id = log_entry['protoPayload']['metadata']['jobChange']['job']['jobName']
           print(f"Retrying failed job: {failed_job_id}")
          
           # Extract the endTime from the log entry
           end_timestamp = log_entry['protoPayload']['metadata']['jobChange']['job']['jobStats']['endTime']


           # Check if the start_timestamp is "CURRENT_TIMESTAMP - INTERVAL 10 MINUTE"
           if "CURRENT_TIMESTAMP - INTERVAL 10 MINUTE" in sql_query:
               # If it is, replace it with the endTime from the previous job + INTERVAL 1 MICROSECOND
               new_timestamp_str = f"TIMESTAMP('{end_timestamp}') + INTERVAL 1 MICROSECOND"
               sql_query = sql_query.replace("CURRENT_TIMESTAMP - INTERVAL 10 MINUTE", new_timestamp_str)
          
           # If the start_timestamp is an explicit timestamp
           else:
               # Extract the APPENDS TVF timestamp from the previous job's FROM statement
               match = re.search(r"\s*TIMESTAMP\(('.*?')\)(\s*\+ INTERVAL 1 MICROSECOND)?", sql_query)
               if match:
                   # Extract the original timestamp value
                   original_timestamp = match.group(1)


                   # Create the new timestamp string
                   new_timestamp_str = f"'{end_timestamp}'"


                   # Replace only the timestamp part
                   sql_query = sql_query.replace(original_timestamp, new_timestamp_str)
          
           # Get access token
           credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
           request = google.auth.transport.requests.Request()
           credentials.refresh(request)
           access_token = credentials.token


           # API endpoint
           url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/jobs"


           # Request headers
           headers = {
               "Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"
           }


           # Generate a random UUID
           random_suffix = str(uuid.uuid4())[:8]  # Take the first 8 characters of the UUID


           # Combine the prefix and random suffix
           job_id = f"continuous_query_label_{random_suffix}"


           # Request payload
           data = {
               "configuration": {
                   "query": {
                       "query": sql_query,
                       "useLegacySql": False,
                       "continuous": True,
                       "connectionProperties":[{"key":"service_account","value":"SERVICE_ACCOUNT"}]
                       # ... other query parameters ...
                   },
                   "labels": {
                           "bqux_job_id_prefix": "CUSTOM_JOB_ID_PREFIX"
                       }
               },
               "jobReference": {
                       "projectId": project,
                       "jobId": job_id  # Use the generated job ID here
                   }
           }


           # Make the API request
           response = requests.post(url, headers=headers, json=data)


           # Handle the response
           if response.status_code == 200:
               print("Query job successfully created.")
           else:
               print(f"Error creating query job: {response.text}")


       except Exception as e:
           print(f"Error processing log entry or retrying query: {e}")
   else:
       print("No data in Pub/Sub message.")
