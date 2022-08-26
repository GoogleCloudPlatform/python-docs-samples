from subprocess import run

project = "dcavazos-lyra"
bucket = "dcavazos-lyra"
location = "us-central1"

# python -m build weather-data

cmd = [
    "python",
    "create-dataset.py",
    f"--data-path=gs://{bucket}/temp/data",
    "--num-dates=1",
    "--num-bins=1",
    "--runner=Dataflow",
    f"--project={project}",
    f"--region={location}",
    f"--temp_location=gs://{bucket}/temp",
    "--extra_package=./serving/weather-data/dist/weather-data-1.0.0.tar.gz",
]
run(cmd, check=True)
