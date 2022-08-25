FROM continuumio/miniconda3 as build

COPY ./deploy/conda/env.yml .
COPY ./app.py .
COPY ./connect_azure.py .

# Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

RUN conda env create -f env.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n azuremlops_venv -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# Initialize conda in bash config fiiles:
RUN conda init bash

# Activate the environment, and make sure it's activated:
RUN echo "conda activate azuremlops_venv" > ~/.bashrc


FROM debian:buster as run
COPY --from=build /venv /venv
COPY --from=build /app.py .
COPY --from=build /connect_azure.py .

# Enable below line with valid access key
ENV AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=gangadharstorageaccount;AccountKey=nrzyZOjZmczt1nIZ4cuoIIM74zCS5z12tVw6Rk79TLGMzyCgP3ou8IHmTdw0eZr7Sk8dCj6NM7EC+ASt1JF5ew==;EndpointSuffix=core.windows.net"
ENV FLASK_DEBUG=1

SHELL ["/bin/bash", "-c"]

ENTRYPOINT source /venv/bin/activate && gunicorn --timeout 1000 --workers 1 --threads 4 --log-level debug --bind 0.0.0.0:5000 app:app
# ENTRYPOINT source /venv/bin/activate && python app.py