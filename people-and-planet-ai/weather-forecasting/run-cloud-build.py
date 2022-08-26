from subprocess import run

project = "dcavazos-lyra"
bucket = "dcavazos-lyra"
location = "us-central1"

cmd = [
    "gcloud",
    "builds",
    "submit",
    "serving/",
    f"--tag=gcr.io/{project}/weather",
    "--machine-type=N1_HIGHCPU_8",
]
run(cmd, check=True)
