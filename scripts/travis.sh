#!/bin/bash

# Decrypt secrets if not on an external PR.
if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
    openssl aes-256-cbc -k "$secrets_password" -in secrets.tar.enc -out secrets.tar -d;
    tar xvf secrets.tar;
fi

if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
     source ${TRAVIS_BUILD_DIR}/testing/resources/test-env.sh;
     nox --stop-on-first-error -s lint travis;
else
    # only run lint on external PRs
    echo 'External PR: only running lint.'
    nox --stop-on-first-error -s lint;
fi
