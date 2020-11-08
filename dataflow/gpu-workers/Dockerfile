# Available nvidia/cuda images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
FROM nvcr.io/nvidia/cuda:10.1-cudnn8-runtime-ubi7

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
    && go build -o /opt/apache/beam/boot

ENTRYPOINT [ "/opt/apache/beam/boot" ]


#===--- Install Python 3 ---===#
# The nvidia/cuda image comes with Python 2, but we want Python 3.
#   ℹ️ This is _not necessary_ if your base image already comes with the
#      Python version you want, like `python:3.7-slim`.
ENV PATH=/opt/conda/envs/py3/bin:/opt/conda/bin:$PATH

RUN curl -o conda.sh -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh conda.sh -b -p /opt/conda \
    && conda update -y conda \
    && conda create -y --name py3 python=3.7 \
    && conda clean -y --all


#===--- Install the pipeline requirements ---===#
# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`,
#      or else you need to install it manually here.
COPY requirements.txt .

RUN pip install -U pip \
    && pip install --use-feature=2020-resolver -r requirements.txt \
    # Clean up caches and temporary files to reduce the image size.
    && rm -rf ./* $HOME/.cache /tmp/*
