# Make a temp directory - copy all python files
# remove tests
# gsutil cp what's left

import os
import tempfile
from shutil import copytree, ignore_patterns
import glob
# Imports the Google Cloud client library
from google.cloud import storage

temp_dir = tempfile.mkdtemp()


# ignore non-DAG Python files
files_to_ignore = ignore_patterns("__init__.py", "*_test.py")
DAGS_DIRECTORY = "../dags/"

# Copy everything but the ignored files to a temp directory
copytree(DAGS_DIRECTORY, f"{temp_dir}/", ignore=files_to_ignore, dirs_exist_ok=True)

# The only Python files left in our temp directory are DAG files
# so we can exclude all non Python files
dags = glob.glob(f"{temp_dir}/*.py")

# Note - the GCS client library does not currently support batch requests on uploads
# if you have a large number of files, consider using
# the Python subprocess module to run gsutil -m cp -r on your dags
# See https://cloud.google.com/storage/docs/gsutil/commands/cp for more info
BUCKET="your-bucket"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET)

for dag in dags:
    # Remove path to temp dir
    dag = dag.replace(f"{temp_dir}/", "")
    
    #Upload to your bucket
    blob = bucket.blob(dag)
    blob.upload_from_string(dag)
    print(f"File {dag} uploaded to {BUCKET}/{dag}.")

