#!/usr/bin/env python

# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple application that performs a query with BigQuery and
    writes results to a Google Sheet"""

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import bigquery


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/bigquery',
          'https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1Y-dnHRKYGfirhJOfHUO_jDZ9ke7Q5FwPwXdt6VjjaG0'
SPREADSHEET_RANGE = 'Sheet1!A:Z'
VALUE_INPUT_OPTION = 'RAW'


def query_sample():
    client = bigquery.Client()
    sql = """

    SELECT
      CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10
           """

    # Pandas DataFrame to hold sql results
    df = client.query(sql).to_dataframe()
    write_to_sheets(df)


def write_to_sheets(df):
    creds = None

    # End-User Authentication
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # Change PATH_TO_CLIENT_SECRETS.JSON to Client_Secrets.json path
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'PATH_TO_CLIENT_SECRETS.JSON', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    #  Creates list of column names
    column_list = list(df)

    # Append column_list to empty value_list to match sheets api format
    # [['url', 'view_count']]
    value_list = [column_list]

    # Convert DataFrame values to list
    data = df.values.tolist()
    # Extend data list to headers list
    value_list.extend(data)

    # Create ValueRange object
    body = {'values': value_list}
    # Call the Google Sheets API and write sql results to sheet
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=SPREADSHEET_RANGE,
        valueInputOption=VALUE_INPUT_OPTION, body=body).execute()

    print('{} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    query_sample()
