#!/bin/bash
#
set -ue

VERSION=$(git log -1 --pretty=format:%H)
if [ -n "$(git status --porcelain)" ]
then
  VERSION="dirty-$VERSION"
fi

git status
echo
echo -e "Hit [ENTER] to continue: \c"
read

SCRIPTS_DIR=$( dirname $0 )
ROOT_DIR=$( dirname $SCRIPTS_DIR )

APPCFG=$(which appcfg.py) \
  || (echo "ERROR: appcfg.py must be in your PATH"; exit 1)
while [ -L $APPCFG ]
do
  APPCFG=$(readlink $APPCFG)
done

BIN_DIR=$(dirname $APPCFG)

if [ "$(basename $BIN_DIR)" == "bin" ]
then
  SDK_HOME=$(dirname $BIN_DIR)
  if [ -d $SDK_HOME/platform/google_appengine ]
  then
    SDK_HOME=$SDK_HOME/platform/google_appengine
  fi
else
  SDK_HOME=$BIN_DIR
fi

function get_app_id() {
  local app_id
  app_id=$( cat $ROOT_DIR/app.yaml | egrep '^application:' | sed 's/application: *\([0-9a-z][-0-9a-z]*[0-9a-z]\).*/\1/' )
  while [ $# -gt 0 ]
  do
    if [ "$1" == "-A" ]
    then
      shift
      app_id=$1
    elif [ "${1/=*/}" == "--application" ]
    then
      app_id=${1/--application=/}
    fi
    shift
  done
  echo $app_id
}

function deploy() {
  echo -e "\n*** Rolling back any pending updates (just in case) ***\n"
  appcfg.py --oauth2 $* rollback .

  echo -e "\n*** DEPLOYING ***\n"
  appcfg.py --oauth2 $* update -V $VERSION .

  echo -e "\n*** SETTING DEFAULT VERSION ***\n"
  appcfg.py --oauth2 $* set_default_version -V $VERSION .
}

APP_ID=$(get_app_id $*)
echo
echo "Using app id: $APP_ID"

deploy $* -A $APP_ID
