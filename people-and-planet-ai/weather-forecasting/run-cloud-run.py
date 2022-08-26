from subprocess import run

project = "dcavazos-lyra"
bucket = "dcavazos-lyra"
location = "us-central1"

service_name = "weather"

cmd = [
    "gcloud",
    "run",
    "deploy",
    service_name,
    "--source=./serving",
    f"--region={location}",
    "--no-allow-unauthenticated",
]
run(cmd, check=True)
