# Introduction

This sample contains the code referenced in the 
[Sentiment Analysis Tutorial](http://cloud.google.com/natural-language/docs/sentiment-tutorial)
within the Google Cloud Natural Language API Documentation. A full walkthrough of this sample
is located within the documentation.

This sample is a simple illustration of how to construct a sentiment analysis
request and process a response using the API.

## Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).

2. Setup the gcloud tool. This provides authentication to Google Cloud APIs and services.

```
$ gcloud init
```


## Download the Code

```
$ git clone https://github.com/GoogleCloudPlatform/python-dev-samples/language/sentiment/
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
Sentiment: polarity of -0.1 with magnitude of 6.7
```
