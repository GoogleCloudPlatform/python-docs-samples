# AutoML Tables Pipeline
- Launch training and prediction jobs for AutoML Tables with a single command. 
- Define your pipelines with YAML configuration files for easy reuse.
- Log parameters, operations, and results.

## Before you begin
Install the most recent google cloud packages and additional requirements.
```
pip install --upgrade google-cloud
pip install --upgrade google-cloud-automl
pip install -r requirements.txt
```
Set up service account authentication with an env variable or in cmd line at run
time with the `--json_key_filepath` arg.
```
export GOOGLE_APPLICATION_CREDENTIALS=path/to/json_key
```


## Defining a pipeline
YAML configuration files are used to manage an inventory of previously trained
models, or to act as a template for repeated jobs with shared parameters. As a
minimal example, consider a config file "my_config.yaml" with parameters:
```
dataset_display_name: my_dataset
dataset_input_path: bq://project.dataset.table
model_display_name: my_model
label_column: my_label
```
See the provided "example.yaml" and Configuration section below for more
details.

## Running a pipeline
Parameters can also be provided in the command line, and will take priority over
parameters in the config. Together they support a number of usage patterns, here
are the two most common repeated jobs.

#### Training job
Import a new dataset "my_dataset" then train a new model "my_model" with
`--build_dataset` and `--build_model`:
```
python run_pipeline.py \
    --project=my_project \
    --config_filename=config/my_config.yaml \
    --build_dataset \
    --build_model
```

#### Batch prediction job
Load "my_dataset" and "my_model" (default behavior) then make a batch
prediction with `--make_prediction`:
```
python run_pipeline.py \
    --project=my_project \
    --config_filename=config/my_config.yaml \    
    --predict_input_path=bq://project.dataset.table \
    --predict_output_path=bq://project \
    --make_prediction
```

## Project Structure
```
.
├── run_pipeline     # Script to run the Tables pipeline from the command line.
├── tables_config    # TablesConfig reads parameters from YAML and command line.
├── tables_client    # TablesClient adds helper functions for the AutoML client.
├── tables_pipeline  # TablesPipeline queues/executes operations with logging.
├── config/          # Directory to read YAML parameter config files from.
└── log/             # Directory to write logging files to.
```

## Configuration
YAML configuration files may be created in the config/ directory, an
example.yaml is provided as a basis, and detailed descriptions for all
parameters are provided below (X denotes required).

| Parameter              | Default        | Type   | Comments                                                                       |
|------------------------|----------------|--------|--------------------------------------------------------------------------------|
| project                | X              | String | Recommend setting through command line.                                        |
| location               | us-central1    | String | Location of compute resources.                                                 |
| build_dataset          | false          | Bool   | true builds a new dataset, false loads an old one.                             |
| build_model            | false          | Bool   | true builds a new model, false loads an old one.                               |
| make_prediction        | false          | Bool   | Make a batch prediction after loads/builds.                                    |
| dataset_display_name   | X              | String | A unique and informative < 32 char name.                                       |
| dataset_input_path     | X              | String | bq://project.dataset.table or gs://path/to/train/data                          |
| label_column           | X              | String | Label dtype determines if regression or classification.                        |
| weight_column          | null           | String | Weights loss and evaluation metrics.                                           |
| split_column           | null           | String | Manually split data, time column is preferred.                                 |
| time_column            | null           | String | TIMESTAMP type column, auto split data on it.                                  |
| columns_nullable       | null           | Dict   | Only modify columns detected differently than intended (display name to bool). |
| columns_dtype          | null           | Dict   | Only modify columns detected differently than intended (display name to str).  |
| model_display_name     | X              | String | A unique and informative < 32 char name.                                       |
| train_hours            | 1.0            | Float  | Maximum time for training, must be >= 1.                                       |
| optimization_objective | null           | String | Recommend using defaults.                                                      |
| ignore_columns         | null           | List   | Columns (other than label/split/weight) to exclude in train.                   |
| predict_input_path     | X (if predict) | String | bq://project.dataset.table or gs://path/to/predict/data                        |
| predict_output_path    | X (if predict) | String | bq://project or gs://path/to/basedir (dataset.table or subdir generated).      |


## Logging
Log files are written to the log/ directory by default, but the directory and
filename can be set explicitly with the `--log_filepath` arg. Log levels can be
set by `--console_log_level` and `--console_log_level` args.

- Parameters are logged (in YAML format) at run time for reproducibility.
- Evaluation metrics and feature importance are logged during model load/build.
- Full output path logged during prediction.
- Operation names logged at INFO level, full responses at DEBUG.
