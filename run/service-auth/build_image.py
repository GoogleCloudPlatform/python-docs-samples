import os
import tarfile
import tempfile
import time

from google.cloud.devtools import cloudbuild_v1
from google.cloud.devtools.cloudbuild_v1.types import Build, BuildStep, Source, StorageSource
from google.cloud import storage

from deploy import deploy_cloud_run_service

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

def build_image_from_source(
    project_id: str,
    region: str,
    service_name: str,
    source_directory: str = ".",
    gcs_bucket_name: str = None,
    image_tag: str = "latest",
) -> str | None:
    """Builds a container image from local source using Google Cloud Build
    and Google Cloud Buildpacks."""

    build_client = cloudbuild_v1.CloudBuildClient()
    storage_client = storage.Client(project=project_id)

    if not gcs_bucket_name:
        gcs_bucket_name = f"{project_id}-cloud-build-source"
        print(f"GCS bucket name not provided, using {gcs_bucket_name}. Ensure it exists.")

        # TODO: Add bucket creation logic here

    timestamp = int(time.time())
    gcs_source_object = f"source/{service_name}-{timestamp}.tar.gz"

    # Use a temporary directory for the archive
    with tempfile.TemporaryDirectory() as tmpdir:
        source_archive = os.path.join(tmpdir, f"{service_name}-{timestamp}.tar.gz")

        print(f"Packaging source from {source_directory} to {source_archive}")
        with tarfile.open(source_archive, "w:gz") as tar:
            # Add files from source_directory directly, arcname='.' means they are at the root of the tar
            tar.add(source_directory, arcname='.')

        bucket = storage_client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_source_object)
        print(f"Uploading {source_archive} to gs://{gcs_bucket_name}/{gcs_source_object}")
        blob.upload_from_filename(source_archive)
        print("Source uploaded.")

    artifact_registry_repo = "cloud-run-source-deploy"
    image_name = f"{region}-docker.pkg.dev/{project_id}/{artifact_registry_repo}/{service_name}"
    full_image_uri = f"{image_name}:{image_tag}"

    # Construct the Build request using the directly imported types
    build_request = Build(
        source=Source(
            storage_source=StorageSource(
                bucket=gcs_bucket_name,
                object_=gcs_source_object,
            )
        ),
        images=[full_image_uri],
        steps=[
            BuildStep(
                name="gcr.io/k8s-skaffold/pack",
                args=[
                    "build",
                    full_image_uri,
                    "--builder", "gcr.io/buildpacks/builder:v1",
                    "--path", ".",
                ],
            )
        ],
        timeout={"seconds": 1200},
    )

    print(f"Starting Cloud Build for image {full_image_uri}...")
    operation = build_client.create_build(project_id=project_id, build=build_request)

    # The operation returned by create_build for google-cloud-build v1.x.x
    # is actually a google.api_core.operation.Operation, which has a `result()` method
    # or you can poll the build resource itself using build_client.get_build.
    # The `operation.metadata.build.id` pattern is more for long-running operations from other APIs.
    # Let's get the build ID from the name which is usually in the format projects/{project_id}/builds/{build_id}
    build_id = operation.name.split("/")[-1] # Extract build ID from operation.name
    print(f"Build operation created. Build ID: {build_id}")

    # Get the initial build details to find the log URL
    initial_build_info = build_client.get_build(project_id=project_id, id=build_id)
    print(f"Logs URL: {initial_build_info.log_url}")
    print("Waiting for build to complete...")

    while True:
        build_info = build_client.get_build(project_id=project_id, id=build_id)

        if build_info.status == Build.Status.SUCCESS:
            print(f"Build {build_info.id} completed successfully.")
            print(f"Built image: {full_image_uri}")
            return full_image_uri
        elif build_info.status in [
            Build.Status.FAILURE,
            Build.Status.INTERNAL_ERROR,
            Build.Status.TIMEOUT,
            Build.Status.CANCELLED,
        ]:
            print(f"Build {build_info.id} failed with status: {build_info.status.name}")
            print(f"Logs URL: {build_info.log_url}")
            return None

        time.sleep(10)


if __name__ == "__main__":
    REGION = "us-central1"
    SERVICE_NAME = "my-app-from-source"
    SOURCE_DIRECTORY = "./source/"
    GCS_BUILD_BUCKET = f"{PROJECT_ID}_cloudbuild_sources"

    ENVIRONMENT_VARIABLES = {}

    built_image_uri = None
    try:
        print(f"Step 1: Building image for {SERVICE_NAME} from source {SOURCE_DIRECTORY}.")
        built_image_uri = build_image_from_source(
            project_id=PROJECT_ID,
            region=REGION,
            service_name=SERVICE_NAME,
            source_directory=SOURCE_DIRECTORY,
            gcs_bucket_name=GCS_BUILD_BUCKET
        )

        if built_image_uri:
            print(f"\nStep 2: Deploying image {built_image_uri} to Cloud Run service {SERVICE_NAME}.")
            deploy_cloud_run_service(
                project_id=PROJECT_ID,
                region=REGION,
                service_name=SERVICE_NAME,
                image_uri=built_image_uri,
                env_vars=ENVIRONMENT_VARIABLES,
                allow_unauthenticated=True,
            )
            print(f"\nDeployment process for {SERVICE_NAME} finished.")
        else:
            print(f"Image build failed for {SERVICE_NAME}. Deployment aborted.")

    except Exception as e:
        print(f"An error occurred during the build or deployment process: {e}")
        import traceback
        traceback.print_exc()
