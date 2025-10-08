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
FROM mirror.gcr.io/library/ubuntu:24.04

ENV DEBIAN_FRONTEND noninteractive

# Ensure local Python is preferred over distribution Python.
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# At the moment, setting "LANG=C" on a Linux system fundamentally breaks
# Python 3.
ENV LANG C.UTF-8

# Install dependencies.
RUN apt-get update \
  && apt -y upgrade \
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

# From https://www.python.org/downloads/metadata/sigstore/
# Starting with Python 3.14, Sigstore is the only method of signing and verification of release artifacts. 
RUN LATEST_VERSION="2.6.1" && \
    wget "https://github.com/sigstore/cosign/releases/download/v${LATEST_VERSION}/cosign_${LATEST_VERSION}_amd64.deb" && \
    dpkg -i cosign_${LATEST_VERSION}_amd64.deb && \
    rm cosign_${LATEST_VERSION}_amd64.deb

ARG PYTHON_VERSIONS="3.7.17 3.8.20 3.9.23 3.10.18 3.11.13 3.12.11 3.13.8 3.14.0"

SHELL ["/bin/bash", "-c"]

RUN set -eux; \
    # Define the required associative arrays completely.
    declare -A PYTHON_IDENTITIES; \
    PYTHON_IDENTITIES=(\
        [3.7]="nad@python.org" \
        [3.8]="lukasz@langa.pl" \
        [3.9]="lukasz@langa.pl" \
        [3.10]="pablogsal@python.org" \
        [3.11]="pablogsal@python.org" \
        [3.12]="thomas@python.org" \
        [3.13]="thomas@python.org" \
        [3.14]="hugo@python.org" \
    ); \
    declare -A PYTHON_ISSUERS; \
    PYTHON_ISSUERS=(\
        [3.7]="https://github.com/login/oauth" \
        [3.8]="https://github.com/login/oauth" \
        [3.9]="https://github.com/login/oauth" \
        [3.10]="https://accounts.google.com" \
        [3.11]="https://accounts.google.com" \
        [3.12]="https://accounts.google.com" \
        [3.13]="https://accounts.google.com" \
        [3.14]="https://github.com/login/oauth" \
    ); \
    \
    for VERSION in $PYTHON_VERSIONS; do \
        # 1. Define VERSION_GROUP (e.g., 3.14 from 3.14.0)
        VERSION_GROUP="$(echo "${VERSION}" | cut -d . -f 1,2)"; \
        \
        # 2. Look up IDENTITY and ISSUER using the defined VERSION_GROUP
        IDENTITY="${PYTHON_IDENTITIES[$VERSION_GROUP]}"; \
        ISSUER="${PYTHON_ISSUERS[$VERSION_GROUP]}"; \
        \
      wget --quiet -O python-${VERSION}.tar.xz "https://www.python.org/ftp/python/${VERSION}/Python-$VERSION.tar.xz" \
      && wget --quiet -O python-${VERSION}.tar.xz.sigstore "https://www.python.org/ftp/python/${VERSION}/Python-$VERSION.tar.xz.sigstore" \
      # Verify the Python tarball signature with cosign.
      && cosign verify-blob python-${VERSION}.tar.xz \
        --certificate-oidc-issuer "${ISSUER}" \
        --certificate-identity "${IDENTITY}" \
        --bundle python-${VERSION}.tar.xz.sigstore \
      && mkdir -p /usr/src/python-${VERSION} \
      && tar -xJC /usr/src/python-${VERSION} --strip-components=1 -f python-${VERSION}.tar.xz \
      && rm python-${VERSION}.tar.xz \
      && cd /usr/src/python-${VERSION} \
      && ./configure \
          --enable-shared \
          --with-system-ffi \
      && make -j$(nproc) \
      && make install \
      && ldconfig \
  ; done \
  && rm -rf /usr/src/python* \
  && rm -rf ~/.cache/


# Install pip on Python 3.10 only.
# If the environment variable is called "PIP_VERSION", pip explodes with
# "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 21.3.1
RUN wget --no-check-certificate -O /tmp/get-pip-3-7.py 'https://bootstrap.pypa.io/pip/3.7/get-pip.py' \
  && wget --no-check-certificate -O /tmp/get-pip-3-8.py 'https://bootstrap.pypa.io/pip/3.8/get-pip.py' \
  && wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.10 /tmp/get-pip.py "pip==$PYTHON_PIP_VERSION" \
  # we use "--force-reinstall" for the case where the version of pip we're trying to install is the same as the version bundled with Python
  # ("Requirement already up-to-date: pip==8.1.2 in /usr/local/lib/python3.10/site-packages")
  # https://github.com/docker-library/python/pull/143#issuecomment-241032683
  && pip3 install --no-cache-dir --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION" \
  # then we use "pip list" to ensure we don't have more than one pip version installed
  # https://github.com/docker-library/python/pull/100
  && [ "$(pip list |tac|tac| awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ]

# Ensure Pip for all python3 versions
RUN python3.14 /tmp/get-pip.py
RUN python3.13 /tmp/get-pip.py
RUN python3.12 /tmp/get-pip.py
RUN python3.11 /tmp/get-pip.py
RUN python3.9 /tmp/get-pip.py
RUN python3.8 /tmp/get-pip-3-8.py
RUN python3.7 /tmp/get-pip-3-7.py
RUN rm /tmp/get-pip.py

# Test Pip
RUN python3 -m pip
RUN python3.7 -m pip
RUN python3.8 -m pip
RUN python3.9 -m pip
RUN python3.10 -m pip
RUN python3.11 -m pip
RUN python3.12 -m pip
RUN python3.13 -m pip
RUN python3.14 -m pip

# Install "setuptools" for Python 3.12+ (see https://docs.python.org/3/whatsnew/3.12.html#distutils)
RUN python3.12 -m pip install --no-cache-dir setuptools
RUN python3.13 -m pip install --no-cache-dir setuptools

# Install "virtualenv", since the vast majority of users of this image will want it.
RUN pip install --no-cache-dir virtualenv

# Setup Cloud SDK
ENV CLOUD_SDK_VERSION 502.0.0
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
# UID 1000 is taken in Ubuntu 24.04
ARG UID=10000
ARG USERNAME=kbuilder

# Add a new user to the container image.
# This is needed for ssh and sudo access.

# Add a new user with the caller's uid and the username.
RUN useradd -d /h -u ${UID} ${USERNAME}

# Allow nopasswd sudo
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install Chrome.
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
  && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
  && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
  && mkdir -p /usr/share/desktop-directories \
  && apt-get -y update && apt-get install -y google-chrome-stable

# Disable the SUID sandbox so that Chrome can launch without being in a privileged container.
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
  && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
  && chmod 755 /opt/google/chrome/google-chrome

# Install Chrome Driver.
RUN mkdir -p /opt/selenium \
  && curl http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
  && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;

CMD ["python3"]
