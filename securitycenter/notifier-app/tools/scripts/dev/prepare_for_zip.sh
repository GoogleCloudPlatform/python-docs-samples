#!/bin/bash

. $(dirname $0)/../lib/sh_commons.sh

OLD_NOTIFICATION_NAMESPACE=$NOTIFICATION_NAMESPACE
OLD_ENDPOINTS_SERVICE_PREFIX=$ENDPOINTS_SERVICE_PREFIX
OLD_NOTIFY_GCP_PROJECT_ID=$NOTIFY_GCP_PROJECT_ID

function _finally(){
export NOTIFICATION_NAMESPACE=$OLD_NOTIFICATION_NAMESPACE
export ENDPOINTS_SERVICE_PREFIX=$OLD_ENDPOINTS_SERVICE_PREFIX
export NOTIFY_GCP_PROJECT_ID=$OLD_NOTIFY_GCP_PROJECT_ID
}

trap _finally INT TERM EXIT

main() {
 
export NOTIFIER_ENDPOINTS_SERVICE_PREFIX=notifier
export NOTIFIER_PROJECT_ID=notifier-app

run_command mvn clean install -f notifier/app/pom.xml -DskipTests=true 
    
run_command mvn -f notifier/app/dispatcher/pom.xml appengine:stage -DskipTests=true
cp -f notifier/app/dispatcher/target/appengine-staging/WEB-INF/appengine-web.xml{,.tpl}

run_command mvn -f notifier/app/api/pom.xml appengine:stage -DskipTests=true
cp -f notifier/app/api/target/appengine-staging/WEB-INF/appengine-web.xml{,.tpl}

run_command mvn -f notifier/app/api/pom.xml exec:java -DskipTests=true -DGetOpenApiDoc \
 -DENDPOINTS_SERVICE_PREFIX=$NOTIFIER_ENDPOINTS_SERVICE_PREFIX -Dendpoints.project.id=$NOTIFIER_PROJECT_ID

cp -f openapi.json  notifier/app/api/openapi.json.tpl
}

main "$@"
