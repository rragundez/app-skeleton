# base image
FROM continuumio/miniconda3:4.3.11

# about
LABEL description=""
LABEL version=""
LABEL maintainer=""

# define project variables
ENV APPLICATION_NAME dummy_application
ENV PACKAGE_NAME dummypackage
ENV VIRTUAL_ENVIRONMENT conda_environment_name

# create virtual environment and clean leftovers
COPY docker/environment_docker.yml /$APPLICATION_NAME/environment_docker.yml
RUN conda env create -f /$APPLICATION_NAME/environment_docker.yml && \
    conda clean --tarballs --packages -y

# copy application directory to container
COPY app /$APPLICATION_NAME/app

# copy package directory to container
COPY $PACKAGE_NAME /$APPLICATION_NAME/$PACKAGE_NAME

# port to run application on
ARG port=5000
EXPOSE $port

# add package to python's path
ENV PYTHONPATH $PYTHONPATH:/$APPLICATION_NAME/$PACKAGE_NAME
ENV FLASK_APP /$APPLICATION_NAME/app/app.py

ENTRYPOINT ["/opt/conda/envs/$VIRTUAL_ENVIRONMENT/bin/python", "/$APPLICATION_NAME/app/app.py"]
CMD ["--host", "127.0.0.1", "--port", $port, "--workers", "1", "--threads", "1", "--log-level", "debug"]
