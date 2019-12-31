#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

pip install coveralls
coverage combine
coveralls
