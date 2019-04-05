#!/bin/bash

main(){
rm -rf notifier/tools/python_cli/api_client/
local host_url=$(grep host openapi.json | sed -e 's# "host": "\(.*\)",#\1#g')
swagger-codegen generate -i openapi.json -l python -o notifier/tools/python_cli/client -DpackageName=api_client

mv notifier/tools/python_cli/client/api_client notifier/tools/python_cli/api_client/

# fix generated code
sed -i '' -e "s#querys.append.*#querys[auth_setting['key']] = auth_setting['value']#g" notifier/tools/python_cli/api_client/api_client.py

# reset host information on generated code
sed -i '' -e "s#self.host = \"https://$host_url/_ah/api\"#self.host = \"\"#g" notifier/tools/python_cli/api_client/configuration.py
cp notifier/tools/python_cli/client/README.md notifier/tools/python_cli/

printf 'pyyaml >= 3.12' >> notifier/tools/python_cli/client/requirements.txt
cp notifier/tools/python_cli/client/requirements.txt notifier/tools/python_cli/

git grep -l $host_url | xargs sed -i '' -e "s#$host_url#\$API_ENDPOINT_URL#g"

rm -rf notifier/tools/python_cli/client
}

main "$@"
