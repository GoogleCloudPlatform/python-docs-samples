import os
import tempfile

from google.cloud import storage
from google.cloud.storage.blob import Blob
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Data information
DATA_DIR = os.path.join(tempfile.gettempdir(), 'final_data')
BUCKET_NAME = 'citibikevd'
DATA_FOLDER = 'feature_engineering'
NUM_FEATURES = 11
TRAINING_FILE = 'final_data.csv'
TRAINING_BLOB = f'{DATA_FOLDER}/{TRAINING_FILE}'

# Get bucket information
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)


def load_data():
    '''Loads data from GCS bucket into training and testing dataframes'''
    # Download data from GCS bucket
    tf.io.gfile.makedirs(DATA_DIR)
    training_file_path = f'{DATA_DIR}/training.csv'
    bucket.blob(TRAINING_BLOB).download_to_filename(training_file_path)
    print('Downloaded file: ' + training_file_path)

    # Load data into dataframes
    df = pd.read_csv(training_file_path, low_memory=False)
    df = df.drop(df.columns[0], axis=1)

    # Extract feature and target columns
    x = df.iloc[:, :NUM_FEATURES]
    y = df.iloc[:, NUM_FEATURES:-1]

    # Split datasets into training and testing
    train_x, eval_x, train_y, eval_y = train_test_split(x, y, test_size=0.2)

    return train_x, train_y, eval_x, eval_y

def copy_file_to_GCS(filename, destination):
    '''Copies filename from working directory into GCS bucket'''
    if not destination.endswith('/'):
        destination = destination + '/'
    print(destination)
    blob = Blob.from_string(destination + filename, client=client)
    blob.upload_from_filename(filename)
    print('hello..?')
