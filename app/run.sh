#!/bin/sh
TYPE_SELECTED=$1

docker run -it -p 8888:8888 --env-file google_env_vars.env \
    -v "$(pwd)/keys:/keys" \
    "${TYPE_SELECTED}_dockerfile"

