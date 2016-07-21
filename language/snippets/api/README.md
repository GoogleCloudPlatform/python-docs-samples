
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

For example, if you run:

```sh
$ python analyze.py entities "Tom Sawyer is a book written by a guy known as Mark Twain."
```

You will see something like the following returned:

```
{
  "entities": [
    {
      "salience": 0.49785897,
      "mentions": [
        {
          "text": {
            "content": "Tom Sawyer",
            "beginOffset": 0
          }
        }
      ],
      "type": "PERSON",
      "name": "Tom Sawyer",
      "metadata": {
        "wikipedia_url": "http://en.wikipedia.org/wiki/The_Adventures_of_Tom_Sawyer"
      }
    },
    {
      "salience": 0.12209519,
      "mentions": [
        {
          "text": {
            "content": "Mark Twain",
            "beginOffset": 47
          }
        }
      ],
      "type": "PERSON",
      "name": "Mark Twain",
      "metadata": {
        "wikipedia_url": "http://en.wikipedia.org/wiki/Mark_Twain"
      }
    }
  ],
  "language": "en"
}
```
