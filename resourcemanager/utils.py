from time import sleep

from googleapiclient.discovery import build
import httplib2
from oauth2client.client import GoogleCredentials


def build_client():
    return build('cloudresourcemanager',
                 'v1beta1',
                 credentials=GoogleCredentials.get_application_default(),
                 # Use long timeout for create requests
                 http=httplib2.Http(timeout=90))


def wait_for_active(client, project):
    timeout = 1
    while project['lifecycleState'] != 'ACTIVE':
        sleep(timeout)
        timeout = timeout*2
        project = client.projects().get(
            projectId=project['projectId']
            ).execute()
    return project
