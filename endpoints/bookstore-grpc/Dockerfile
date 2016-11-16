FROM debian:jessie

RUN apt-get update \
    && apt-get install --no-install-recommends -y -q ca-certificates \
    && apt-get -y -q upgrade \
    && apt-get install -y python-dev python-pip \
    && rm -rf /var/lib/apt/lists/*

ADD . /bookstore/

RUN cd /bookstore \
    && pip install --ignore-installed six \
    && pip install --ignore-installed -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "/bookstore/bookstore_server.py"]
