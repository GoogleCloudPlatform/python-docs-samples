
# Google Cloud Natural Language API Sample

This Python sample demonstrates the use of the [Google Cloud Natural Language API][NL-Docs]
for sentiment, entity, and syntax analysis.

[NL-Docs]: https://cloud.google.com/natural-language/docs/

## Setup

Please follow the [Set Up Your Project](https://cloud.google.com/natural-language/docs/getting-started#set_up_your_project)
steps in the Quickstart doc to create a project and enable the
Cloud Natural Language API. Following those steps, make sure that you
[Set Up a Service Account](https://cloud.google.com/natural-language/docs/common/auth#set_up_a_service_account),
and export the following environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json
```

## Run the sample

Install [pip](https://pip.pypa.io/en/stable/installing) if not already installed.

To run the example, install the necessary libraries using pip:

```sh
$ pip install -r requirements.txt
```

Then, run the script:

```sh
$ python analyze.py <command> <text-string>
```

where `<command>` is one of:  `entities`, `sentiment`, or `syntax`.

The script will write to STDOUT the json returned from the API for the requested feature.

* Example1:

```sh
$ python analyze.py entities "Tom Sawyer is a book written by a guy known as Mark Twain."
```

You will see something like the following returned:

```
{
  "entities": [
    {
      "salience": 0.50827783,
      "mentions": [
        {
          "text": {
            "content": "Tom Sawyer",
            "beginOffset": 0
          },
          "type": "PROPER"
        }
      ],
      "type": "PERSON",
      "name": "Tom Sawyer",
      "metadata": {
        "mid": "/m/01b6vv",
        "wikipedia_url": "http://en.wikipedia.org/wiki/The_Adventures_of_Tom_Sawyer"
      }
    },
    {
      "salience": 0.22226454,
      "mentions": [
        {
          "text": {
            "content": "book",
            "beginOffset": 16
          },
          "type": "COMMON"
        }
      ],
      "type": "WORK_OF_ART",
      "name": "book",
      "metadata": {}
    },
    {
      "salience": 0.18305534,
      "mentions": [
        {
          "text": {
            "content": "guy",
            "beginOffset": 34
          },
          "type": "COMMON"
        }
      ],
      "type": "PERSON",
      "name": "guy",
      "metadata": {}
    },
    {
      "salience": 0.086402282,
      "mentions": [
        {
          "text": {
            "content": "Mark Twain",
            "beginOffset": 47
          },
          "type": "PROPER"
        }
      ],
      "type": "PERSON",
      "name": "Mark Twain",
      "metadata": {
        "mid": "/m/014635",
        "wikipedia_url": "http://en.wikipedia.org/wiki/Mark_Twain"
      }
    }
  ],
  "language": "en"
}
```

* Example2:

```sh
$ python analyze.py entities "Apple has launched new iPhone."
```

You will see something like the following returned:

```
{
  "entities": [
    {
      "salience": 0.72550339,
      "mentions": [
        {
          "text": {
            "content": "Apple",
            "beginOffset": 0
          },
          "type": "PROPER"
        }
      ],
      "type": "ORGANIZATION",
      "name": "Apple",
      "metadata": {
        "mid": "/m/0k8z",
        "wikipedia_url": "http://en.wikipedia.org/wiki/Apple_Inc."
      }
    },
    {
      "salience": 0.27449661,
      "mentions": [
        {
          "text": {
            "content": "iPhone",
            "beginOffset": 23
          },
          "type": "PROPER"
        }
      ],
      "type": "CONSUMER_GOOD",
      "name": "iPhone",
      "metadata": {
        "mid": "/m/027lnzs",
        "wikipedia_url": "http://en.wikipedia.org/wiki/IPhone"
      }
    }
  ],
  "language": "en"
}
```
