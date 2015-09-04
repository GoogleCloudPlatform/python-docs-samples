#!/bin/bash

set -ev

# Install Google App Engine Python SDK
if [[ ! -d "${GAE_PYTHONPATH}" ]]; then
  python tests/scripts/fetch_gae_sdk.py `dirname "${GAE_PYTHONPATH}"`
fi

# Google Cloud Service account key.
# ENCRYPT YOUR PRIVATE KEY (If you need authentication)
# 1. Install and login to the Travis CLI:
#       $ gem install travis
#       $ travis login
# 2. Move your json private key to client_secrets.json
# 3. Run:
#       $ travis encrypt-file client_secrets.json --add
# 4. Commit changes:
#       $ git add client_secrets.json.enc
#       $ git commit client_secrets.json.enc .travis.yml
openssl aes-256-cbc \
    -K $encrypted_4fda24e244ca_key \
    -iv $encrypted_4fda24e244ca_iv \
    -in ${TRAVIS_BUILD_DIR}/python-docs-samples.json.enc \
    -out ${TRAVIS_BUILD_DIR}/python-docs-samples.json -d
