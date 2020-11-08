# Available nvidia/cuda images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
ARG base_image=nvcr.io/nvidia/cuda:10.1-cudnn8-runtime

# We use a multi stage build to reduce the image size.
# The first stage builds the Dataflow entry point and installs Python 3.
# Then, we create a clean image without all the temporary files.
#   https://docs.docker.com/develop/develop-images/multistage-build/
FROM ${base_image} as builder

WORKDIR /root


# Install any packages needed, there is no need to clear the cache since the
# whole stage is discarded except for the files we explicitly copy.
RUN apt-get update && apt-get install -y wget


# Download and compile the Dataflow worker boot file.
#   ℹ️ This is required for the Dataflow runner.
ENV PATH=${PATH}:/usr/local/go/bin

RUN wget -O golang.tar.gz https://golang.org/dl/go1.15.3.linux-amd64.tar.gz \
    && wget -O boot.go https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/boot.go \
    && wget -O piputil.go https://raw.githubusercontent.com/apache/beam/master/sdks/python/container/piputil.go \
    && tar -C /usr/local -xzf golang.tar.gz \
    && go mod init github.com/apache/beam/sdks/python/boot \
    && go build -o /opt/apache/beam/boot


# The nvidia/cuda image doesn't have Python, so we install it with conda.
#   ℹ️ This is not required if your base image already comes with the
#      Python version you want, like `python:3.7-slim`.
ENV PATH=/opt/conda/bin:${PATH}
ENV PATH=/opt/python/bin:${PATH}

RUN wget -O conda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh conda.sh -b -p /opt/conda \
    && conda update -y conda \
    && conda create -y --prefix /opt/python python=3.7


# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`.
COPY requirements.txt .

RUN pip install -U pip \
    && pip install -r requirements.txt


#===------------------------------------------------------------------------===#
# The final image only contains the final builds.
FROM ${base_image}

# Copy the worker boot and python from the builder stage.
# Make sure to copy the Python installation into the same directory where it was
# built in the previous stage, since it expects it to live there.
COPY --from=builder /opt/apache/beam/boot /opt/apache/beam/boot
COPY --from=builder /opt/python /opt/python

# Set the entrypoint to the worker boot file.
# The worker boot file expects a $pip environment variable with pip's location.
ENV pip=/opt/python/bin/pip
ENV PATH=/opt/python/bin:${PATH}
ENTRYPOINT [ "/opt/apache/beam/boot" ]
