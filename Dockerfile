# base image
FROM continuumio/miniconda3:4.3.11

# about
LABEL description=""
LABEL version=""
LABEL maintainer=""

# in the paths below substitute paths with your own
# substitue:
#  - app-skeleton (application name)
#  - dummypackage (own package name)
#  - conda_env (name of conda environment in environment_docker.yml)

# create virtual environment and clean leftovers
COPY environment_docker.yml /app-skeleton/environment_docker.yml
RUN conda env create -f /app-skeleton/environment_docker.yml && \
    conda clean --tarballs --packages -y

# copy application directory to container
COPY app /app-skeleton/app

# copy package directory to container
COPY dummypackage /app-skeleton/dummypackage

# port to run application on
ARG port
EXPOSE $port

# add package to python's path
ENV PYTHONPATH $PYTHONPATH:/app-skeleton

ENTRYPOINT ["/opt/conda/envs/conda_env/bin/python", "/app-skeleton/app/run_app.py"]
