#!/bin/bash
set -e

usage="$(basename "$0") [-h help] (-p push | -r run) [-b background] [-d delete] -- Dockerize the application.

Run this script from the docker directory. Without arguments it will build the image.

where:
    -h  show this help text
    -r  run container
    -b  if running container run in background
    -p  if you want to push to the docker registry
    -d  delete container and docker image"

# docker registry and repository if pushing
REGISTRY=""
REPOSITORY=""
# docker file name inside the docker directory
DOCKER_FILE="Dockerfile"
# port to run application on
port=5000

GIT_TAG=$(git log --pretty=format:'%h' -n 1)
NAME=$REPOSITORY

push=false
run=false
background=false
delete=false

while getopts 'hpbdrk:s:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    p) push=true;;
    b) background=true;;
    r) run=true;;
    d) delete=true;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done


if $delete; then
  echo "removing..."
  docker rm -f $NAME
  docker rmi -f "${NAME}:${GIT_TAG}"
else
  echo "building..."
  docker build --build-arg port=$port -t "${NAME}:${GIT_TAG}" -f $DOCKER_FILE ..
  if $push; then
    echo "tagging with repository name..."
    docker tag "${NAME}:${GIT_TAG}" "${ECR_REGISTRY}/${REPOSITORY}:${GIT_TAG}"
    echo "pushing..."
    docker push "${ECR_REGISTRY}/${REPOSITORY}:${GIT_TAG}"
  if $run; then
    if $background; then
      echo "running in the background..."
      docker run -d -p $port:$port -t "${NAME}:${GIT_TAG}"
    else
      echo "running..."
      docker run -p $port:$port -t "${NAME}:${GIT_TAG}"
    fi
  fi
fi
