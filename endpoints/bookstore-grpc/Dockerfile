FROM debian:jessie

RUN apt-get update \
    && apt-get install --no-install-recommends -y -q ca-certificates \
    && apt-get -y -q upgrade \
    && apt-get install -y python-dev python-pip virtualenv \
    && rm -rf /var/lib/apt/lists/*

RUN virtualenv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD . /bookstore/

WORKDIR /bookstore
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "/bookstore/bookstore_server.py"]
