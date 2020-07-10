FROM python:3.8.3

RUN pip3 install --upgrade pip

RUN apt-get update \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

WORKDIR /app
RUN pip3 install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENTRYPOINT ["python"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
