#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

docker build -t vanillaslice/dawdle-test -f ./docker/test.Dockerfile .
docker run -v $(pwd):/opt/app vanillaslice/dawdle-test /opt/app/scripts/all-tests.sh
