#!/bin/bash
set -euxo pipefail
echo '--- Installing git and cloning repository on VM ---'
sudo apt-get update && sudo apt-get install -y git python3-pip python3-venv

# Clone the repository and checkout the specific commit from the build trigger.
git clone --no-checkout --depth 1 --sparse --filter=blob:none https://github.com/GoogleCloudPlatform/python-docs-samples
cd python-docs-samples
git sparse-checkout set storage
git fetch origin "refs/pull/${_PR_NUMBER}/head"
git checkout ${COMMIT_SHA}
cd storage


echo '--- Installing Python and dependencies on VM ---'
python3 -m venv env
source env/bin/activate

echo 'Install testing libraries explicitly, as they are not in setup.py'
pip install --upgrade pip
pip install pytest pytest-timeout pytest-subtests pytest-asyncio
pip install google-cloud-testutils google-cloud-kms
pip install google-cloud-storage[grpc,testing]

echo '--- Setting up environment variables on VM ---'
export ZONAL_BUCKET=${_ZONAL_BUCKET}
export RUN_ZONAL_SYSTEM_TESTS=True
export GCE_METADATA_MTLS_MODE=None
CURRENT_ULIMIT=$(ulimit -n)
echo '--- Running Zonal tests on VM with ulimit set to ---' $CURRENT_ULIMIT
pytest -vv -s --log-format='%(asctime)s %(levelname)s %(message)s' --log-date-format='%H:%M:%S' samples/snippets/zonal_buckets/zonal_snippets_test.py
