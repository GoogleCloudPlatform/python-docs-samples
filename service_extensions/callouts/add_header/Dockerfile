FROM marketplace.gcr.io/google/debian11
WORKDIR /home/callouts
COPY . .
RUN apt-get update && apt-get install -y python3-grpc-tools
EXPOSE 80
EXPOSE 8080
EXPOSE 443
CMD [ "/usr/bin/python3", "server.py" ]
