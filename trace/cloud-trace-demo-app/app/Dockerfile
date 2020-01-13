FROM python:3.8.0

RUN pip3 install --upgrade pip

RUN apt-get update \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install opencensus-ext-stackdriver
RUN pip3 install grpcio
COPY *.py /app/

ENTRYPOINT ["python"]
CMD ["./app.py"]
