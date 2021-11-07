This section contains a sample of using [Prometheus](https://prometheus.io) to instrument a Flask application to emit Service Level Indicator metrics.

## Running the samples locally

1.  Many samples require extra libraries to be installed. If there is a `requirements.txt`, you will need to install the dependencies with [`pip`](pip.readthedocs.org).

        pip install -t lib -r requirements.txt

2.  Use `main.py` to run the sample:

        python main.py

3.  Visit `http://localhost:8080` to view your application.

4.  Visit `http://localhost:8080/metrics` to view your metrics.

## Additional resources

For more information on Prometheus:

> https://prometheus.io
