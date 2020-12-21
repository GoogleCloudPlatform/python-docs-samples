FROM tensorflow/tensorflow:2.3.1-gpu

WORKDIR /root

# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`.
COPY requirements.txt .

# Don't install `tensorflow` since the base image already comes with it.
RUN egrep -v '^tensorflow([=<>]|$)' requirements.txt > /tmp/requirements.txt \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the worker boot file from the beam image.
COPY --from=apache/beam_python3.6_sdk /opt/apache/beam/boot /opt/apache/beam/boot

# Set the entrypoint to the worker boot file.
ENTRYPOINT [ "/opt/apache/beam/boot" ]
