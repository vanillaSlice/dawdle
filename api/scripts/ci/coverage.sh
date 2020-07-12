#!/usr/bin/env bash

set -e

cd $(dirname "$0")/../..

if [[ -z "$CI" ]]; then
  echo "Must be run by CI server."
  exit 1
fi

docker cp $(docker ps -l -q):/opt/app/.coverage .coverage.tmp
pip install coverage
coverage combine
coverage xml
