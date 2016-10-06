# Tic Tac Toe, using Firebase, on App Engine Standard

This sample shows how to use the [Firebase](https://firebase.google.com/)
realtime database to implement a simple Tic Tac Toe game on [Google App Engine
Standard](https://cloud.google.com/appengine).

## Setup

### Authentication

* Create a project in the [Firebase console](https://firebase.google.com/console)
* Retrieve two sets of credentials from the Firebase console:
    * In the Overview section, click 'Add Firebase to your web app' and replace
      the file
      [`templates/_firebase_config.html`](templates/_firebase_config.html) with
      the given snippet. This provides credentials for the javascript client.
    * Click the gear icon and head to 'Permissions'; then click the 'Service
      accounts' tab. Download a new or existing App Engine service account
      credentials file, and replace the file
      [`credentials.json`](credentials.json) with this file. This allows the
      server to securely create unique tokens for each user, that Firebase can
      validate.

### Install dependencies

Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -t lib -r requirements.txt

## Running the sample

    dev_appserver.py .

For more information on running or deploying the sample, see the [App Engine
Standard README](../../README.md).
