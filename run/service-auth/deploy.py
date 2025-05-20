import os
from google.cloud import run_v2
from google.cloud.run_v2 import types
from google.cloud.run_v2.types import revision_template as revision_template_types
from google.cloud.run_v2.types import k8s_min as k8s_min_types
from google.protobuf import field_mask_pb2

from google.api_core.exceptions import NotFound

from google.iam.v1 import policy_pb2, iam_policy_pb2

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def deploy_cloud_run_service(
    project_id: str,
    region: str,
    service_name: str,
    image_uri: str,
    env_vars: dict = None,
    memory_limit: str = "512Mi",
    cpu_limit: str = "1",
    port: int = 8080,
    allow_unauthenticated: bool = True,
):
    """Deploys or updates a Cloud Run service using the Python client library."""
    client = run_v2.ServicesClient()

    parent = f"projects/{project_id}/locations/{region}"
    full_service_name = f"{parent}/services/{service_name}"

    container = types.Container(
        image=image_uri,
        ports=[k8s_min_types.ContainerPort(container_port=port)],
        resources=k8s_min_types.ResourceRequirements(
            limits={"cpu": cpu_limit, "memory": memory_limit}
        ),
    )

    if env_vars:
        container.env = [
            k8s_min_types.EnvVar(name=key, value=value) for key, value in env_vars.items()
        ]

    service_config = types.service.Service(
        name=full_service_name,
        template=revision_template_types.RevisionTemplate(
            containers=[container],
            scaling=types.RevisionScaling(
                min_instance_count=0,
                max_instance_count=1,
            ),
        ),
        traffic=[
            types.TrafficTarget(
                type_=types.TrafficTargetAllocationType.TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST,
                percent=100,
            )
        ]
    )

    deployed_service = None
    try:
        client.get_service(name=full_service_name)
        print(f"Service {service_name} found. Attempting to update...")

        update_mask = field_mask_pb2.FieldMask()
        update_mask.paths.append("template")
        update_mask.paths.append("traffic")

        operation = client.update_service(service=service_config, field_mask=update_mask)
        print(f"Update operation started for service {service_name}: {operation.operation.name}")
        deployed_service = operation.result()
        print(f"Service {service_name} updated successfully: {deployed_service.uri}")

    except NotFound as e:
        print(f"Service {service_name} not found. Attempting to create...")
        service_config.name = "" # API will construct the full name based on service_id

        operation = client.create_service(
            parent=parent,
            service=service_config,
            service_id=service_name,
        )
        print(f"Create operation started for service {service_name}: {operation.operation.name}")
        deployed_service = operation.result()
        print(f"Service {service_name} created successfully: {deployed_service.uri}")
    except Exception as e:
            print(f"An error occurred during service deployment: {e}")
            raise

    # Allow unauthenticated requests if requested
    if deployed_service and allow_unauthenticated:
        try:
            print(f"Attempting to allow unauthenticated access for {service_name}...")
            # Get the current IAM policy
            # The resource path for IAM is the full service name
            policy_request = iam_policy_pb2.GetIamPolicyRequest(resource=deployed_service.name)
            current_policy = client.get_iam_policy(request=policy_request)

            # Create a new binding for allUsers
            new_binding = policy_pb2.Binding(
                role="roles/run.invoker",
                members=["allUsers"],
            )

            # Add the new binding to the policy
            # Be careful not to remove existing bindings.
            # Check if this binding already exists to avoid duplicates (optional but good practice)
            binding_exists = False
            for binding in current_policy.bindings:
                if binding.role == new_binding.role and "allUsers" in binding.members:
                    print(f"Binding for allUsers with role {new_binding.role} already exists.")
                    binding_exists = True
                    break

            if not binding_exists:
                current_policy.bindings.append(new_binding)

                set_policy_request = iam_policy_pb2.SetIamPolicyRequest(
                    resource=deployed_service.name,
                    policy=current_policy,
                )
                client.set_iam_policy(request=set_policy_request)
                print(f"Successfully allowed unauthenticated access for {service_name}.")
            else:
                # If you want to ensure the policy is set even if only other bindings change,
                # you might still call set_iam_policy here, but for just adding allUsers,
                # this check avoids an unnecessary API call if it's already public.
                pass


        except Exception as e:
            print(f"Failed to set IAM policy for unauthenticated access: {e}")
            # Depending on requirements, you might want to raise this error or just log it.

    return deployed_service


if __name__ == "__main__":
    REGION = "us-central1"
    SERVICE_NAME = "my-python-deployed-service"
    IMAGE_URI = "gcr.io/cloudrun/hello"

    # Optional environment variables
    ENVIRONMENT_VARIABLES = {}

    deploy_cloud_run_service(
            project_id=PROJECT_ID,
            region=REGION,
            service_name=SERVICE_NAME,
            image_uri=IMAGE_URI,
            env_vars=ENVIRONMENT_VARIABLES,
        )

    try:
        pass
    except Exception as e:
        print(f"Deployment failed: {e}")