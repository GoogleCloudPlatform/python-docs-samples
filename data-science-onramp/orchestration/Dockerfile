# Dockerfile
FROM python:3.9-slim

# # Installs google cloud sdk
# RUN wget -nv \
#     https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
#     mkdir /root/tools && \
#     tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
#     rm google-cloud-sdk.tar.gz && \
#     /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
#         --path-update=false --bash-completion=false \
#         --disable-installation-options && \
#     rm -rf /root/.config/* && \
#     ln -s /r

# # Path configuration
# ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
# # Make sure gsutil will use the default service account
# RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

# # Copies feature engineering code and dependencies
# COPY resources/feature_engineering.py /root
# COPY resources/requirements.txt /root

COPY ../feature_engineering/feature_engineering.ipynb .
COPY ../feature_engineering/requirements.txt .


# Installs feature engineering dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Convert the feature engineering notebook to a Python script
RUN jupyter nbconvert \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags test \
    --ClearOutputPreprocessor.enabled=True \
    --to python feature_engineering.ipynb

# Sets entry point to run feature engineering script
ENTRYPOINT ["python", "feature_engineering.py"]
