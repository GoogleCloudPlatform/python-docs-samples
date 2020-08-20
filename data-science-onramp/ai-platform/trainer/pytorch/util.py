import os

from google.cloud import storage
import pandas as pd
import torch
from torch.utils.data import Dataset

BUCKET_NAME = 'citibikevd'
DATA_BLOB = f'feature_engineering/final_data.csv'

class CitibikeDataset(Dataset):

    def __init__(self, csv_path=None, download=True):
        """Represents the Citibike dataset."""
        # Define temp path if no specified csv path
        if csv_path is None:
            csv_path = '/tmp/citibike.csv'

        # Create directories for path if necessary
        if not os.path.isdir(os.path.dirname(csv_path)):
            os.mkdir(os.path.dirname(csv_path))

        # Add .csv extension to path
        if os.path.splitext(csv_path)[1] != '.csv':
            csv_path += '.csv'

        # Download data from GCS bucket
        if download:
            client = storage.Client()
            bucket = client.bucket(BUCKET_NAME)
            bucket.blob(DATA_BLOB).download_to_filename(csv_path)
            print('Downloaded Citibike data to ' + csv_path)

        # Read data into dataframe
        self.df = pd.read_csv(csv_path, index_col=0)

    def __getitem__(self, idx):
        # Get data and target from dataframe 
        NUM_FEATURES = 11
        x = self.df.iloc[idx, :NUM_FEATURES].to_numpy()
        y = self.df.iloc[idx, NUM_FEATURES:].to_numpy()

        # Convert to tensors
        x = torch.from_numpy(x).float()
        y = torch.from_numpy(y).float()

        return x, y

    def __len__(self):
        return len(self.df)
