#!/usr/bin/env bash

set -e

cd $(dirname $0)/..

pytest --cov=dawdle --cov-report=term-missing --cov-fail-under=90 -W ignore::DeprecationWarning
