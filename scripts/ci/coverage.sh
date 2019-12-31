#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

pip install coveralls
mv .coverage .coverage.tmp
coverage combine
coveralls
