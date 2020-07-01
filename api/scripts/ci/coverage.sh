#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

docker cp $(docker ps -l -q):/opt/app/.coverage .coverage.tmp
pip install coverage
coverage combine
coverage xml
