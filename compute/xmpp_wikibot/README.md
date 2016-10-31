# Wikibot example that can be run on Google Compute Engine

This sample shows how to use the [SleekXMPP](http://sleekxmpp.com/index.html)
client and [Flask](http://flask.pocoo.org/) to build a simple chatbot that can
be run on [Google Compute Engine](https://cloud.google.com/compute/). The
chatbot does two things:

1. Sends messages to XMPP users via http get:
    * The server is running on port 5000
    * if running on virtual machine use:
    `http://<MACHINE IP>:5000/send_message?recipient=<RECIPIENT ADDRESS>&message=<MSG>`
    * If running locally use:
    `http://localhost:5000/send_message?recipient=<RECIPIENT ADDRESS>&message=<MSG>`

2. Responds to incoming messages with a Wikipedia page on the topic:
    * Send a message with a topic (e.g., 'Hawaii') to the XMPP account the
      server is using
    * It should respond with a Wikipedia page (when one exists)

## Setup

Follow the instructions at the
[Compute Engine Quickstart Guide](https://cloud.google.com/compute/docs/quickstart-linux)
on how to create a project, create a virtual machine, and connect to your
instance via SSH. Once you have done this, you may jump to
[Installing files and dependencies](#installing-files-and-dependencies).

You should also download the [Google Cloud SDK](https://cloud.google.com/sdk/).
It will allow you to access many of the features of Google Compute Engine via
your local machine.

**IMPORTANT** You must enable tcp traffic on port 5000 to send messages to the
XMPP server. This can be done by running the following SDK commands:

    gcloud config set project <YOUR PROJECT NAME>

    gcloud compute firewall-rules create wikibot-server-rule --allow tcp:5000 --source-ranges=0.0.0.0/0

Or you can create a new firewall rule via the UI in the
[Networks](https://console.cloud.google.com/networking/networks/list) section of
the Google Cloud Console.

### Installing files and dependencies

First, install the `wikibot.py` and `requirements.txt` files onto your remote
instance. See the guide on
[Transferring Files](https://cloud.google.com/compute/docs/instances/transfer-files)
for more information on how to do this using the Mac file browser, `scp`, or
the Google Cloud SDK.

Before running or deploying this application, you must install the dependencies
using [pip](http://pip.readthedocs.io/en/stable/):

    pip install -r requirements.txt


## Running the sample

You'll need to have an XMPP account prior to actually running the sample.
If you do not have one, you can easily create an account at one of the many
XMPP servers such as [xmpp.jp](http://xmpp.jp).
Once you have an account, run the following command:

    python wikibot.py -j '<YOUR XMPP USERNAME>' -p '<PASSWORD>'

Where the username (e.g., 'bob@xmpp.jp') and password for the account that
you'd like to use for your chatbot are passed in as arguments.

Enter control-C to stop the server


### Running on your local machine

You may also run the sample locally by simply copying `wikibot.py` to a project
directory and installing all python dependencies there.
