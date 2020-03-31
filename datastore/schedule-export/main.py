import base64
import json
import os

from googleapiclient.discovery import build

datastore = build('datastore', 'v1')
project_id = os.environ.get('GCP_PROJECT')


def datastore_export(event, context):
    '''Trigger a Datastore export from a Cloud Scheduler message on a
    Cloud Pub/Sub topic.
    Args:
         event (dict): event[data] must contain a json object. Must include
         'bucket'. Can include 'kinds' and 'namespaceIds'.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    '''

    json_data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    bucket = json_data['bucket']
    entity_filter = {}

    if 'kinds' in json_data:
        entity_filter['kinds'] = json_data['kinds']

    if 'namespaceIds' in json_data:
        entity_filter['namespaceIds'] = json_data['namespaceIds']

    request_body = {
        'outputUrlPrefix': bucket,
        'entityFilter': entity_filter
        }

    export_request = datastore.projects().export(
        projectId=project_id,
        body=request_body
    )
    response = export_request.execute()
    print(response)
