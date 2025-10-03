FROM apache/beam_python3.9_sdk@sha256:246c4b813c6de8c240b49ed03c426f413f1768321a3c441413031396a08912f9

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
