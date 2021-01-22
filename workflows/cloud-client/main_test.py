# Copyright 2021 Google LLC
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

import os

from google.cloud import workflows_v1beta

import main

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
WORKFLOW_ID = "myFirstWorkflow"


def test_workflow_execution():
    assert PROJECT != ""

    if not workflow_exists():
        workflows_client = workflows_v1beta.WorkflowsClient()
        workflows_client.create_workflow(request={
            # Manually construct the location
            # https://github.com/googleapis/python-workflows/issues/21
            "parent": f'projects/{PROJECT}/locations/{LOCATION}',
            "workflow_id": WORKFLOW_ID,
            "workflow": {
                "name": WORKFLOW_ID,
                # Copied from
                # https://github.com/GoogleCloudPlatform/workflows-samples/blob/main/src/myFirstWorkflow.workflows.yaml
                "source_contents": '# Copyright 2020 Google LLC\n#\n# Licensed under the Apache License, Version 2.0 (the "License");\n# you may not use this file except in compliance with the License.\n# You may obtain a copy of the License at\n#\n#      http://www.apache.org/licenses/LICENSE-2.0\n#\n# Unless required by applicable law or agreed to in writing, software\n# distributed under the License is distributed on an "AS IS" BASIS,\n# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n# See the License for the specific language governing permissions and\n# limitations under the License.\n\n# [START workflows_myfirstworkflow]\n- getCurrentTime:\n    call: http.get\n    args:\n      url: https://us-central1-workflowsample.cloudfunctions.net/datetime\n    result: currentTime\n- readWikipedia:\n    call: http.get\n    args:\n      url: https://en.wikipedia.org/w/api.php\n      query:\n        action: opensearch\n        search: ${currentTime.body.dayOfTheWeek}\n    result: wikiResult\n- returnResult:\n    return: ${wikiResult.body[1]}\n# [END workflows_myfirstworkflow]\n'
            }
        })

    result = main.execute_workflow(PROJECT)
    assert len(result) > 0


def workflow_exists():
    """Returns True if the workflow exists in this project
    """
    try:
        workflows_client = workflows_v1beta.WorkflowsClient()
        workflow_name = workflows_client.workflow_path(PROJECT, LOCATION, WORKFLOW_ID)
        workflows_client.get_workflow(request={"name": workflow_name})
        return True
    except Exception as e:
        print(f"Workflow doesn't exist: {e}")
        return False
