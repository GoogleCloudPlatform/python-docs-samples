
# [START ai_platform_utils]
# [START ai_platform_utils_imports]
import os
import pandas as pd
from sklearn.model_selection import train_test_split
# [END ai_platform_utils_imports]

# [START ai_platform_utils_load_data]
def load_data(input_path):
    """Loads data from GCS bucket into training and testing dataframes"""
    # Download data from GCS bucket and load data into dataframes
    df = pd.read_csv(input_path, low_memory=False)
    df = df.drop(df.columns[0], axis=1)

    # Extract feature and target columns
    x = df.iloc[:, :-1]
    y = df.iloc[:, -1:]

    # Split datasets into training and testing data. This will return four sets of data
    return train_test_split(x, y, test_size=0.2)
# [END ai_platform_utils_load_data]
# [END ai_platform_utils]

