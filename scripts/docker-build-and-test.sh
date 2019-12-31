#!/usr/bin/env sh

set -e

cd $(dirname $0)/..

docker build -t vanillaslice/dawdle-test -f ./docker/test.Dockerfile .
docker run vanillaslice/dawdle-test /opt/app/scripts/all-tests.sh
