#!/usr/bin/env bash

set -e

cd $(dirname $0)/../..

pytest tests \
  --cov=dawdle \
  --cov-fail-under=95 \
  --cov-report=term-missing \
  --pythonwarnings=ignore::DeprecationWarning
