# Introduction

This sample contains the code referenced in the 
[Text Classification Tutorial](http://cloud.google.com/natural-language/docs/classify-text-tutorial) within the Google Cloud Natural Language API Documentation. A full walkthrough of this sample is located within the documentation.

This sample shows how one can use the text classification feature of the Natural Language API to find similar texts based on a query.

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
$ cd python-docs-samples/language/classify_text
```

## Run the Code

Open a sample folder, create a virtualenv, install dependencies, and run the sample:

```
$ virtualenv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```

### Usage

This sample is organized as a script runnable from the command line.  It can perform the following tasks:

   * Classifies multiple text files and write the result to an "index" file.
   * Processes input query text to find similar text files.
   * Processes input query category label to find similar text files.

## Classify text

```
python classify_text_tutorial.py classify "$(cat resources/query_text.txt)"
```

Note that the text needs to be sufficiently long for the API to return a non-empty
response.

## Index mulitple text files

```
python classify_text_tutorial.py index resources/texts
```

By default this creates a file `index.json`, which you can specify by passing in the optional `--index_file` argument.

## Query with a category label

The indexed text files can be queried with any of the category labels listed on the [Categories](https://cloud.google.com/natural-language/docs/categories) page.

```
python classify_text_tutorial.py query-category index.json "/Internet & Telecom/Mobile & Wireless"
```

## Query with text

The indexed text files can be queried with another text that might not have been indexed.

```
python classify_text_tutorial.py query index.json "$(cat resources/query_text.txt)"
```





