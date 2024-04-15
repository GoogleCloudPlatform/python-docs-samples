# [START create_cloud_function_v2]
from google.cloud.functions_v2 import FunctionServiceClient, CreateFunctionRequest
from google.cloud.functions_v2.types import (
    Function,
    BuildConfig,
    ServiceConfig,
    StorageSource,
    Source,
)


def create_cloud_function(
    project_id,
    bucket_name,
    location_id,
    function_id,
    entry_point,
    function_archive,
    runtime="python311",
):
    client = FunctionServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    function_name = (
        f"projects/{project_id}/locations/{location_id}/functions/{function_id}"
    )
    function = Function(
        name=function_name,
        build_config=BuildConfig(
            source=Source(
                storage_source=StorageSource(
                    bucket=bucket_name,
                    object_=function_archive,
                    generation=2,
                )
            ),
            runtime=runtime,
            entry_point=entry_point,
        ),
        service_config=ServiceConfig(available_memory="256M"),
    )

    request = CreateFunctionRequest(
        parent=parent, function=function, function_id=function_id
    )

    operation = client.create_function(request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)


# [END create_cloud_function_v2]


if __name__ == "__main__":
    import uuid
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    BUCKET_NAME = os.environ["BUCKET_NAME"]
    create_cloud_function(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
        location_id="us-central1",
        function_id=f"test-function-{uuid.uuid4()}",
        entry_point="my_function_entry",
        function_archive="my_function.zip",  # assume, that function already uploaded to <BUCKET_NAME>
    )
