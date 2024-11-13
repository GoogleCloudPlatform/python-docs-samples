# From apache/beam_python3.9_sdk:2.43.0
FROM apache/beam_python3.9_sdk@sha256:0cb6eceed3652d01dd5a555fd9ff4eff5df62161dd99ad53fe591858bdb57741

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
