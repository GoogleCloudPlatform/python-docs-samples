# Using the Cloud Natural Language API to find subject-verb-object triples in text

This example finds subject-verb-object triples in a given piece of text using
syntax analysis capabilities of
[Cloud Natural Language API](https://cloud.google.com/natural-language/).
To do this, it calls the extractSyntax feature of the API
and uses the dependency parse tree and part-of-speech tags in the resposne
to build the subject-verb-object triples. The results are printed to STDOUT.
This type of analysis can be considered as the
first step towards an information extraction task.

## Set Up to Authenticate With Your Project's Credentials

Please follow the [Set Up Your Project](https://cloud.google.com/natural-language/docs/getting-started#set_up_your_project)
steps in the Quickstart doc to create a project and enable the
Cloud Natural Language API. Following those steps, make sure that you
[Set Up a Service Account](https://cloud.google.com/natural-language/docs/common/auth#set_up_a_service_account),
and export the following environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json
```

## Running the example

Install [pip](https://pip.pypa.io/en/stable/installing) if not already installed.

To run the example, install the necessary libraries using pip:

```
$ pip install -r requirements.txt
```
You must also be set up to authenticate with the Cloud APIs using your
project's service account credentials, as described above.

Then, run the script on a file containing the text that you wish to analyze.
The text must be encoded in UTF8 or ASCII:

```
$ python main.py <path-to-text-file>
```

Try this on a sample text in the resources directory:

```
$ python main.py resources/obama_wikipedia.txt
```

## A walkthrough of the example and its results

Let's take a look at what the example generates when run on the
`obama_wikipedia.txt` sample file, and how it does it.

The goal is to find all subject-verb-object
triples in the text. The example first sends the text to the Cloud Natural
Language API to perform extractSyntax analysis. Then, using part-of-speech tags,
 it finds all the verbs in the text. For each verb, it uses the dependency
parse tree information to find all the dependent tokens.

For example, given the following sentence in the `obama_wikipedia.txt` file:

```
"He began his presidential campaign in 2007"
```
The example finds the verb `began`, and `He`, `campaign`, and `in` as its
dependencies. Then the script enumerates the dependencies for each verb and
finds all the subjects and objects. For the sentence above, the found subject
and object are `He` and `campaign`.

The next step is to complete each subject and object token by adding their
dependencies to them. For example, in the sentence above, `his` and
`presidential` are dependent tokens for `campaign`. This is done using the
dependency parse tree, similar to verb dependencies as explained above. The
final result is (`He`, `began`, `his presidential campaign`) triple for
the example sentence above.

The script performs this analysis for the entire text and prints the result.
For the `obama_wikipedia.txt` file, the result is the following:

```sh
+------------------------------+------------+------------------------------+
| Obama                        | received   | national attention           |
+------------------------------+------------+------------------------------+
| He                           | began      | his presidential campaign    |
+------------------------------+------------+------------------------------+
| he                           | won        | sufficient delegates in the  |
|                              |            | Democratic Party primaries   |
+------------------------------+------------+------------------------------+
| He                           | defeated   | Republican nominee John      |
|                              |            | McCain                       |
```
