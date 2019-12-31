#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

docker build -t vanillaslice/dawdle-test -f ./docker/test.Dockerfile .
docker run vanillaslice/dawdle-test
docker cp $(docker ps -l -q):/opt/app/.coverage .coverage.tmp
