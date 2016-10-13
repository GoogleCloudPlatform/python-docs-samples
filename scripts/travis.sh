#!/bin/bash

# Decrypt secrets if not on an external PR.
if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
    scripts/decrypt-secrets.sh "$SECRETS_PASSWORD"
fi

if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
     source ${TRAVIS_BUILD_DIR}/testing/test-env.sh;
     nox --stop-on-first-error -s lint travis;
else
    # only run lint on external PRs
    echo 'External PR: only running lint.'
    nox --stop-on-first-error -s lint;
fi
