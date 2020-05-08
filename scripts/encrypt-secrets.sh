#!/bin/bash

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$( dirname "$DIR" )

# Work from the project root.
cd $ROOT

read -s -p "Enter password for encryption: " PASSWORD
echo

tar cvf secrets.tar testing/{service-account.json,client-secrets.json,test-env.sh}
openssl aes-256-cbc -k "$PASSWORD" -in secrets.tar -out testing/secrets.tar.enc
rm secrets.tar

travis encrypt "SECRETS_PASSWORD=$PASSWORD" --add --override
