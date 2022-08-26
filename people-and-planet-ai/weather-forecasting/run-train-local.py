from subprocess import run

cmd = [
    "weather-trainer",
    # "python",
    # "serving/trainer.py",
    "--data-path=data",
    "--model-path=/tmp/model",
    "--epoch=2",
]
run(cmd, check=True)

# Beam requires dill (doesn't work)
# dill==0.3.1.1
# multiprocess==0.70.9

# Works
# multiprocess==0.70.11

# Works with latest
# dill==0.3.6
# multiprocess==0.70.14
