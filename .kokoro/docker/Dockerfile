# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# We want to use LTS ubuntu from our mirror because dockerhub has a
# rate limit.
# FROM mirror.gcr.io/library/ubuntu:18.04
# However, now the above image is not working, we're using our own cache
FROM gcr.io/cloud-devrel-kokoro-resources/ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Ensure local Python is preferred over distribution Python.
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# At the moment, setting "LANG=C" on a Linux system fundamentally breaks
# Python 3.
ENV LANG C.UTF-8

# Install dependencies.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    apt-transport-https \
    build-essential \
    ca-certificates \
    curl \
    dirmngr \
    git \
    gcc \
    gpg-agent \
    graphviz \
    libbz2-dev \
    libdb5.3-dev \
    libexpat1-dev \
    libffi-dev \
    liblzma-dev \
    libmagickwand-dev \
    libmemcached-dev \
    libpython3-dev \
    libreadline-dev \
    libsnappy-dev \
    libssl-dev \
    libsqlite3-dev \
    portaudio19-dev \
    python3-distutils \
    pkg-config \
    redis-server \
    software-properties-common \
    ssh \
    sudo \
    systemd \
    tcl \
    tcl-dev \
    tk \
    tk-dev \
    uuid-dev \
    wget \
    zlib1g-dev \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

# Install docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    docker-ce \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

# Install Bazel for compiling Tink in Cloud SQL Client Side Encryption Samples
# TODO: Delete this section once google/tink#483 is resolved
RUN apt install -y curl gpgconf gpg \
  && curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg \
  && mv bazel.gpg /etc/apt/trusted.gpg.d/ \
  && echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list \
  && apt update &&  apt install -y bazel \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

# Install Microsoft ODBC 17 Driver and unixodbc for testing SQL Server samples
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql17 \
    unixodbc-dev \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

RUN wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.8 /tmp/get-pip.py \
  && rm /tmp/get-pip.py

# Install "virtualenv", since the vast majority of users of this image
# will want it.
RUN pip install --no-cache-dir virtualenv

# Setup Cloud SDK
ENV CLOUD_SDK_VERSION 339.0.0
# Use system python for cloud sdk.
ENV CLOUDSDK_PYTHON python3.8
RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-$CLOUD_SDK_VERSION-linux-x86_64.tar.gz
RUN tar xzf google-cloud-sdk-$CLOUD_SDK_VERSION-linux-x86_64.tar.gz
RUN /google-cloud-sdk/install.sh
ENV PATH /google-cloud-sdk/bin:$PATH

# Enable redis-server on boot.
RUN sudo systemctl enable redis-server.service

# Create a user and allow sudo

# kbuilder uid on the default Kokoro image
ARG UID=1000
ARG USERNAME=kbuilder

# Add a new user to the container image.
# This is needed for ssh and sudo access.

# Add a new user with the caller's uid and the username.
RUN useradd -d /h -u ${UID} ${USERNAME}

# Allow nopasswd sudo
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

CMD ["python3.8"]
