# Introduction

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=language/sentiment/README.md

This sample contains the code referenced in the 
[Sentiment Analysis Tutorial](http://cloud.google.com/natural-language/docs/sentiment-tutorial)
within the Google Cloud Natural Language API Documentation. A full walkthrough of this sample
is located within the documentation.

This sample is a simple illustration of how to construct a sentiment analysis
request and process a response using the API.

## Prerequisites

Set up your 
[Cloud Natural Language API project](https://cloud.google.com/natural-language/docs/getting-started#set_up_a_project)
, which includes:

* Enabling the Natural Language API
* Setting up a service account
* Ensuring you've properly set up your `GOOGLE_APPLICATION_CREDENTIALS` for proper
    authentication to the service.

## Download the Code

```
$ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
$ cd python-docs-samples/language/sentiment
```

## Run the Code

Open a sample folder, create a virtualenv, install dependencies, and run the sample:

```
$ virtualenv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```

### Usage

This sample provides four sample movie reviews which you can
provide to the sample on the command line. (You can also
pass your own text files.)

```
(env)$ python sentiment_analysis.py textfile.txt
Sentiment: score of -0.1 with magnitude of 6.7
```
