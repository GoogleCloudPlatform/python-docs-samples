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

COPY fetch_gpg_keys.sh /tmp
# Install the desired versions of Python.
RUN set -ex \
  && export GNUPGHOME="$(mktemp -d)" \
  && echo "disable-ipv6" >> "${GNUPGHOME}/dirmngr.conf" \
  && /tmp/fetch_gpg_keys.sh \
  && for PYTHON_VERSION in 2.7.18 3.7.16 3.8.16 3.9.16 3.10.9 3.11.1; do \
  wget --no-check-certificate -O python-${PYTHON_VERSION}.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
  && wget --no-check-certificate -O python-${PYTHON_VERSION}.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
  && gpg --batch --verify python-${PYTHON_VERSION}.tar.xz.asc python-${PYTHON_VERSION}.tar.xz \
  && rm -r python-${PYTHON_VERSION}.tar.xz.asc \
  && mkdir -p /usr/src/python-${PYTHON_VERSION} \
  && tar -xJC /usr/src/python-${PYTHON_VERSION} --strip-components=1 -f python-${PYTHON_VERSION}.tar.xz \
  && rm python-${PYTHON_VERSION}.tar.xz \
  && cd /usr/src/python-${PYTHON_VERSION} \
  && ./configure \
  --enable-shared \
  # This works only on Python 2.7 and throws a warning on every other
  # version, but seems otherwise harmless.
  --enable-unicode=ucs4 \
  --with-system-ffi \
  --without-ensurepip \
  && make -j$(nproc) \
  && make install \
  && ldconfig \
  ; done \
  && rm -rf "${GNUPGHOME}" \
  && rm -rf /usr/src/python* \
  && rm -rf ~/.cache/


# Install pip on Python 3.10 only.
# If the environment variable is called "PIP_VERSION", pip explodes with
# "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 21.3.1
RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.10 /tmp/get-pip.py "pip==$PYTHON_PIP_VERSION" \
  # we use "--force-reinstall" for the case where the version of pip we're trying to install is the same as the version bundled with Python
  # ("Requirement already up-to-date: pip==8.1.2 in /usr/local/lib/python3.10/site-packages")
  # https://github.com/docker-library/python/pull/143#issuecomment-241032683
  && pip3 install --no-cache-dir --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION" \
  # then we use "pip list" to ensure we don't have more than one pip version installed
  # https://github.com/docker-library/python/pull/100
  && [ "$(pip list |tac|tac| awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ]

# Ensure Pip for all python3 versions
RUN python3.11 /tmp/get-pip.py
RUN python3.9 /tmp/get-pip.py
RUN python3.8 /tmp/get-pip.py
RUN python3.7 /tmp/get-pip.py
RUN rm /tmp/get-pip.py

# Test Pip
RUN python3 -m pip
RUN python3.7 -m pip
RUN python3.8 -m pip
RUN python3.9 -m pip
RUN python3.10 -m pip
RUN python3.11 -m pip

# Install "virtualenv", since the vast majority of users of this image
# will want it.
RUN pip install --no-cache-dir virtualenv

# Setup Cloud SDK
ENV CLOUD_SDK_VERSION 389.0.0
# Use system python for cloud sdk.
ENV CLOUDSDK_PYTHON python3.10
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

CMD ["python3"]
