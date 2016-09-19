# Google Cloud Natural Language API examples

This directory contains Python examples that use the
[Google Cloud Natural Language API](https://cloud.google.com/natural-language/).

- [api](api) has a simple command line tool that shows off the API's features.

- [movie_nl](movie_nl) combines sentiment and entity analysis to come up with
actors/directors who are the most and least popular in the imdb movie reviews.

- [ocr_nl](ocr_nl) uses the [Cloud Vision API](https://cloud.google.com/vision/)
to extract text from images, then uses the NL API to extract entity information
from those texts, and stores the extracted information in a database in support
of further analysis and correlation.

- [sentiment](sentiment) contains the [Sentiment Analysis
  Tutorial](https://cloud.google.com/natural-language/docs/sentiment-tutorial)
code as used within the documentation.

- [syntax_triples](syntax_triples) uses syntax analysis to find
subject-verb-object triples in a given piece of text.
