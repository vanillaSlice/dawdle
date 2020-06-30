#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

docker build -t vanillaslice/dawdle-back-end-test -f ./docker/test.Dockerfile .
docker run vanillaslice/dawdle-back-end-test
