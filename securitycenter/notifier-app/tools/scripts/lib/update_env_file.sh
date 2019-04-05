#!/bin/bash

SCRIPT_CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPTS_LIB_DIR=${SCRIPTS_LIB_DIR:-$SCRIPT_CURRENT_DIR}

. ${SCRIPTS_LIB_DIR}/sh_commons.sh

function to_upper() {
  local text=$1
  echo $text|tr '[:lower:]' '[:upper:]'
}

function display_env_file() {
  local env_file=`cat .env`
  local custom_msg=$1
  echo ""
  log "$custom_msg"
  echo ""
  log "$env_file"
  echo ""
}

function get_cloud_path_unix() {
  echo "$(which gcloud 2>/dev/null)"
}

function get_cloud_path_win() {
  echo "$(where gcloud.cmd 2>/dev/null)"
}

function strip_suffix() {
  local gpath=$1
  local suffix=$2
  echo ${gpath%$suffix}
}

function get_installed_gcloud_path() {
  case "$(uname -s)" in
   Darwin|Linux)
     echo $(strip_suffix "$(get_cloud_path_unix)" "/bin/gcloud")
     ;;

   CYGWIN*|MINGW32*|MINGW64*|MSYS*)
     echo $(strip_suffix "$(get_cloud_path_win)" "\\\\bin\\\\gcloud.cmd")
     ;;
   *)
     echo ''
     ;;
 esac

}

function get_default_endpoint_url() {
  local version=$1
  local project_id=$2
  echo "https://""$version""-api-dot-api-service-dot-""$project_id"".appspot.com/_ah/api "
}

function get_default_topic_name() {
  local version=$1
  echo $version"-noti-topic"
}

function print_in_green() {
  local GREEN='\033[0;32m'
  local NC='\033[0m'
  local text="$@"
  printf "${GREEN}""$text""${NC}" 2>/dev/null

}

function read_new_env_file() {
  local version=$1
  local project_id=$2

  echo ""
  echo -e "Press ENTER to save ""$(print_in_green $project_id)"" as your Project Id in the configuration file"
  read -r -p "or provide a different google cloud project: " TEMP_NOTIFY_GCP_PROJECT_ID
  if [ -z "$TEMP_NOTIFY_GCP_PROJECT_ID" ];then
    TEMP_NOTIFY_GCP_PROJECT_ID=$project_id
  fi

  local default_url="$(get_default_endpoint_url $version $project_id)"
  echo ""
  echo "Press ENTER to save ""$(print_in_green $default_url)"
  read -r -p "as your API endpoint url or provide a different url for your api: " TEMP_API_ENDPOINT_URL
  if [ -z "$TEMP_API_ENDPOINT_URL" ]; then
    TEMP_API_ENDPOINT_URL="$default_url"
  fi

  local default_topic="$(get_default_topic_name $version)"
  echo ""
  echo "Press ENTER to save ""$(print_in_green "$default_topic")"" as your pubsub message topic"
  read -r -p "or provide a different topic to publish messages to: " TEMP_NOTIFY_GCP_TOPIC
  if [ -z "$TEMP_NOTIFY_GCP_TOPIC" ]; then
    TEMP_NOTIFY_GCP_TOPIC="$default_topic"
  fi

  echo ""
  local installed_sdk="$(get_installed_gcloud_path)"

  if [ -z $installed_sdk ]; then
    echo "A installed google cloud SDK was not found in your system."
    echo "If you don't have a google cloud SDK please install one first."
    read -r -p  "If you have one installed please provide a custom path: " TEMP_CLOUD_SDK_PATH
  else
    echo "Press ENTER to save ""$(print_in_green $installed_sdk)"" as the path to your cloud sdk"
    read -r -p "or provide a custom path: " TEMP_CLOUD_SDK_PATH
    if [ -z "$TEMP_CLOUD_SDK_PATH" ]; then
      TEMP_CLOUD_SDK_PATH="$installed_sdk"
    fi
  fi

  echo "# Environment configuration file created at "`date`" by "`whoami`  > .env_temp
  echo "" >> .env_temp
  echo "export NOTIFY_GCP_PROJECT_ID=$TEMP_NOTIFY_GCP_PROJECT_ID" >> .env_temp
  echo "export API_ENDPOINT_URL=$TEMP_API_ENDPOINT_URL" >> .env_temp
  echo "export NOTIFY_GCP_TOPIC=$TEMP_NOTIFY_GCP_TOPIC" >> .env_temp
  echo "export CLOUD_SDK_PATH=\"$TEMP_CLOUD_SDK_PATH\"" >> .env_temp

  mv -f .env{_temp,}

}

function prepare_env_file() {
  local version=$1
  local project_id=$2

  if [ -f ".env" ]; then
    # if exist show content and ask if user wants to use it
    display_env_file "Content of current environment configuration file:"
    read -r -p "Do you want to keep using these configurations? (Y/N) " KEEP_CONFIG
    KEEP_CONFIG=`to_upper "$KEEP_CONFIG"`
    if [ "$KEEP_CONFIG" == "N" ] || [ "$KEEP_CONFIG" == "NO" ]; then
      read_new_env_file $version $project_id
    fi
  else
    read_new_env_file $version $project_id
  fi
  display_env_file "Configuration that will be used on this execution:"
}
