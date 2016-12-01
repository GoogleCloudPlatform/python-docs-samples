#!/bin/bash

# Decrypt secrets and run tests if not on an external PR.
if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
    scripts/decrypt-secrets.sh "$SECRETS_PASSWORD"
    source ${TRAVIS_BUILD_DIR}/testing/test-env.sh;
    export GOOGLE_APPLICATION_CREDENTIALS=${TRAVIS_BUILD_DIR}/testing/service-account.json
    export GOOGLE_CLIENT_SECRETS=${TRAVIS_BUILD_DIR}/testing/client-secrets.json
    nox --stop-on-first-error -s lint gae py35 -- -m "not slow";
else
    # only run lint on external PRs
    echo 'External PR: only running lint.'
    nox --stop-on-first-error -s lint;
fi
