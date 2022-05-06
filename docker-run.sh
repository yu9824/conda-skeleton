#!/bin/bash

# config
source $(dirname $0)/_config.sh

# run
docker container run -it --rm --name conda-skeleton --mount type="bind",src="$(pwd)/output/",dst="/home/$USERNAME/output" yu9824/conda-skeleton