import sys
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import httplib2

# for python3 compat
raw_input = vars(__builtins__).get('raw_input', input)

FLOW = OAuth2WebServerFlow(
    client_id='xxxxxxx.apps.googleusercontent.com',
    client_secret='shhhhhhhhhhhh',
    scope='https://www.googleapis.com/auth/bigquery',
    user_agent='my-program-name/1.0')


def loadTable(http, service):
    projectId = raw_input('Choose your project ID: ')
    datasetId = raw_input('Choose a dataset ID: ')
    tableId = raw_input('Choose a table name to load the data to: ')

    url = ('https://www.googleapis.com/upload/bigquery/v2/projects/' +
           projectId + '/jobs')
    newSchemaFile = raw_input('What is your schema? ')
    schema = open(newSchemaFile, 'r')

    # Create the body of the request, separated by a boundary of xxx
    newresource = ('--xxx\n' +
                   'Content-Type: application/json; charset=UTF-8\n' + '\n' +
                   '{\n' +
                   '   "configuration": {\n' +
                   '     "load": {\n' +
                   '       "schema": {\n'
                   '         "fields": ' + schema.read() + '\n' +
                   '      },\n' +
                   '      "destinationTable": {\n' +
                   '        "projectId": "' + projectId + '",\n' +
                   '        "datasetId": "' + datasetId + '",\n' +
                   '        "tableId": "' + tableId + '"\n' +
                   '      }\n' +
                   '    }\n' +
                   '  }\n' +
                   '}\n' +
                   '--xxx\n' +
                   'Content-Type: application/octet-stream\n' +
                   '\n')
    newDataFile = raw_input('What is your data? ')

    # Append data from the specified file to the request body
    f = open(newDataFile, 'r')
    newresource += f.read()

    # Signify the end of the body
    newresource += ('--xxx--\n')

    headers = {'Content-Type': 'multipart/related; boundary=xxx'}
    resp, content = http.request(url, method='POST',
                                 body=newresource, headers=headers)

    if resp.status == 200:
        jsonResponse = json.loads(content)
    jobReference = jsonResponse['jobReference']['jobId']
    import time
    while True:
        jobCollection = service.jobs()
    getJob = jobCollection.get(projectId=projectId,
                               jobId=jobReference).execute()
    currentStatus = getJob['status']['state']

    if 'DONE' == currentStatus:
        print('Done Loading!')
        return
    else:
        print('Waiting to load...')
    print('Current status: ' + currentStatus)
    print(time.ctime())
    time.sleep(10)


def main(argv):
    # If the credentials don't exist or are invalid, run the native client
    # auth flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    #
    # Choose a file name to store the credentials.
    storage = Storage('bigquery2.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests
    # and authorize it with our good credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('bigquery', 'v2', http=http)

    loadTable(http, service)

if __name__ == '__main__':
    main(sys.argv)
