"""Sample appengine app demonstrating 3-legged oauth."""
import cgi
import json
import os
import sys

from flask import Flask

from googleapiclient.discovery import build

from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

# The project id whose datasets you'd like to list
PROJECTID = '<myproject_id>'

# Create the method decorator for oauth.
decorator = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    scope='https://www.googleapis.com/auth/bigquery')

# Create the bigquery api client
service = build('bigquery', 'v2')

# Create the Flask app
app = Flask(__name__)
app.config['DEBUG'] = True

# Create the endpoint to receive oauth flow callbacks
app.route(decorator.callback_path)(decorator.callback_handler())


@app.route('/')
@decorator.oauth_required
def list_datasets():
    """Lists the datasets in PROJECTID"""
    http = decorator.http()
    datasets = service.datasets()

    try:
        response = datasets.list(projectId=PROJECTID).execute(http)

        return ('<h3>Datasets.list raw response:</h3>'
                '<pre>%s</pre>' % json.dumps(response, sort_keys=True,
                                             indent=4, separators=(',', ': ')))
    except:
        e = cgi.escape(sys.exc_info()[0], True)
        return '<p>Error: %s</p>' % e
