# From apache/beam_python3.9_sdk:2.43.0
FROM apache/beam_python3.9_sdk@sha256:5582620a9e542564a428682d0262d97bb467d5a0536af0ca99b59eea8f3dfbfb

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
