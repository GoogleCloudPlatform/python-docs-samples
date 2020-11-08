# Available nvidia/cuda images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
ARG base_image=nvcr.io/nvidia/cuda:10.1-cudnn8-runtime-ubi8

# We use a multi stage build to reduce the image size.
# The first stage builds the Dataflow entry point and installs Python 3.
# Then, we create a clean image without all the temporary files.
#   https://docs.docker.com/develop/develop-images/multistage-build/
FROM ${base_image} as builder

WORKDIR /root


# Download and compile the Dataflow worker booting sequence.
#   ℹ️ This is required for the Dataflow runner.
ENV PATH=${PATH}:/usr/local/go/bin

RUN curl -o golang.tar.gz -L https://golang.org/dl/go1.15.3.linux-amd64.tar.gz \
    && curl -o boot.go -L https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/boot.go \
    && curl -o piputil.go -L https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/piputil.go \
    && tar -C /usr/local -xzf golang.tar.gz \
    && go mod init github.com/apache/beam/sdks/python/boot \
    && go build -o /opt/apache/beam/boot


# The nvidia/cuda image doesn't have Python, so we install it with conda.
#   ℹ️ This is not necessary if your base image already comes with the
#      Python version you want, like `python:3.7-slim`.
ENV PATH=/opt/conda/bin:${PATH}

RUN curl -o conda.sh -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh conda.sh -b -p /opt/conda \
    && conda update -y conda \
    && conda create -y --prefix /opt/python python=3.7


#===------------------------------------------------------------------------===#
# The final image only contains the final builds.
FROM ${base_image}

# The worker boot expects the pip location in a `pip` environment variable.
ENV pip=/opt/python/bin/pip
ENV PATH=/opt/python/bin:${PATH}

# Copy the worker boot and python from the builder stage.
COPY --from=builder /opt/apache/beam/boot /opt/apache/beam/boot
COPY --from=builder /opt/python /opt/python

# Set the entrypoint to the worker boot.
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`.
COPY requirements.txt .

RUN pip config set global.cache-dir false \
    && pip install -U pip \
    && pip install -r requirements.txt \
    # Tensorflow expects SSL certificates at /etc/ssl/certs/ca-certificates.crt
    #   https://github.com/tensorflow/tensorflow/issues/40065
    && ln -s /etc/ssl/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
