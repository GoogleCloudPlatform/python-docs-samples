# From apache/beam_python3.9_sdk:2.43.0
FROM apache/beam_python3.9_sdk@sha256:497a6151928ce5b6cfe59a403944500ac02b7aa7f1f8f2e5304b0a845358fc93

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
