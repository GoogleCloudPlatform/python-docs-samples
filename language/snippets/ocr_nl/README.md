
# Using the Cloud Natural Language API to analyze image text found with Cloud Vision

This example uses the [Cloud Vision API](https://cloud.google.com/vision/) to
detect text in images, then analyzes that text using the [Cloud NL (Natural
Language) API](https://cloud.google.com/natural-language/) to detect
[entities](https://cloud.google.com/natural-language/docs/basics#entity_analysis)
in the text. It stores the detected entity
information in an [sqlite3](https://www.sqlite.org) database, which may then be
queried.

(This kind of analysis can be useful with scans of brochures and fliers,
invoices, and other types of company documents... or maybe just organizing your
memes).

After the example script has analyzed a directory of images, it outputs some
information on the images' entities to STDOUT. You can also further query
the generated sqlite3 database.

## Setup

### Install sqlite3 as necessary

The example requires that sqlite3 be installed. Most likely, sqlite3 is already
installed for you on your machine, but if not, you can find it
[here](https://www.sqlite.org/download.html).

### Set Up to Authenticate With Your Project's Credentials

* Please follow the [Set Up Your Project](https://cloud.google.com/natural-language/docs/getting-started#set_up_your_project)
steps in the Quickstart doc to create a project and enable the
Cloud Natural Language API.
* Following those steps, make sure that you [Set Up a Service
  Account](https://cloud.google.com/natural-language/docs/common/auth#set_up_a_service_account),
  and export the following environment variable:

    ```
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json
    ```
* This sample also requires that you [enable the Cloud Vision
  API](https://console.cloud.google.com/apis/api/vision.googleapis.com/overview?project=_)

## Running the example

Install [pip](https://pip.pypa.io/en/stable/installing) if not already installed.

To run the example, install the necessary libraries using pip:

```sh
$ pip install -r requirements.txt
```

You must also be set up to authenticate with the Cloud APIs using your
project's service account credentials, as described above.

Then, run the script on a directory of images to do the analysis, E.g.:

```sh
$ python main.py --input_directory=<path-to-image-directory>
```

You can try this on a sample directory of images:

```sh
$ curl -O http://storage.googleapis.com/python-docs-samples-tests/language/ocr_nl-images.zip
$ unzip ocr_nl-images.zip
$ python main.py --input_directory=images/
```

## A walkthrough of the example and its results

Let's take a look at what the example generates when run on the `images/`
sample directory, and how it does it.

The script looks at each image file in the given directory, and uses the Vision
API's text detection capabilities (OCR) to find any text in each image.  It
passes that info to the NL API, and asks it to detect [entities](xxx) in the
discovered text, then stores this information in a queryable database.

To keep things simple, we're just passing to the NL API all the text found in a
given image, in one string. Note that sometimes this string can include
misinterpreted characters (if the image text was not very clear), or list words
"out of order" from how a human would interpret them. So, the text that is
actually passed to the NL API might not be quite what you would have predicted
with your human eyeballs.

The Entity information returned by the NL API includes *type*, *name*, *salience*,
information about where in the text the given entity was found, and detected
language.  It may also include *metadata*, including a link to a Wikipedia URL
that the NL API believes this entity maps to.  See the
[documentation](https://cloud.google.com/natural-language/docs/) and the [API
reference pages](https://cloud.google.com/natural-language/reference/rest/v1beta1/Entity)
for more information about `Entity` fields.

For example, if the NL API was given the sentence:

```
"Holmes and Watson walked over to the cafe."
```

it would return a response something like the following:

```
{
  "entities": [{
      "salience": 0.51629782,
      "mentions": [{
          "text": {
            "content": "Holmes",
            "beginOffset": 0
          }}],
      "type": "PERSON",
      "name": "Holmes",
      "metadata": {
        "wikipedia_url": "http://en.wikipedia.org/wiki/Sherlock_Holmes"
      }},
    {
      "salience": 0.22334209,
      "mentions": [{
          "text": {
            "content": "Watson",
            "beginOffset": 11
          }}],
      "type": "PERSON",
      "name": "Watson",
      "metadata": {
        "wikipedia_url": "http://en.wikipedia.org/wiki/Dr._Watson"
      }}],
  "language": "en"
}
```

Note that the NL API determined from context that "Holmes" was referring to
'Sherlock Holmes', even though the name "Sherlock" was not included.

Note also that not all nouns in a given sentence are detected as Entities. An
Entity represents a phrase in the text that is a known entity, such as a person,
an organization, or location. The generic mention of a 'cafe' is not treated as
an entity in this sense.

For each image file, we store its detected entity information (if any) in an
sqlite3 database.

### Querying for information about the detected entities

Once the detected entity information from all the images is stored in the
sqlite3 database, we can run some queries to do some interesting analysis.  The
script runs a couple of such example query sets and outputs the result to STDOUT.

The first set of queries outputs information about the top 15 most frequent
entity names found in the images, and the second outputs information about the
top 15 most frequent Wikipedia URLs found.

For example, with the sample image set, note that the name 'Sherlock Holmes' is
found three times, but entities associated with the URL
http://en.wikipedia.org/wiki/Sherlock_Holmes are found four times; one of the
entity names was only "Holmes", but the NL API detected from context that it
referred to Sherlock Holmes. Similarly, you can see that mentions of 'Hive' and
'Spark' mapped correctly – given their context – to the URLs of those Apache
products.

```
----entity: http://en.wikipedia.org/wiki/Apache_Hive was found with count 1
Found in file images/IMG_20160621_133020.jpg, detected as type OTHER, with
  locale en.
names(s): set([u'hive'])
salience measure(s): set([0.0023808887])
```

Similarly, 'Elizabeth' (in screencaps of text from "Pride and Prejudice") is
correctly mapped to http://en.wikipedia.org/wiki/Elizabeth_Bennet because of the
context of the surrounding text.

```
----entity: http://en.wikipedia.org/wiki/Elizabeth_Bennet was found with count 2
Found in file images/Screenshot 2016-06-19 11.51.50.png, detected as type PERSON, with
  locale en.
Found in file images/Screenshot 2016-06-19 12.08.30.png, detected as type PERSON, with
  locale en.
names(s): set([u'elizabeth'])
salience measure(s): set([0.34601286, 0.0016268975])
```

## Further queries to the sqlite3 database

When the script runs, it makes a couple of example queries to the database
containing the entity information returned from the NL API. You can make further
queries on that database by starting up sqlite3 from the command line, and
passing it the name of the database file generated by running the example.  This
file will be in the same directory, and have `entities` as a prefix, with the
timestamp appended. (If you have run the example more than once, a new database
file will be created each time).

Run sqlite3 as follows (using the name of your own database file):

```sh
$ sqlite3 entities1466518508.db
```

You'll see something like this:

```
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
sqlite>
```

From this prompt, you can make any queries on the data that you want.  E.g.,
start with something like:

```
sqlite> select * from entities limit 20;
```

Or, try this to see in which images the most entities were detected:

```
sqlite> select filename, count(filename) from entities group by filename;
```

You can do more complex queries to get further information about the entities
that have been discovered in your images.  E.g., you might want to investigate
which of the entities are most commonly found together in the same image. See
the [SQLite documentation](https://www.sqlite.org/docs.html) for more
information.


