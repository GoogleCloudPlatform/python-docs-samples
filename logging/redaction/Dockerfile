# From apache/beam_python3.9_sdk:2.43.0
FROM apache/beam_python3.9_sdk@sha256:015dc70d239475fc8e193e1c55c54b89d1ca9e771e05aadec1037f2f13fbdbbb

# Install google-cloud-logging package that is missing in Beam SDK
COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && pip3 check
