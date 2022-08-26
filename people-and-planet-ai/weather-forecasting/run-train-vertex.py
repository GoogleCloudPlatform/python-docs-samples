from google.cloud import aiplatform

project = "dcavazos-lyra"
bucket = "dcavazos-lyra"
location = "us-central1"

# python -m build serving/weather-model
# gsutil cp serving/weather-model/dist/*.tar.gz gs://$BUCKET/weather/

epochs = 1000

aiplatform.init(project=project, location=location, staging_bucket=bucket)

job = aiplatform.CustomPythonPackageTrainingJob(
    display_name=f"weather-3k-{epochs}-from-checkpoint",
    python_package_gcs_uri=f"gs://{bucket}/weather/weather-model-1.0.0.tar.gz",
    python_module_name="weather.trainer",
    container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-11:latest",
)

job.run(
    # machine_type="n1-highmem-8",
    machine_type="n1-highmem-16",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    args=[
        f"--data-path=/gcs/{bucket}/weather/data-3000",
        f"--model-path=/gcs/{bucket}/weather/model/data-3k-{epochs}",
        f"--epochs={epochs}",
        "--from-checkpoint",
    ],
)
