# Available nvidia/cuda images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
# FROM nvcr.io/nvidia/cuda:10.1-cudnn8-runtime-ubi7
FROM gcr.io/deeplearning-platform-release/tf2-gpu

WORKDIR /root


#===--- Create the entry point ---===#
# Download and compile the bootloader for the Dataflow workers.
#   ℹ️ This is _required_ for the Dataflow runner.
ENV PATH=$PATH:/usr/local/go/bin

RUN curl -o golang.tar.gz -L https://golang.org/dl/go1.15.3.linux-amd64.tar.gz \
    && curl -o boot.go -L https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/boot.go \
    && curl -o piputil.go -L https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/piputil.go \
    && tar -C /usr/local -xzf golang.tar.gz \
    && go mod init github.com/apache/beam/sdks/python/boot \
    && go build -o /opt/apache/beam/boot \
    && rm -rf *

ENTRYPOINT [ "/opt/apache/beam/boot" ]


# #===--- Install Python 3 with pyenv ---===#
# # The nvidia/cuda image comes with Python 2, but we want Python 3.
# #   ℹ️ This is _not necessary_ if your base image already comes with the
# #      Python version you want, like `python:3.7-slim`.
# ENV PYENV_ROOT=/pyenv
# ENV PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
# ENV CFLAGS=-O2

# # You can specify a different version when building the image:
# #   gcloud builds submit -t $IMAGE --build-arg python_version=3.8.6 .
# ARG python_version=3.7.9

# # We need to install some dependencies for pyenv:
# #   https://github.com/pyenv/pyenv/wiki/Common-build-problems
# RUN yum install -y git gcc make @development zlib-devel bzip2 bzip2-devel readline-devel sqlite \
#     sqlite-devel openssl-devel xz xz-devel libffi-devel findutils \
#     && yum clean all \
#     && curl https://pyenv.run | bash \
#     && pyenv install $python_version \
#     && pyenv global $python_version


#===--- Install the pipeline requirements ---===#
# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`,
#      or else you need to install it manually here.
COPY requirements.txt .
RUN pip install -U pip \
    && pip install -r requirements.txt \
    # Dataflow expects pip to live in /usr/local/bin/pip
    && ln -s $(which pip) /usr/local/bin/pip \
    # Clean up the cache to reduce the image size.
    && rm -rf $HOME/.cache
