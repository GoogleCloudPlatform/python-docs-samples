#!/bin/bash
. $(dirname $0)/../lib/sh_commons.sh

main(){
  local POM_VERSION=$(mvn -f notifier/app -q  -Dexec.executable='echo' -Dexec.args='${project.version}' --non-recursive exec:exec)
  local provided_version="$1"
  local version="${provided_version:-$POM_VERSION}"

  if [ -z $version ]; then
    usage
  fi

  # local zip_file="scc-tools-${version}.zip"
  local dist_path="dist"
  local connector_app="scc-connector"
  local creator_app="scc-creator"
  local hello_world_app="scc-hello-world"
  local notifier_app="scc-notifier"
  local audit_logs_app="scc-audit-logs"
  local query_builder_app="scc-query-builder"
  local setup_scripts_app="scc-setup-scripts"
  local documentation_sources="documentation-sources"

  local connector_zip_file="${dist_path}/${connector_app}/${connector_app}-${version}.zip"
  local creator_zip_file="${dist_path}/${creator_app}/${creator_app}-${version}.zip"
  local helloworld_zip_file="${dist_path}/${hello_world_app}/${hello_world_app}-${version}.zip"
  local notifier_zip_file="${dist_path}/${notifier_app}/${notifier_app}-${version}.zip"
  local audit_logs_zip_file="${dist_path}/${audit_logs_app}/${audit_logs_app}-${version}.zip"
  local query_builder_zip_file="${dist_path}/${query_builder_app}/${query_builder_app}-${version}.zip"
  local setup_scripts_zip_file="${dist_path}/${setup_scripts_app}/${setup_scripts_app}-${version}.zip"
  
  rm -rf ${dist_path}
  mkdir -p ${dist_path}/${connector_app}
  mkdir -p ${dist_path}/${creator_app}
  mkdir -p ${dist_path}/${hello_world_app}
  mkdir -p ${dist_path}/${notifier_app}
  mkdir -p ${dist_path}/${audit_logs_app}
  mkdir -p ${dist_path}/${query_builder_app}
  mkdir -p ${dist_path}/${setup_scripts_app}
  mkdir -p ${dist_path}/${documentation_sources}

  chmod -R 777 ${dist_path}

  git archive -o "${connector_zip_file}" --prefix connector/ -9 HEAD:connector
  log "${connector_zip_file} created!"
  
  git archive -o "${query_builder_zip_file}" --prefix scc-query-builder/ -9 HEAD:scc-query-builder
  log "${query_builder_zip_file} created!"

  git archive -o "${creator_zip_file}" --prefix creator/ -9 HEAD:creator
  (
    # add the scc-client in the correct directory structure in the final creator zip file
    cp -r scc-client creator/appflex/
    zip -ur ${creator_zip_file} creator/appflex/scc-client/ -q
  )
  log "${creator_zip_file} created!"
  
  git archive -o "${notifier_zip_file}" --prefix notifier/ -9 HEAD:notifier
  log "${notifier_zip_file} created!"
  
  git archive -o "${helloworld_zip_file}" --prefix hello-world/ -9 HEAD:hello-world
  log "${helloworld_zip_file} created!"

  git archive -o "${audit_logs_zip_file}" --prefix scc-logs/ -9 HEAD:scc-logs
  (
    # generate necessary throtler library 
    cd scc-logs/throttler;
    pipenv run pip install -t lib -r requirements.txt -U -q;
  )
  (
    # add the scc-client-node in the correct directory structure in the final audit logs zip file
    cp -r scc-client-node scc-logs/function/finding-scc-writer
    zip -ur ${audit_logs_zip_file} scc-logs/function/finding-scc-writer/ -q
  )
  zip -ur ${audit_logs_zip_file} scc-logs/throttler/lib -q
  log "${audit_logs_zip_file} created!"

  git archive -o "${setup_scripts_zip_file}" -9 HEAD setup
  log "${setup_scripts_zip_file} created!"
  
  cp -R ${documentation_sources} ${dist_path}
  log "${documentation_sources} created!"
}

usage(){
local help=""
read -d '' help <<- EOF
USAGE:
    `basename $0` version
EOF
  err "$help"
  exit $E_OPTERROR # Exit and explain usage.
}

main "$@"
