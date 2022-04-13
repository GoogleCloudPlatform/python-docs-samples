# Dockerfile
FROM python:3.9


# install the google cloud sdk
RUN curl https://sdk.cloud.google.com > install.sh && bash install.sh --disable-prompts 
ENV PATH $PATH:/root/google-cloud-sdk/bin
#TODO change to be a parameter
#RUN gcloud config set project leah-playground 

COPY feature_engineering.ipynb .
COPY requirements.txt .


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
