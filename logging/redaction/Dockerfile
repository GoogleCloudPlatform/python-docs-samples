# From apache/beam_python3.9_sdk:2.43.0
FROM apache/beam_python3.9_sdk@sha256:372abe1d342447118d517ed1325969115e2df03f09fc7604e606c7552380b2ce

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
