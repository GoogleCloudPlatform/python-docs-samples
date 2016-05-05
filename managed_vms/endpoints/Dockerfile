FROM debian:jessie

RUN apt-get update && \
    apt-get install -y python2.7 python-pip python-gevent && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_*

COPY requirements.txt /requirements.txt
COPY swagger.yaml /swagger.yaml
COPY main.py /main.py

RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn", "-b", ":8081", "main:app"]
