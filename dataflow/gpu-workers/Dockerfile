# Available nvidia/cuda images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
ARG base_image=nvcr.io/nvidia/cuda:10.1-cudnn7-runtime


#===------------------------------------------------------------------------===#
# We use a multi stage build to reduce the image size.
# The first stage builds and installs Python 3 and the requirements.
# Then, we create a clean image without all the temporary files.
#   https://docs.docker.com/develop/develop-images/multistage-build/
FROM ${base_image} as builder

WORKDIR /root

# Install any packages needed, there is no need to clear the cache since the
# whole stage is discarded except for the files we explicitly copy.
RUN apt-get update && apt-get install -y wget

# The nvidia/cuda image doesn't have Python, so we install it with conda.
#   ℹ️ This is not required if your base image already comes with the
#      Python version you want, like `python:3.7-slim`.
ENV PYTHON_VERSION=3.7
ENV PATH=/opt/conda/bin:${PATH}
ENV PATH=/opt/python/bin:${PATH}

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O conda.sh \
    && sh conda.sh -b -p /opt/conda \
    && conda update -y conda \
    && conda create -y --prefix /opt/python python=${PYTHON_VERSION}

# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`.
COPY requirements.txt .

RUN pip install -U pip \
    && pip install -r requirements.txt


#===------------------------------------------------------------------------===#
# The final image only contains the final builds.
FROM ${base_image}

# Tensorflow needs this to find some cuda libraries.
RUN echo "/usr/local/cuda/compat" >> /etc/ld.so.conf.d/cuda-compat.conf \
    && ldconfig

# Copy the worker boot file from the beam image.
# Make sure to copy the Python installation into the same directory where it was
# built in the previous stage, since it expects it to live there.
COPY --from=apache/beam_python3.7_sdk /opt/apache/beam/boot /opt/apache/beam/boot
COPY --from=builder /opt/python /opt/python

# Add the Python installation to the $PATH environment variable.
ENV PATH=/opt/python/bin:${PATH}

# The worker boot file expects a $pip environment variable with pip's location.
ENV pip=/opt/python/bin/pip

# Set the entrypoint to the worker boot file.
ENTRYPOINT [ "/opt/apache/beam/boot" ]
