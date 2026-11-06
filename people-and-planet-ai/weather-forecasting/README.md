# 🌦 Weather Forecasting and Storm Risk Nowcasting

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_git_branch=feat/modernize-ppai-weather-forecasting&cloudshell_open_in_editor=people-and-planet-ai/weather-forecasting/README.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/feat/modernize-ppai-weather-forecasting/people-and-planet-ai/weather-forecasting/README.ipynb)
[![Open in Colab Enterprise](https://img.shields.io/badge/Open_in-Colab_Enterprise-4285F4?logo=googlecloud&logoColor=white)](https://console.cloud.google.com/agent-platform/colab/import/https:%2F%2Fraw.githubusercontent.com%2FGoogleCloudPlatform%2Fpython-docs-samples%2Ffeat%2Fmodernize-ppai-weather-forecasting%2Fpeople-and-planet-ai%2Fweather-forecasting%2FREADME.ipynb)

> [Watch the video on YouTube ![thumbnail](https://img.youtube.com/vi/6-UJzEXMvGY/0.jpg)](https://youtu.be/6-UJzEXMvGY)

Forecast hourly precipitation and synthesize localized flood-risk reports by combining multi-resolution satellite and elevation data from [Google Earth Engine] with zero-shot time-series forecasting in [BigQuery ML] (`AI.FORECAST` powered by **TimesFM 2.5**), global ensemble forecasts from [WeatherNext], and multimodal analysis with **Gemini 3.8 Flash** (`google-genai` SDK).

* **Multi-resolution satellite and terrain ingestion**: **NASA GPM IMERG V07**, **NOAA GOES-19 / GOES-18 / GOES-16**, and **MERIT DEM** from [Google Earth Engine]
* **Time-series ingestion pipeline**: [Apache Beam] on [Dataflow] writing structured storm observation tables to [BigQuery]
* **Zero-shot time-series forecasting**: **TimesFM 2.5** via `AI.FORECAST` in [BigQuery ML]
* **Global 64-member ensemble forecasting**: **WeatherNext 3** (`weathernext_3_0_0_0p1deg`) via [Google Earth Engine]
* **Multimodal flood-risk synthesis**: **Gemini 3.8 Flash** (`gemini-3.8-flash`) via the [Google Gen AI SDK]

## Included files

* **[`README.ipynb`](README.ipynb)**: Interactive tutorial notebook walking through historical hurricane hindcasting (Steps 1–5) and live San Francisco & Monterey Bay microclimate forecasting (Step 6).
* **[`fetch_weather_patch.py`](fetch_weather_patch.py)** (`earthengine_weather_fetch_patch`): Queries calibrated half-hourly precipitation from **NASA GPM IMERG V07** (`NASA/GPM_L3/IMERG_V07`), geostationary cloud and moisture channels from **NOAA GOES-19 / GOES-18 / GOES-16**, surface elevation from **MERIT DEM** (`MERIT/DEM/v1_0_3`), and **WeatherNext 3** ensemble trajectories via the Earth Engine High Volume API (`ee.data.computePixels`).
* **[`load_weather_time_series.py`](load_weather_time_series.py)** (`dataflow_weather_load_time_series`): Runs an [Apache Beam] / [Dataflow] pipeline to populate a [BigQuery] table (`storm_hourly_observations`) with hourly storm precipitation, cloud moisture, and elevation observations.
* **[`forecast_precipitation.py`](forecast_precipitation.py)** (`bigquery_weather_forecast_precipitation`): Executes zero-shot time-series precipitation nowcasting (+6 hour horizon with 90% prediction intervals) in [BigQuery ML] using `AI.FORECAST` and Google Research's **TimesFM 2.5** foundation model.
* **[`analyze_storm_risk.py`](analyze_storm_risk.py)** (`googlegenaisdk_weather_analyze_storm_risk`): Combines the 4-panel satellite and DEM multi-band strip (`types.Part.from_bytes`) with the `AI.FORECAST` trajectory using `gemini-3.8-flash` on the `global` endpoint and a Pydantic `StormRiskAssessment` response schema.
* **[`visualize.py`](visualize.py)**: Renders interactive Plotly figures and multi-band PNG strips for GOES cloud/moisture, GPM IMERG V07 rainfall, MERIT DEM elevation, `AI.FORECAST` confidence bands, **WeatherNext 3** ensemble plumes, and Bay Area microclimate comparisons.

## Featured case studies

* **Hurricane Melissa (`2025-10-28T17:00:00Z`, Jamaica Landfall)**: Category 5 landfall in southwestern Jamaica (`18.1N, 78.0W`), showcasing coastal rainbands interacting with the Blue Mountains (`2,256 m` peak elevation) alongside **Google DeepMind [WeatherNext]** (`weathernext_3_0_0_0p1deg`). To inspect another historical storm, pass its UTC `iso_time`, `latitude`, and `longitude` to `fetch_weather_patch.get_storm_patch_arrays()` and load its hourly observations into BigQuery.
* **Live Current Weather & Bay Area Microclimates (`San Francisco, Palo Alto, San Jose, Santa Cruz & Monterey`)**: Automatically selects **GOES-18 West** (`NOAA/GOES/18/MCMIPF`) for Western longitudes (`longitude < -105.0°`) or **GOES-19 East** (`NOAA/GOES/19/MCMIPF`) for Eastern longitudes, pairs live 10-minute cloud/marine-layer imagery with **MERIT DEM** topography, 2.5 km **NOAA RTMA** surface analyses, and 72-hour **NOAA GFS (`NOAA/GFS0P25`)** forecasts, and synthesizes a localized microclimate report with `gemini-3.8-flash`.

## Running locally or in Google Cloud

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
python analyze_storm_risk.py "$GOOGLE_CLOUD_PROJECT" storm_multiband_strip.png
```

## Running tests

```bash
pytest test_weather_forecasting.py
```

[Apache Beam]: https://beam.apache.org/
[BigQuery]: https://cloud.google.com/bigquery/docs
[BigQuery ML]: https://cloud.google.com/bigquery/docs/timesfm-model
[Dataflow]: https://cloud.google.com/dataflow/docs
[Google Earth Engine]: https://earthengine.google.com/
[Google Gen AI SDK]: https://googleapis.github.io/python-genai/
[WeatherNext]: https://developers.google.com/weathernext/guides/models
