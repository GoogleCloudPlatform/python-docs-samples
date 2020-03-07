FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

RUN mkdir -p /cloud/dataflow

COPY streaming_beam.py /cloud/dataflow
COPY requirements.txt /cloud/dataflow

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE /cloud/dataflow/requirements.txt
ENV FLEX_TEMPLATE_PYTHON_PY_FILE /cloud/dataflow/streaming_beam.py

RUN pip install -U -r /cloud/dataflow/requirements.txt
