#!/usr/bin/env bash

set -e

cd $(dirname "$0")/../..

if [[ -z "$CI" ]]; then
  echo "Must be run by CI server."
  exit 1
fi

docker build -t vanillaslice/dawdle-api-test -f ./docker/test.Dockerfile .
docker run vanillaslice/dawdle-api-test
