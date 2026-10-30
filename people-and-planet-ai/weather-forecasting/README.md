# Weather Forecasting and Storm Risk Nowcasting

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_git_branch=feat/modernize-ppai-weather-forecasting&cloudshell_open_in_editor=people-and-planet-ai/weather-forecasting/README.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/feat/modernize-ppai-weather-forecasting/people-and-planet-ai/weather-forecasting/README.ipynb)
[![Open in Colab Enterprise](https://img.shields.io/badge/Open_in-Colab_Enterprise-4285F4?logo=googlecloud&logoColor=white)](https://console.cloud.google.com/agent-platform/colab/import/https:%2F%2Fraw.githubusercontent.com%2FGoogleCloudPlatform%2Fpython-docs-samples%2Ffeat%2Fmodernize-ppai-weather-forecasting%2Fpeople-and-planet-ai%2Fweather-forecasting%2FREADME.ipynb)
[![Open in Agent Platform Workbench](https://img.shields.io/badge/Open_in-Agent_Platform_Workbench-4285F4?logo=googlecloud&logoColor=white)](https://console.cloud.google.com/agent-platform/workbench/instances?download_url=https://raw.githubusercontent.com/GoogleCloudPlatform/python-docs-samples/feat/modernize-ppai-weather-forecasting/people-and-planet-ai/weather-forecasting/README.ipynb)

This sample demonstrates how to combine satellite observations and terrain elevation from [Google Earth Engine] with zero-shot time-series forecasting in [BigQuery ML] (`AI.FORECAST` powered by **TimesFM 2.5**) and multimodal storm-risk synthesis using **Gemini 3.8 Flash** (`google-genai` SDK).

## Architecture & Atomic Tasks

The end-to-end interactive workflow is consolidated in [`README.ipynb`](README.ipynb) and backed by standalone, single-task Python modules:

* **[`fetch_weather_patch.py`](fetch_weather_patch.py)**: Queries calibrated half-hourly precipitation from **NASA GPM IMERG V07** (`NASA/GPM_L3/IMERG_V07`), geostationary cloud and moisture channels from **NOAA GOES-19** (`NOAA/GOES/19/MCMIPF`) or **GOES-16** (`NOAA/GOES/16/MCMIPF`), and surface elevation from **MERIT DEM** (`MERIT/DEM/v1_0_3`) via the Earth Engine High Volume API (`ee.data.computePixels`).
* **[`load_weather_time_series.py`](load_weather_time_series.py)** (`dataflow_weather_load_time_series`): Runs an [Apache Beam] / [Dataflow] pipeline to populate a [BigQuery] table (`storm_hourly_observations`) with hourly storm precipitation, cloud moisture, and elevation observations.
* **[`forecast_precipitation.py`](forecast_precipitation.py)** (`bigquery_weather_forecast_precipitation`): Executes zero-shot time-series precipitation nowcasting (+6 hour horizon with 90% prediction intervals) in [BigQuery ML] using `AI.FORECAST` and Google Research's **TimesFM 2.5** foundation model.
* **[`analyze_storm_risk.py`](analyze_storm_risk.py)** (`googlegenaisdk_weather_analyze_storm_risk`): Combines the 3-panel satellite and DEM composite image (`types.Part.from_bytes`) with the `AI.FORECAST` trajectory using `gemini-3.8-flash` on the `global` endpoint and a Pydantic `StormRiskAssessment` response schema.
* **[`visualize.py`](visualize.py)**: Renders interactive Plotly figures for GOES cloud/moisture, GPM IMERG V07 rainfall, MERIT DEM elevation, and `AI.FORECAST` confidence bands.

### Featured Storm Case Studies & WeatherNext

* **Hurricane Melissa (`2025-10-28T17:00:00Z`, Jamaica Landfall)**: Category 5 landfall in southwestern Jamaica (`18.1N, 78.0W`), showcasing coastal rainbands interacting with the Blue Mountains (`2,256 m` peak elevation) and highlighted in [`README.ipynb`](README.ipynb) alongside **Google DeepMind [WeatherNext]** (`weathernext_3_0_0_0p1deg` and `weathernext_2_0_0`).
* **Hurricane Helene (`2024-09-27T06:00:00Z`, Southern Appalachians)**: Historic inland atmospheric moisture plume interacting with Blue Ridge mountain topography (`35.60N, 82.55W`, up to `2,037 m` elevation).
* **Customizable Local Current Weather Forecasting (`San Francisco Bay Area, CA` or any coordinates)**: Automatically selects **GOES-18 West** (`NOAA/GOES/18/MCMIPF`) for Western longitudes (`longitude < -105.0°`) or **GOES-19 East** (`NOAA/GOES/19/MCMIPF`) for Eastern longitudes, pairs live 10-minute cloud/marine-layer imagery with **MERIT DEM** topography and the latest operational **NOAA GFS (`NOAA/GFS0P25`)** 72-hour forecast trajectory, and synthesizes a localized microclimate report with `gemini-3.8-flash`.

## Running Locally or in Google Cloud

```bash
pip install -r requirements.txt

# 1. Fetch a multi-band storm patch from Earth Engine
python fetch_weather_patch.py "$GOOGLE_CLOUD_PROJECT"

# 2. Load hourly storm observations into BigQuery with Apache Beam
python load_weather_time_series.py \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --dataset=weather_forecasting \
  --table=storm_hourly_observations \
  --runner=DirectRunner \
  --temp_location="gs://$BUCKET_NAME/temp"

# 3. Forecast precipitation for the next 6 hours with BigQuery ML AI.FORECAST (TimesFM 2.5)
python forecast_precipitation.py "$GOOGLE_CLOUD_PROJECT" weather_forecasting storm_hourly_observations

# 4. Generate a structured multimodal storm & flood-risk report with Gemini 3.8 Flash
python analyze_storm_risk.py "$GOOGLE_CLOUD_PROJECT" storm_composite.png
```

## Running Tests

```bash
pytest test_weather_forecasting.py
```

[Google Earth Engine]: https://earthengine.google.com/
[Apache Beam]: https://beam.apache.org/
[Dataflow]: https://cloud.google.com/dataflow/docs
[BigQuery]: https://cloud.google.com/bigquery/docs
[BigQuery ML]: https://cloud.google.com/bigquery/docs/timesfm-model
[WeatherNext]: https://developers.google.com/weathernext/guides/models
