from subprocess import run

cmd = [
    "python",
    "create_dataset.py",
    "--data-path=data",
    "--num-dates=1",
    "--num-bins=2",
]
run(cmd, check=True)
