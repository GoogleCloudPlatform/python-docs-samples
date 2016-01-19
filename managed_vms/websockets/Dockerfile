FROM gcr.io/google_appengine/python

# Change the -p argument to use Python 2.7 if desired.
RUN virtualenv /env -p python3.4

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

# Use a special gunicorn worker class to support websockets.
CMD gunicorn -b :$PORT -b :65080 -k flask_sockets.worker main:app
