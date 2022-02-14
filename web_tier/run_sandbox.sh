#!/bin/bash

set -e

ID="$1"
FILE_BASE_64="$2"

docker build -f sandbox/Dockerfile -t "datapane-sandbox-$ID" --build-arg ID="$ID" --build-arg FILE_BASE_64="$FILE_BASE_64" .

docker run -d --rm -e ID="$ID" --network=datapane_frontend -v /var/run/docker.sock:/var/run/docker.sock "datapane-sandbox-$ID"