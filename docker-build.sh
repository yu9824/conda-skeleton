#!/bin/bash

# config
source $(dirname $0)/_config.sh

# build
docker image build --build-arg username=$USERNAME -t yu9824/conda-skeleton .