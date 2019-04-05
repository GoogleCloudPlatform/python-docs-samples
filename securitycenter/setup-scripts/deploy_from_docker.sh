SCRIPT_CURRENT_DIR="$(dirname $(readlink -f -- $0))"
SCRIPTS_LIB_DIR=${SCRIPTS_LIB_DIR:-$SCRIPT_CURRENT_DIR/lib}

. ${SCRIPTS_LIB_DIR}/sh_commons.sh

deploy_from_docker_usage(){
  read -d '' help <<- EOF
GOAL:
Deploy from docker.

USAGE:
  $(basename $0) PARAMETERS

PARAMETERS:
  -a skip api management (DEFAULT false)
  -b cloud bucket name to be reused to store the cloud function
  -f service account key file (defaults to $HOME/Downloads/${develop_notify_gcp_project_id:-\{GCP project id\}}_deployer.json)
  -g GCP project id (REQUIRED)
  -h print this help
  -i docker image name (REQUIRED)
  -q disable all interactive prompts when running
  -s CLOUD_SDK_PATH on docker image (defaults to /usr/local/google-cloud-sdk)
  -v version that will be deployed (REQUIRED)

EOF

    echo "$help"
    exit $E_OPTERROR # Exit and explain usage.
}

deploy_from_docker_main(){
  local options="haqb:i:v:g:s:f:"
  if ( ! getopts "${options}" opt); then
    deploy_from_docker_usage
  fi

  local develop_notify_gcp_project_id=""
  local develop_notify_version=""
  local docker_image_name=""
  local cloud_sdk_path="/usr/local/google-cloud-sdk"
  local service_account_file=""
  local develop_gcloud_api_keyfile=""
  local parameters=""

  while getopts "${options}" opt; do
    case $opt in
      h)
        deploy_from_docker_usage
        ;;
      v)
        develop_notify_version=$OPTARG
        ;;
      g)
        develop_notify_gcp_project_id=$OPTARG
        ;;
      i)
        docker_image_name=$OPTARG
        ;;
      s)
        cloud_sdk_path=$OPTARG
        ;;
      f)
        service_account_file=$OPTARG
        ;;
      a)
        parameters="$parameters -$opt"
        ;;
      b)
        parameters="$parameters -$opt $OPTARG"
        ;;
      q)
        parameters="$parameters -$opt"
        ;;
      \?)
        err "Invalid option: -$OPTARG"
        deploy_from_docker_usage
        ;;
      :)
        err "Option -$OPTARG requires an argument."
        deploy_from_docker_usage
        ;;
    esac
  done

  if [ -z "$develop_notify_gcp_project_id" ] ||
     [ -z "$docker_image_name" ] || 
     [ -z "$develop_notify_version" ] ; then
    deploy_from_docker_usage
  fi

  if [ -z "$service_account_file" ] ; then
    service_account_file="$HOME/Downloads/${develop_notify_gcp_project_id}_deployer.json"
  fi

  develop_gcloud_api_keyfile=$(base64 -w 0 $service_account_file)

  docker rm $USER-notification

  docker run -ti --name $USER-notification \
          -e CLOUD_SDK_PATH="$cloud_sdk_path" \
          -e DEVELOP_GCLOUD_API_KEYFILE="$develop_gcloud_api_keyfile" \
          -e DEVELOP_NOTIFY_VERSION="$develop_notify_version" \
          -e DEVELOP_NOTIFY_GCP_PROJECT_ID="$develop_notify_gcp_project_id" \
          -e PARAMETERS="$parameters" \
          -v $HOME/logs:/tmp/ \
          -v $HOME/.m2:/root/.m2 \
          -v $(pwd):/deploy \
          $docker_image_name \
          /bin/bash -c ' echo  ; \
          echo $DEVELOP_GCLOUD_API_KEYFILE | base64 --decode --ignore-garbage > ./gcloud-api-key.json; \
          gcloud auth activate-service-account --key-file gcloud-api-key.json ; \
          gcloud config set project $DEVELOP_NOTIFY_GCP_PROJECT_ID ; \
          (cd /deploy/ ; time ./tools/scripts/deploy_all.sh -v $DEVELOP_NOTIFY_VERSION -g $DEVELOP_NOTIFY_GCP_PROJECT_ID $PARAMETERS) ;  \
          echo ;'
}

deploy_from_docker_main "$@"
