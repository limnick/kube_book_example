#!/bin/sh
TYPE_SELECTED=$1

docker build -t "${TYPE_SELECTED}_dockerfile" \
             -f "${TYPE_SELECTED}.Dockerfile" .



