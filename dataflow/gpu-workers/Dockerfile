# TODO: remove this -- for local testing only
# FROM python:3.7-slim
# RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

FROM apache/beam_python3.7_sdk:2.24.0

WORKDIR /root

# ℹ️ You need to download cuDNN 10.1 from Nvidia into the sample directory.
#   https://developer.nvidia.com/cudnn
COPY cudnn-10.1-linux-x64-v8.0.4.30.tgz cudnn.tgz

# Required by the Cuda Toolkit installation script.
RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*

# Download and install Cuda Toolkit and cuDNN.
RUN wget -O cuda.run https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.168_418.67_linux.run \
    # Install Cuda Toolkit, or show the errors from the logs if something went wrong.
    && sudo sh cuda.run --toolkit --silent || (egrep '^\[ERROR\]' /var/log/cuda-installer.log && exit 1) \
    # Extract the cuDNN library, and copy only the include and lib64 directories.
    # We don't need the rest of the files, and they take up a lot of space.
    && mkdir cudnn \
    && tar -xzvf cudnn.tgz -C cudnn \
    && cp cudnn/cuda/include/* /usr/local/cuda/include/ \
    && cp cudnn/cuda/lib64/* /usr/local/cuda/lib64/ \
    # Clean up files not needed to make the image smaller.
    && rm -f cuda.run \
    && rm -f cudnn.tgz \
    && rm -rf cudnn/

# We expect that a volume with GPU drivers will be mounted at /usr/local/nvidia.
ENV CUDA_HOME=/usr/local/cuda
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib64:/usr/local/nvidia/lib64
ENV PATH=$PATH:/usr/local/cuda:/usr/local/nvidia/bin

# Copy and install the pipeline requirements.
COPY requirements.txt .
RUN pip install -U pip \
    && pip install -r requirements.txt
