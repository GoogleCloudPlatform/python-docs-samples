# The Google Cloud Platform Python runtime is based on Debian Jessie
# You can read more about the runtime at:
#   https://github.com/GoogleCloudPlatform/python-runtime
FROM gcr.io/google_appengine/python

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV -p python3.5 /env
ENV PATH /env/bin:$PATH

COPY requirements.txt /app/
RUN pip install --requirement /app/requirements.txt
COPY . /app/

ENTRYPOINT []

CMD ["python", "/app/greeter_server.py"]
