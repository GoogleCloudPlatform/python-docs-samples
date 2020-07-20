import os
import tempfile
import numpy as np
import pandas as pd
import tensorflow as tf

from google.cloud import storage
from sklearn.model_selection import train_test_split

# Data information
DATA_DIR = os.path.join(tempfile.gettempdir(), 'final_data')
BUCKET_NAME = 'citibikevd'
DATA_FOLDER = 'feature_engineering'
NUM_FEATURES = 11
TRAINING_FILE = 'final_data.csv'
TRAINING_BLOB = f'{DATA_FOLDER}/{TRAINING_FILE}'

# Hyperparameters
BATCH_SIZE = 128
NUM_EPOCHS = 20
LEARNING_RATE = .01

# Get bucket information
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)


def extract_labels(df):
    '''Extract the target columns of the dataset'''
    label_cols = []
    for col in range(NUM_FEATURES, len(df.columns)):
        label_cols.append(df.columns[col])
    return label_cols

def load_data():
    '''Loads data from GCS bucket into training and testing dataframes'''
    # Download data from GCS bucket
    tf.io.gfile.makedirs(DATA_DIR)
    training_file_path = f'{DATA_DIR}/training.csv'
    blob = bucket.blob(TRAINING_BLOB).download_to_filename(training_file_path)
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
