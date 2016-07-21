# Introduction
This sample is an application of the Google Cloud Platform Natural Language API.
It uses the [imdb movie reviews data set](https://www.cs.cornell.edu/people/pabo/movie-review-data/) 
from [Cornell University](http://www.cs.cornell.edu/) and performs sentiment & entity
analysis on it. It combines the capabilities of sentiment analysis and entity recognition
to come up with actors/directors who are the most and least popular.

### Set Up to Authenticate With Your Project's Credentials

Please follow the [Set Up Your Project](https://cloud.google.com/natural-language/docs/getting-started#set_up_your_project)
steps in the Quickstart doc to create a project and enable the
Cloud Natural Language API. Following those steps, make sure that you
[Set Up a Service Account](https://cloud.google.com/natural-language/docs/common/auth#set_up_a_service_account),
and export the following environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json
```

**Note:** If you get an error saying your API hasn't been enabled, make sure
that you have correctly set this environment variable, and that the project that
you got the service account from has the Natural Language API enabled.

## How it works
This sample uses the Natural Language API to annotate the input text. The
movie review document is broken into sentences using the `extract_syntax` feature. 
Each sentence is sent to the API for sentiment analysis. The positive and negative
sentiment values are combined to come up with a single overall sentiment of the
movie document.

In addition to the sentiment, the program also extracts the entities of type
`PERSON`, who are the actors in the movie (including the director and anyone
important). These entities are assigned the sentiment value of the document to
come up with the most and least popular actors/directors.

### Movie document
We define a movie document as a set of reviews. These reviews are individual
sentences and we use the NL API to extract the sentences from the document. See
an example movie document below.

```
  Sample review sentence 1. Sample review sentence 2. Sample review sentence 3.
```

### Sentences and Sentiment
Each sentence from the above document is assigned a sentiment as below.

```
  Sample review sentence 1 => Sentiment 1
  Sample review sentence 2 => Sentiment 2
  Sample review sentence 3 => Sentiment 3
```

### Sentiment computation
The final sentiment is computed by simply adding the sentence sentiments.

```
  Total Sentiment = Sentiment 1 + Sentiment 2 + Sentiment 3
```


### Entity extraction and Sentiment assignment
Entities with type `PERSON` are extracted from the movie document using the NL
API. Since these entities are mentioned in their respective movie document,
they are associated with the document sentiment.

```
  Document 1 => Sentiment 1

  Person 1
  Person 2
  Person 3

  Document 2 => Sentiment 2

  Person 2
  Person 4
  Person 5
```

Based on the above data we can calculate the sentiment associated with Person 2:

```
  Person 2 => (Sentiment 1 + Sentiment 2)
```

## Movie Data Set
We have used the Cornell Movie Review data as our input. Please follow the instructions below to download and extract the data.

### Download Instructions

```
 $ curl -O http://www.cs.cornell.edu/people/pabo/movie-review-data/mix20_rand700_tokens.zip
 $ unzip mix20_rand700_tokens.zip
```

## Command Line Usage
In order to use the movie analyzer, follow the instructions below. (Note that the `--sample` parameter below runs the script on
fewer documents, and can be omitted to run it on the entire corpus)

### Install Dependencies

Install [pip](https://pip.pypa.io/en/stable/installing) if not already installed.

Then, install dependencies by running the following pip command:

```
$ pip install -r requirements.txt
```
### How to Run

```
$ python main.py analyze --inp "tokens/*/*" \
                 --sout sentiment.json \
                 --eout entity.json \
                 --sample 5
```

You should see the log file `movie.log` created.

## Output Data
The program produces sentiment and entity output in json format. For example:

### Sentiment Output
```
  {
    "doc_id": "cv310_tok-16557.txt",
    "sentiment": 3.099,
    "label": -1
  }
```

### Entity Output

```
  {
    "name": "Sean Patrick Flanery",
    "wiki_url": "http://en.wikipedia.org/wiki/Sean_Patrick_Flanery",
    "sentiment": 3.099
  }
```

### Entity Output Sorting
In order to sort and rank the entities generated, use the same `main.py` script. For example,
this will print the top 5 actors with negative sentiment:

```
$ python main.py rank --entity_input entity.json \
                 --sentiment neg \
                 --reverse True \
                 --sample 5
```
