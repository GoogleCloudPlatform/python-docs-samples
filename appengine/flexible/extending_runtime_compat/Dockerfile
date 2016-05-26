# Extend the App Engine Flexible python-compat runtime.
FROM gcr.io/google_appengine/python-compat-multicore

# Install the fortunes binary from the debian repositories.
RUN apt-get update && apt-get install -y fortunes

ADD . /app/

RUN if [ -s requirements.txt ]; then pip install -r requirements.txt; fi
